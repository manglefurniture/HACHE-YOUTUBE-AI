#!/usr/bin/env python3
"""Stream verified official model files to fixed private R2 shared keys."""
import argparse
import hashlib
import os
import sys
import urllib.request

BUCKET = "hache-ai-models"
PART_SIZE = 64 * 1024 * 1024
READ_SIZE = 8 * 1024 * 1024

MODELS = {
    "juggernaut-xl-ragnarok": {
        "source": "https://huggingface.co/Kandoo/Juggernaut-XL-Ragnarok/resolve/main/juggernautXL_ragnarok.safetensors",
        "source_name": "Kandoo/Juggernaut-XL-Ragnarok",
        "key": "shared/checkpoints/juggernautXL_ragnarok.safetensors",
        "size": 7_105_350_162,
        "sha256": "dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a",
    },
    "clip-vit-h-14": {
        "source": "https://huggingface.co/Comfy-Org/CLIP-ViT-H-14-laion2B-s32B-b79K_repackaged/resolve/main/split_files/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "source_name": "Comfy-Org/CLIP-ViT-H-14-laion2B-s32B-b79K_repackaged",
        "key": "shared/clip_vision/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors",
        "size": 2_528_373_448,
        "sha256": "6ca9667da1ca9e0b0f75e46bb030f7e011f44f86cbfb8d5a36590fcd7507b030",
    },
}


def hash_r2(client, key, expected_sha):
    response = client.get_object(Bucket=BUCKET, Key=key)
    declared_size = response["ContentLength"]
    digest = hashlib.sha256()
    total = 0
    body = response["Body"]
    try:
        while True:
            chunk = body.read(READ_SIZE)
            if not chunk:
                break
            total += len(chunk)
            digest.update(chunk)
    finally:
        body.close()
    actual = digest.hexdigest()
    if total != declared_size:
        raise RuntimeError(f"R2 readback length mismatch: {total} != {declared_size}")
    if actual != expected_sha:
        raise RuntimeError(f"R2 SHA256 mismatch for {key}: {actual}")
    return total, actual


def existing_object(client, model):
    from botocore.exceptions import ClientError

    try:
        head = client.head_object(Bucket=BUCKET, Key=model["key"])
    except ClientError as exc:
        code = str(exc.response.get("Error", {}).get("Code", ""))
        status = exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if code in {"404", "NoSuchKey", "NotFound"} or status == 404:
            return False
        raise
    if head["ContentLength"] != model["size"]:
        raise RuntimeError(
            f"Refusing to overwrite {model['key']}: existing object has a different size"
        )
    actual_size, actual_sha = hash_r2(client, model["key"], model["sha256"])
    if actual_size != model["size"] or actual_sha != model["sha256"]:
        raise RuntimeError(f"Refusing to overwrite mismatched object: {model['key']}")
    print(
        f"ALREADY_VERIFIED_R2 bucket={BUCKET} key={model['key']} "
        f"bytes={actual_size} sha256={actual_sha}",
        flush=True,
    )
    return True


def ingest(client, model):
    if existing_object(client, model):
        return

    request = urllib.request.Request(
        model["source"], headers={"User-Agent": "Hache-AI-model-ingest/1.0"}
    )
    digest = hashlib.sha256()
    total = 0
    parts = []
    upload_id = None
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            if response.status != 200:
                raise RuntimeError(f"Source returned HTTP {response.status}")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) != model["size"]:
                raise RuntimeError(
                    f"Source size mismatch: {content_length} != {model['size']}"
                )

            upload = client.create_multipart_upload(
                Bucket=BUCKET,
                Key=model["key"],
                ContentType="application/octet-stream",
                Metadata={"source": model["source_name"]},
            )
            upload_id = upload["UploadId"]
            number = 1
            while True:
                part = bytearray()
                while len(part) < PART_SIZE:
                    chunk = response.read(min(READ_SIZE, PART_SIZE - len(part)))
                    if not chunk:
                        break
                    part.extend(chunk)
                    digest.update(chunk)
                    total += len(chunk)
                if not part:
                    break
                result = client.upload_part(
                    Bucket=BUCKET,
                    Key=model["key"],
                    UploadId=upload_id,
                    PartNumber=number,
                    Body=bytes(part),
                )
                parts.append({"PartNumber": number, "ETag": result["ETag"]})
                print(f"Uploaded part {number}; streamed_bytes={total}", flush=True)
                number += 1

        actual_source_sha = digest.hexdigest()
        if total != model["size"]:
            raise RuntimeError(f"Source size mismatch: {total} != {model['size']}")
        if actual_source_sha != model["sha256"]:
            raise RuntimeError(f"Source SHA256 mismatch: {actual_source_sha}")

        client.complete_multipart_upload(
            Bucket=BUCKET,
            Key=model["key"],
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
        upload_id = None

        head = client.head_object(Bucket=BUCKET, Key=model["key"])
        if head["ContentLength"] != total:
            raise RuntimeError(f"R2 size mismatch: {head['ContentLength']} != {total}")
        readback_size, readback_sha = hash_r2(client, model["key"], model["sha256"])
        if readback_size != total:
            raise RuntimeError(f"R2 readback size mismatch: {readback_size} != {total}")
        print(
            f"VERIFIED_R2 bucket={BUCKET} key={model['key']} bytes={readback_size} "
            f"sha256={readback_sha}",
            flush=True,
        )
    except BaseException:
        if upload_id is not None:
            try:
                client.abort_multipart_upload(
                    Bucket=BUCKET, Key=model["key"], UploadId=upload_id
                )
            except Exception as abort_error:
                print(f"Warning: multipart abort failed: {abort_error}", file=sys.stderr)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=sorted(MODELS))
    args = parser.parse_args()
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
    ingest(client, MODELS[args.model])


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
