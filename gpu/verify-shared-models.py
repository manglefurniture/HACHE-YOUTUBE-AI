#!/usr/bin/env python3
"""Read-only verification of the reusable ComfyUI model set from lucia-gpu."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from provision_models import load_inventory, select_models

_, _INVENTORY_MODELS = load_inventory()
MODELS = {model["path"]: model["sha256"] for model in _INVENTORY_MODELS}
def verify(root, hash_files, only="all"):
    results = {}
    selected_paths = {m["path"] for m in select_models(_INVENTORY_MODELS, only)}
    for name, expected in MODELS.items():
        if name not in selected_paths:
            continue
        path = root / name
        if not path.is_file():
            results[name] = "missing"
            continue
        if not hash_files:
            results[name] = "present_unverified"
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
                digest.update(chunk)
        results[name] = "ok" if digest.hexdigest() == expected else "hash_mismatch"
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", type=Path, default=Path(os.environ.get("HACHE_MODELS_DIR", "/workspace/models")))
    parser.add_argument("--hash", action="store_true", help="Hash large files; slower but validates integrity")
    parser.add_argument("--only", choices=("all", "juggernaut"), default="all",
                        help="Check just the image checkpoint for the staged template path")
    args = parser.parse_args()
    results = verify(args.models_dir, args.hash, only=args.only)
    print(json.dumps({"models_dir": str(args.models_dir), "results": results}, indent=2))
    return 0 if all(v in ("ok", "present_unverified") for v in results.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
