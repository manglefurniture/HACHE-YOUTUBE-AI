# Clore ComfyUI — Ubuntu 24.04 with provider-managed SSH

**Status:** GitHub build/CI first; a paid Clore GPU rental is required to verify live
SSH port forwarding, injected public key, NVIDIA GPU and image inference.
Do not claim production success until that rental has been tested.

## Why this variant exists

The Clore PRL miner image `prl-miner-container/Dockerfile.clore` uses
`nvidia/cuda:12.8.2-base-ubuntu24.04`, Clore's **SSH auto-install** and
`/root/onstart.sh`. A real PRL rental (#2352606) authenticated over SSH and
mined with four RTX 5090 GPUs. This proves that *configuration worked on that
rental*, not that every Clore host/gateway is accessible.

Our earlier ComfyUI image based on `yanwk/comfyui-boot:cu130-slim-v2`
uses Rocky Linux 10. On order #2482135, the provider's auto-installer
upgraded hundreds of packages before installing OpenSSH. A subsequent
standalone SSH image (PR #28) disabled Clore auto-install and expected
a manually supplied `SSH_KEY`. Neither image established real SSH on the
sampled gateway `49.12.8.39`. This does NOT prove an image root cause:
host port mapping, provider network and early container exits remain possible.

**This is a separate, reversible image variant:** Ubuntu 24.04, CUDA 13.0.2,
PyTorch 2.13.0 CUDA 13.0 wheels, and a pinned upstream ComfyUI revision.
Its only startup job is to run ComfyUI in the foreground through
`/root/onstart.sh`. Clore's S6 autossh service owns `sshd`, public-key
injection and SSH lifecycle, mirroring the proven PRL mechanism.
No package or model downloads happen when the rental starts.

## How to rent

1. Select the successful workflow-published image:
   `ghcr.io/manglefurniture/hache-clore-comfyui-ubuntu:sha-<MERGE_COMMIT>`.
   For exploratory use, `:latest` is supported; a commit tag is repeatable.
2. **Enable SSH auto-install entrypoint** (unlike PR #28's Rocky derivative).
3. Choose the existing public key **clore-prl-hache** in Clore's SSH key selector.
   Do NOT enter the private key anywhere in Clore. No manual `SSH_KEY`
   variable is required with this mode.
4. Forward **container port 22 as TCP**. Do not expose port 8188.
5. Leave **startup command blank**. Do not replace `/root/onstart.sh`.
   Models are downloaded separately after SSH succeeds; no R2 secrets in
   order screenshots or public scripts.
6. On My Orders, confirm Active/Deployed, the *actual mapped external SSH
   port and host* (do not reuse the port of a previous rental).
7. Connect from Windows PowerShell on laptop Hache:

~~~powershell
ssh -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -p <EXTERNAL_PORT> root@<HOST_FROM_CLORE>
~~~

8. Inspect GPU and ComfyUI:

~~~bash
nvidia-smi -L
curl --noproxy '*' -fsS http://127.0.0.1:8188/system_stats
ps aux | grep '[C]omfyUI/main.py'
~~~

9. When SSH works, start a private tunnel from the laptop and open
   `http://127.0.0.1:18188/`:

~~~powershell
ssh -N -T -L 127.0.0.1:18188:127.0.0.1:8188 -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -p <EXTERNAL_PORT> root@<HOST_FROM_CLORE>
~~~

## What is and is not bundled

- Included: Ubuntu 24.04, pinned CUDA/PyTorch, official ComfyUI, embedded
  Manager option, FFmpeg, Python venv, R2 provisioner CLI dependencies,
  `/root/onstart.sh` and private loopback binding.
- Excluded: private LoRA, photos, model weights and R2 credentials. The
  startup creates `/workspace/models` and `/workspace/hache-youtube`
  but downloads nothing. Provision the needed model(s) from R2 only after
  live SSH, CUDA and API health have been verified.
- Manager is available, but avoid unattended installs of arbitrary nodes.

## Failure diagnosis before any additional paid rental

- TCP timeout *before the SSH banner*: compare actual Clore host, forwarded
  22/TCP port and alternative source network. SSH key has not been tested.
- SSH prompt or `Permission denied (publickey)`: then compare the selected
  public key against the laptop's private key fingerprint.
- SSH OK / ComfyUI unavailable: provider auto-installer may have started SSH
  while `/root/onstart.sh` failed. Inspect container logs and `nvidia-smi`.
- Failures even with Ubuntu image do not prove or disprove a Clore gateway
  problem; collect host/port, deployment logs, SSH debug output, and compare
  against a known working host.

## Sources and safety

- Proven miner baseline: `manglefurniture/prl-miner-container/Dockerfile.clore`
  and `clore/README.md`.
- Upstream pinned ComfyUI commit: `720e923631e685e9cb28b9e2cc7b43f82b44033f`.
- Image Dockerfile: `clore/ubuntu.Dockerfile`.
- Offline checks: `bash scripts/test_clore_ubuntu_onstart.sh`, plus the
  independent Docker build in CI.
- The GitHub PR cannot validate Clore public-key injection or live GPU use.
- Production VPS, existing Rocky image and PRL miner are untouched.
