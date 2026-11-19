#!/usr/bin/env python3
"""Stream public Wan model files from Hugging Face into private Cloudflare R2.

Requires: pip install boto3
Credentials: R2_ACCOUNT_ID, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Optional: R2_BUCKET (default hache-ai-models), R2_PREFIX (default shared/wan22/)
No VPS disk usage; bounded RAM; SHA-256 verification before completing multipart.
"""
import argparse
import hashlib
import os
import sys
import urllib.request

MODELS = {
    "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors": (
        "Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models",
        "6122e79d55e0f235698d11d657f3b196c5273c830da00b2b013c5a048d5e6a42"),
    "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors": (
        "Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models",
        "5471a457b6ac404202a5fbe6c11595a3d5641fc766b00f38763f72303fffc21e"),
    "umt5_xxl_fp8_e4m3fn_scaled.safetensors": (
        "Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/text_encoders",
        "c3355d30191f1f066b26d93fba017ae9809dce6c627dda5f6a66eaa651204f68"),
    "wan_2.1_vae.safetensors": (
        "Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/vae",
        "2fc39d31359a4b0a64f55876d8ff7fa8d780956ae2cb13463b0223e15148976b"),
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true", help="Actually upload (default is dry-run)")
    p.add_argument("--only", choices=sorted(MODELS))
    args = p.parse_args()
    bucket = os.environ.get("R2_BUCKET", "hache-ai-models")
    prefix = os.environ.get("R2_PREFIX", "shared/wan22/").strip("/") + "/"
    selected = {args.only: MODELS[args.only]} if args.only else MODELS
    for name, (repo, folder, sha) in selected.items():
        url = f"https://huggingface.co/{repo}/resolve/main/{folder}/{name}"
        print(f"{bucket}/{prefix}{name} <- {url} sha256={sha}", flush=True)
    if not args.execute:
        print("DRY RUN: no network transfer or R2 writes")
        return
    account = os.environ["R2_ACCOUNT_ID"]
    import boto3
    from botocore.config import Config
    client = boto3.client("s3", endpoint_url=f"https://{account}.r2.cloudflarestorage.com",
                          config=Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}))
    for name, (repo, folder, expected) in selected.items():
        key = prefix + name
        try:
            client.head_object(Bucket=bucket, Key=key)
        except client.exceptions.ClientError as e:
            if e.response["ResponseMetadata"]["HTTPStatusCode"] != 404:
                raise
        else:
            raise RuntimeError(f"Refusing to overwrite existing object: {key}")
        url = f"https://huggingface.co/{repo}/resolve/main/{folder}/{name}"
        request = urllib.request.Request(url, headers={"User-Agent": "Hache-AI-model-ingest/1.0"})
        upload_id = None
        digest = hashlib.sha256()
        parts = []
        total = 0
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                # 64 MiB chunks, assembled in memory. Never writes model bytes to disk.
                upload = client.create_multipart_upload(Bucket=bucket, Key=key)
                upload_id = upload["UploadId"]
                number = 1
                while True:
                    remaining = 64 * 1024 * 1024
                    chunks = []
                    while remaining:
                        chunk = response.read(min(1024 * 1024, remaining))
                        if not chunk:
                            break
                        chunks.append(chunk)
                        digest.update(chunk)
                        total += len(chunk)
                        remaining -= len(chunk)
                    if not chunks:
                        break
                    part = client.upload_part(Bucket=bucket, Key=key, UploadId=upload_id,
                                              PartNumber=number, Body=b"".join(chunks))
                    parts.append({"PartNumber": number, "ETag": part["ETag"]})
                    number += 1
            if digest.hexdigest() != expected:
                raise RuntimeError(f"SHA256 mismatch for {name}: {digest.hexdigest()}")
            client.complete_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id,
                                             MultipartUpload={"Parts": parts})
            upload_id = None
            head = client.head_object(Bucket=bucket, Key=key)
            if head["ContentLength"] != total:
                raise RuntimeError(f"R2 size mismatch for {key}")
            print(f"VERIFIED {key} bytes={total} sha256={expected}", flush=True)
        except BaseException:
            if upload_id is not None:
                client.abort_multipart_upload(Bucket=bucket, Key=key, UploadId=upload_id)
            raise

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
