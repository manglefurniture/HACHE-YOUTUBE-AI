#!/usr/bin/env python3
"""Read-only verification of the reusable ComfyUI model set from lucia-gpu."""
import argparse
import hashlib
import json
import os
from pathlib import Path

MODELS = {
    "checkpoints/juggernautXL_ragnarok.safetensors": "dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a",
    "diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors": "6122e79d55e0f235698d11d657f3b196c5273c830da00b2b013c5a048d5e6a42",
    "diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors": "5471a457b6ac404202a5fbe6c11595a3d5641fc766b00f38763f72303fffc21e",
    "text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors": "c3355d30191f1f066b26d93fba017ae9809dce6c627dda5f6a66eaa651204f68",
    "vae/wan_2.1_vae.safetensors": "2fc39d31359a4b0a64f55876d8ff7fa8d780956ae2cb13463b0223e15148976b",
}
def verify(root, hash_files):
    results = {}
    for name, expected in MODELS.items():
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
    args = parser.parse_args()
    results = verify(args.models_dir, args.hash)
    print(json.dumps({"models_dir": str(args.models_dir), "results": results}, indent=2))
    return 0 if all(v in ("ok", "present_unverified") for v in results.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
