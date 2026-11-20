#!/usr/bin/env python3
"""Fetch the fixed, public-only model allowlist from private Cloudflare R2."""
import hashlib
import json
import os
import random
import shutil
import sys
import time
from pathlib import Path

CHUNK_SIZE = 4 * 1024 * 1024
MAX_ATTEMPTS = 4
INVENTORY = Path(__file__).with_name("model-inventory.json")


def load_inventory():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    models = data["models"]
    if len(models) != 9 or len({m["path"] for m in models}) != 9:
        raise ValueError("Model inventory must contain nine unique destinations")
    for model in models:
        if Path(model["path"]).is_absolute() or ".." in Path(model["path"]).parts:
            raise ValueError("Model destination escapes the configured model directory")
        if not model["key"].startswith("shared/") or ".." in Path(model["key"]).parts:
            raise ValueError("Model key is outside the public shared prefix")
        if model["key"].startswith(("private/", "lucia/")) or "lucia" in model["key"].lower():
            raise ValueError("Private assets are not permitted in the public model inventory")
    return data["bucket"], models


def hash_file(path):
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def is_verified(path, model):
    if not path.is_file():
        return False
    size, digest = hash_file(path)
    return size == model["bytes"] and digest == model["sha256"]


def download_one(client, bucket, root, model):
    root = root.resolve()
    destination = root.joinpath(*Path(model["path"]).parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink() or not destination.resolve().is_relative_to(root):
        raise RuntimeError(f"Unsafe model destination: {model['path']}")
    if is_verified(destination, model):
        print(f"MODEL_READY {model['path']}", flush=True)
        return

    part = destination.with_name(destination.name + ".part")
    if part.is_symlink() or not part.resolve().is_relative_to(root):
        raise RuntimeError(f"Unsafe partial model path: {model['path']}")
    part.unlink(missing_ok=True)
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        digest = hashlib.sha256()
        total = 0
        try:
            response = client.get_object(Bucket=bucket, Key=model["key"])
            body = response["Body"]
            try:
                with part.open("wb") as stream:
                    while True:
                        chunk = body.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        stream.write(chunk)
                        digest.update(chunk)
                        total += len(chunk)
                    stream.flush()
                    os.fsync(stream.fileno())
            finally:
                body.close()
            if total != model["bytes"] or response.get("ContentLength") != total:
                raise ValueError("downloaded model size does not match inventory")
            if digest.hexdigest() != model["sha256"]:
                raise ValueError("downloaded model SHA-256 does not match inventory")
            os.replace(part, destination)
            print(f"MODEL_VERIFIED {model['path']} bytes={total} sha256={model['sha256']}", flush=True)
            return
        except Exception as exc:
            last_error = exc
            try:
                part.unlink(missing_ok=True)
            except OSError:
                pass
            if attempt < MAX_ATTEMPTS:
                time.sleep(min(2 ** (attempt - 1) + random.random(), 8))
    raise RuntimeError(
        f"Could not provision {model['path']} after {MAX_ATTEMPTS} attempts "
        f"({type(last_error).__name__})"
    )


def reclaim_stale_partials(root, models):
    root = root.resolve()
    for model in models:
        destination = root.joinpath(*Path(model["path"]).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.is_symlink() or not destination.resolve().is_relative_to(root):
            raise RuntimeError(f"Unsafe model destination: {model['path']}")
        part = destination.with_name(destination.name + ".part")
        if part.is_symlink():
            part.unlink()
        elif part.exists():
            if not part.resolve().is_relative_to(root):
                raise RuntimeError(f"Unsafe partial model path: {model['path']}")
            part.unlink()


def provision(root=None, client=None):
    bucket, models = load_inventory()
    root = Path(root or os.environ.get("HACHE_MODELS_DIR", "/workspace/models"))
    root.mkdir(parents=True, exist_ok=True)
    missing = [m for m in models if not is_verified(root.joinpath(*Path(m["path"]).parts), m)]
    if not missing:
        for model in models:
            print(f"MODEL_READY {model['path']}", flush=True)
        return

    reclaim_stale_partials(root, missing)
    required_bytes = sum(model["bytes"] for model in missing)
    for model in missing:
        existing = root.joinpath(*Path(model["path"]).parts)
        if existing.is_file():
            required_bytes += existing.stat().st_size
    required_bytes += max(1024**3, required_bytes // 20)
    if shutil.disk_usage(root).free < required_bytes:
        raise RuntimeError("Insufficient free space in the model volume for safe provisioning")

    if client is None:
        account = os.environ.get("R2_ACCOUNT_ID")
        if not account:
            raise RuntimeError("R2_ACCOUNT_ID is required to provision missing models")
        import boto3
        from botocore.config import Config

        client = boto3.client(
            "s3",
            endpoint_url=f"https://{account}.r2.cloudflarestorage.com",
            config=Config(
                signature_version="s3v4",
                retries={"max_attempts": 4, "mode": "standard"},
                connect_timeout=10,
                read_timeout=120,
            ),
        )

    for model in missing:
        download_one(client, bucket, root, model)


if __name__ == "__main__":
    try:
        provision()
    except Exception as exc:
        # Avoid printing SDK request details that can contain sensitive configuration.
        print(f"ERROR: model provisioning failed ({type(exc).__name__})", file=sys.stderr)
        sys.exit(1)
