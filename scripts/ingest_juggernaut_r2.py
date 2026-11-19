#!/usr/bin/env python3
"""Stream the official Juggernaut XL Ragnarok checkpoint to private R2.

Downloads directly from the author's Hugging Face repository, keeps only bounded
multipart chunks in memory, validates the source SHA-256, completes the upload,
then reads the object back from R2 and verifies size and SHA-256.
"""
import hashlib
import os
import sys
import urllib.request

MODEL_NAME = "juggernautXL_ragnarok.safetensors"
SOURCE_URL = (
    "https://huggingface.co/Kandoo/Juggernaut-XL-Ragnarok/"
    "resolve/main/juggernautXL_ragnarok.safetensors"
)
EXPECTED_SHA256 = "dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a"
EXPECTED_SIZE = 7_105_350_162
BUCKET = "hache-ai-models"
KEY = "shared/checkpoints/juggernautXL_ragnarok.safetensors"
PART_SIZE = 64 * 1024 * 1024
READ_SIZE = 8 * 1024 * 1024


def sha256_r2(client):
    response = client.get_object(Bucket=BUCKET, Key=KEY)
    expected_size = response["ContentLength"]
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
    if total != expected_size:
        raise RuntimeError(f"R2 readback length mismatch: {total} != {expected_size}")
    actual = digest.hexdigest()
    if actual != EXPECTED_SHA256:
        raise RuntimeError(f"R2 readback SHA256 mismatch: {actual}")
    return total, actual


def main():
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

    request = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": "Hache-AI-model-ingest/1.0"}
    )
    upload_id = None
    digest = hashlib.sha256()
    total = 0
    parts = []
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            if response.status != 200:
                raise RuntimeError(f"Source returned HTTP {response.status}")
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) != EXPECTED_SIZE:
                raise RuntimeError(
                    f"Source size mismatch: {content_length} != {EXPECTED_SIZE}"
                )

            # Create the multipart upload only after source availability/headers pass.
            upload = client.create_multipart_upload(
                Bucket=BUCKET,
                Key=KEY,
                ContentType="application/octet-stream",
                Metadata={"source": "Kandoo/Juggernaut-XL-Ragnarok"},
            )
            upload_id = upload["UploadId"]
            number = 1

            while True:
                part_bytes = bytearray()
                while len(part_bytes) < PART_SIZE:
                    chunk = response.read(min(READ_SIZE, PART_SIZE - len(part_bytes)))
                    if not chunk:
                        break
                    part_bytes.extend(chunk)
                    digest.update(chunk)
                    total += len(chunk)
                if not part_bytes:
                    break
                result = client.upload_part(
                    Bucket=BUCKET,
                    Key=KEY,
                    UploadId=upload_id,
                    PartNumber=number,
                    Body=bytes(part_bytes),
                )
                parts.append({"PartNumber": number, "ETag": result["ETag"]})
                print(f"Uploaded part {number}; streamed_bytes={total}", flush=True)
                number += 1

        actual_source_hash = digest.hexdigest()
        if total != EXPECTED_SIZE:
            raise RuntimeError(f"Source size mismatch: {total} != {EXPECTED_SIZE}")
        if actual_source_hash != EXPECTED_SHA256:
            raise RuntimeError(f"Source SHA256 mismatch: {actual_source_hash}")

        client.complete_multipart_upload(
            Bucket=BUCKET,
            Key=KEY,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
        upload_id = None

        head = client.head_object(Bucket=BUCKET, Key=KEY)
        if head["ContentLength"] != total:
            raise RuntimeError(
                f"R2 object size mismatch: {head['ContentLength']} != {total}"
            )

        readback_size, readback_hash = sha256_r2(client)
        if readback_size != total:
            raise RuntimeError(f"R2 readback size mismatch: {readback_size} != {total}")
        print(
            f"VERIFIED_R2 bucket={BUCKET} key={KEY} bytes={readback_size} "
            f"sha256={readback_hash}",
            flush=True,
        )
    except BaseException:
        if upload_id is not None:
            try:
                client.abort_multipart_upload(
                    Bucket=BUCKET, Key=KEY, UploadId=upload_id
                )
            except Exception as abort_error:
                print(f"Warning: multipart abort failed: {abort_error}", file=sys.stderr)
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
