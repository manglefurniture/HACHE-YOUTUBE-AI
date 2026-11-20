#!/usr/bin/env python3
"""Stream pinned public ComfyUI model files from Hugging Face into private R2.

Downloads only the explicit public-source allowlist below. Model bytes stay in
memory in bounded chunks; each upload is checked against its pinned SHA-256 and
size before completion, then read back from R2 and checked again.
"""
import argparse
import hashlib
import os
import re
import sys
import urllib.request
import uuid

MODELS = {
    "juggernaut": {
        "repo": "JCTN/Juggernaut",
        "revision": "afebc79ee66301a5dc5121728573bf359a2a7b8c",
        "source_path": "juggernautXL_ragnarokBy.safetensors",
        "filename": "juggernautXL_ragnarok.safetensors",
        "destination": "checkpoints",
        "size": 7105350162,
        "sha256": "dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a",
    },
    "clip_vision": {
        "repo": "h94/IP-Adapter",
        "revision": "0859e809306db97aa2338e370587ab284e8a754f",
        "source_path": "models/image_encoder/model.safetensors",
        "filename": "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "destination": "clip_vision",
        "size": 2528373448,
        "sha256": "6ca9667da1ca9e0b0f75e46bb030f7e011f44f86cbfb8d5a36590fcd7507b030",
    },
    "faceid_adapter": {
        "repo": "h94/IP-Adapter-FaceID",
        "revision": "36ce7f96f0c76c1e8b100f10fa094a2ac48ea1c6",
        "source_path": "ip-adapter-faceid-plusv2_sdxl.bin",
        "filename": "ip-adapter-faceid-plusv2_sdxl.bin",
        "destination": "ipadapter",
        "size": 1487555181,
        "sha256": "c6945d82b543700cc3ccbb98d363b837e9c596281607857c74b713a876daf5fb",
    },
    "faceid_lora": {
        "repo": "h94/IP-Adapter-FaceID",
        "revision": "6eba56f2a87a7ebb2ef5a7737fe6c74df05f1f58",
        "source_path": "ip-adapter-faceid-plusv2_sdxl_lora.safetensors",
        "filename": "ip-adapter-faceid-plusv2_sdxl_lora.safetensors",
        "destination": "loras/ipadapter",
        "size": 371842896,
        "sha256": "f24b4bb2dad6638a09c00f151cde84991baf374409385bcbab53c1871a30cb7b",
    },
    "face_detector": {
        "repo": "Bingsu/adetailer",
        "revision": "103b6d3f064975e94b02715bfe5e873c1d1b5862",
        "source_path": "face_yolov8m.pt",
        "filename": "face_yolov8m.pt",
        "destination": "ultralytics/bbox",
        "size": 51996128,
        "sha256": "e3893a92c5c1907136b6cc75404094db767c1e0cfefe1b43e87dad72af2e4c9f",
    },
}
ALL_PUBLIC = "all-public-comfyui"


def expected_key(prefix, run_id, model):
    return f"{prefix}{model['destination']}/{run_id}/{model['filename']}"


def readback_and_verify(client, bucket, key, model):
    response = client.get_object(Bucket=bucket, Key=key)
    digest = hashlib.sha256()
    total = 0
    body = response["Body"]
    try:
        while True:
            chunk = body.read(8 * 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
    finally:
        body.close()
    if total != model["size"] or total != response["ContentLength"]:
        raise RuntimeError(f"R2 readback size mismatch for {key}: {total} bytes")
    if digest.hexdigest() != model["sha256"]:
        raise RuntimeError(f"R2 readback SHA-256 mismatch for {key}")
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Upload; default is a no-transfer preview")
    parser.add_argument("--only", choices=[ALL_PUBLIC, *sorted(MODELS)], default=ALL_PUBLIC)
    args = parser.parse_args()

    prefix = os.environ.get("R2_PREFIX", "shared/comfyui-public/").strip("/") + "/"
    if ".." in prefix or not re.fullmatch(r"[A-Za-z0-9/_-]+/", prefix):
        raise ValueError("R2_PREFIX contains unsupported characters")
    bucket = os.environ.get("R2_BUCKET", "hache-ai-models")
    selected = list(MODELS.items()) if args.only == ALL_PUBLIC else [(args.only, MODELS[args.only])]
    run_id = uuid.uuid4().hex if args.execute else "<generated-on-upload>"

    for model_id, model in selected:
        url = (
            f"https://huggingface.co/{model['repo']}/resolve/"
            f"{model['revision']}/{model['source_path']}"
        )
        key = expected_key(prefix, run_id, model)
        print(
            f"{bucket}/{key} <- {url} bytes={model['size']} "
            f"sha256={model['sha256']}",
            flush=True,
        )
    if not args.execute:
        print("DRY RUN: no network transfer and no R2 writes")
        return

    account = os.environ["R2_ACCOUNT_ID"]
    import boto3
    from botocore.config import Config

    client = boto3.client(
        "s3",
        endpoint_url=f"https://{account}.r2.cloudflarestorage.com",
        config=Config(
            signature_version="s3v4",
            retries={"max_attempts": 5, "mode": "standard"},
        ),
    )

    for model_id, model in selected:
        key = expected_key(prefix, run_id, model)
        url = (
            f"https://huggingface.co/{model['repo']}/resolve/"
            f"{model['revision']}/{model['source_path']}"
        )
        request = urllib.request.Request(
            url, headers={"User-Agent": "Hache-AI-model-ingest/1.0"}
        )
        upload_id = None
        digest = hashlib.sha256()
        total = 0
        parts = []
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                if response.status != 200:
                    raise RuntimeError(f"Unexpected HTTP status {response.status}")
                upload = client.create_multipart_upload(Bucket=bucket, Key=key)
                upload_id = upload["UploadId"]
                part_number = 1
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
                    part = client.upload_part(
                        Bucket=bucket,
                        Key=key,
                        UploadId=upload_id,
                        PartNumber=part_number,
                        Body=b"".join(chunks),
                    )
                    parts.append({"PartNumber": part_number, "ETag": part["ETag"]})
                    part_number += 1

            if total != model["size"]:
                raise RuntimeError(f"Source size mismatch for {model_id}: {total} bytes")
            if digest.hexdigest() != model["sha256"]:
                raise RuntimeError(f"Source SHA-256 mismatch for {model_id}")

            client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )
            upload_id = None
            head = client.head_object(Bucket=bucket, Key=key)
            if head["ContentLength"] != model["size"]:
                client.delete_object(Bucket=bucket, Key=key)
                raise RuntimeError(f"R2 object size mismatch for {key}")
            try:
                readback_size = readback_and_verify(client, bucket, key, model)
            except Exception:
                client.delete_object(Bucket=bucket, Key=key)
                raise
            print(
                f"VERIFIED_R2 {key} bytes={readback_size} "
                f"sha256={model['sha256']}",
                flush=True,
            )
        except BaseException:
            if upload_id is not None:
                client.abort_multipart_upload(
                    Bucket=bucket, Key=key, UploadId=upload_id
                )
            raise


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
