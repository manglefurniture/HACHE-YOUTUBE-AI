# Clore ComfyUI startup helper — HACHE-YOUTUBE-AI

**Target:** the tested image yanwk/comfyui-boot:cu130-slim-v2 with Clore SSH auto-install entrypoint. This is a reproducible helper, **not yet tested as automatic startup on a new Clore rental**. No image rebuild, GPU rental, or production deployment is involved.

## Background

On 22 November 2026, Clore's order_entrypoint replaced the third-party image's normal startup. The original startup tried binding IPv6, which was unavailable. The validated manual fix was starting ComfyUI explicitly on IPv4 and using a private SSH tunnel.

The new script checks the NVIDIA GPU, copies the bundled ComfyUI to /root/ComfyUI only if missing, starts Python 3.13 on **127.0.0.1:8188**, waits for /system_stats HTTP success, and avoids duplicate processes. It writes logs to /root/.cache/hache-youtube-start/comfyui.log. It does NOT download models, expose 8188 publicly, install packages, change SSH, alter Lucía, or touch the Hache VPS.

## Manual one-command recovery in the rented container

Select image **yanwk/comfyui-boot:cu130-slim-v2**, preserve Clore's SSH auto-install entrypoint and existing SSH public key. Do not configure Clore HTTP public port forwarding for 8188.

Once SSH is available, run:

~~~bash
curl -fsSL --retry 3 https://raw.githubusercontent.com/manglefurniture/HACHE-YOUTUBE-AI/main/scripts/clore-comfyui-start.sh -o /root/hache-clore-start.sh
bash /root/hache-clore-start.sh
~~~

From laptop Hache, using the assigned host and SSH port from **My Orders**, access ComfyUI through:

~~~powershell
ssh -N -T -L 127.0.0.1:18188:127.0.0.1:8188 -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes -p <PUERTO_EXTERNO> root@<HOST_DE_MY_ORDERS>
~~~

Open http://127.0.0.1:18188/ on that laptop. The public Clore proxy may still show 403 or 502; validate the private API first.

Only after startup, use the existing verified model provisioner to load the selected model; this startup script intentionally does **not** download all nine models.

## Future unattended startup via Clore order template

Clore documents a post-start **command** field as well as **autossh_entrypoint**, which executes /root/onstart.sh if that file exists. A newly rented container **will not already contain** our GitHub script. Whether the selected UI mode accepts a startup command that fetches this script while retaining SSH auto-install **must be verified in a real Clore rental**. Do not disable the proven SSH entrypoint to make ComfyUI start. Until validated, the SSH command above is the supported recovery path.

For unattended startup, pin the raw script URL to a reviewed Git **commit SHA** instead of tracking an evolving main branch. Never put credentials or personal assets into the URL, order command, logs, or GitHub.

## Failure handling / rollback

- Missing GPU: verify nvidia-smi -L and Clore GPU pass-through.
- Missing bundle: verify /default-comfyui-bundle/ComfyUI/main.py and exact Docker tag.
- Port occupied but API unhealthy: inspect the process and port; **do not start duplicate ComfyUI**.
- Health check failure: inspect /root/.cache/hache-youtube-start/comfyui.log and /system_stats.
- Re-run is safe if the service is already healthy. No active generation jobs are intentionally stopped.
- Roll back by simply not using the helper on the next rental. Docker image and existing R2 models remain unchanged.

## Offline tests

~~~bash
bash -n scripts/clore-comfyui-start.sh scripts/test_clore_comfyui_start.sh
bash scripts/test_clore_comfyui_start.sh
~~~

Tests mock the GPU, the health endpoint, the bundled files, and the Python process. They do not validate real Clore startup or inference.
