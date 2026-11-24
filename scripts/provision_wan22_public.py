#!/usr/bin/env python3
"""GPU provisioning of four public Wan 2.2 I2V assets pinned in GitHub."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import os
import subprocess
import time

ROOT = Path("/workspace/ComfyUI/models")
BASE22 = "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files"
BASE21 = "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files"
FILES = [
    ("diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", BASE22,
     14294742832, "6122e79d55e0f235698d11d657f3b196c5273c830da00b2b013c5a048d5e6a42"),
    ("diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", BASE22,
     14294742832, "5471a457b6ac404202a5fbe6c11595a3d5641fc766b00f38763f72303fffc21e"),
    ("text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", BASE21,
     6735906897, "c3355d30191f1f066b26d93fba017ae9809dce6c627dda5f6a66eaa651204f68"),
    ("vae/wan_2.1_vae.safetensors", BASE22,
     253815318, "2fc39d31359a4b0a64f55876d8ff7fa8d780956ae2cb13463b0223e15148976b"),
]
def check(path, expected_size, expected_hash):
    if not path.exists() or path.stat().st_size != expected_size: return False
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):sha.update(b)
    return sha.hexdigest()==expected_hash
def run_one(item):
    rel, base, size, sha = item
    dst = ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if check(dst,size,sha):
        print("ALREADY_VERIFIED",rel,flush=True)
        return True
    if dst.exists():raise RuntimeError("Existing invalid model; refuse overwrite: "+rel)
    temp = dst.with_name(dst.name+".part")
    url = base + "/" + rel
    print("DOWNLOAD_BEGIN",rel,flush=True)
    t=time.monotonic()
    command=["curl","-fLSs","--retry","6","--retry-all-errors","--retry-delay","3",
             "--connect-timeout","25","--max-time","3600","-C","-",
             "-o",str(temp),url]
    status=subprocess.run(command,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if status.returncode:
        raise RuntimeError("DOWNLOAD_FAILED "+rel+" "+status.stderr[-500:])
    if not check(temp,size,sha):
        raise RuntimeError("HASH_OR_SIZE_MISMATCH "+rel+" got_bytes="+str(temp.stat().st_size))
    os.replace(temp,dst)
    print("VERIFIED",rel,"bytes",size,"secs",round(time.monotonic()-t,1),flush=True)
    return True
def main():
    free=os.statvfs(ROOT)
    available=free.f_bavail*free.f_frsize
    required=sum(i[2] for i in FILES if not (ROOT/i[0]).exists())
    print("FREE_BYTES",available,"REQUIRED_BYTES",required,flush=True)
    if available-required<6_000_000_000:
        raise RuntimeError("At least 6GB headroom required to protect ComfyUI and output")
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run_one,item) for item in FILES]
        for future in as_completed(futures):future.result()
    print("WAN22_ASSETS_VERIFIED_ALL",flush=True)
if __name__=="__main__":main()
