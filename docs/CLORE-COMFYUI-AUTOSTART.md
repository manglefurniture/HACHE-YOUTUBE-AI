# Clore ComfyUI startup and SSH

**Base:** `yanwk/comfyui-boot:cu130-slim-v2`. For a new rental use the derived image `ghcr.io/manglefurniture/hache-clore-comfyui:latest` after GitHub Actions publishes it. This image bakes in `openssh-server`; configure Clore SSH auto-install off and provide the public key as `SSH_KEY`. A real rental is still required to verify provider integration.

## Diagnosis: order #2482135

Clore showed order #2482135 as Active/Deployed with public TCP 1317 forwarded to container TCP 22. The attached Rocky Linux 10 log shows a completed 453-package update, then starts installing `openssh-server`. Its last relevant line creates the systemd service symlink; it never shows `sshd` starting. The container log warns that systemd is not PID 1, so relying on systemd service activation is incompatible with this container. The reported timeout/connection close occurs before an SSH banner, so public-key authentication is never reached. The captured log does not prove the single immediate failure: it may be a truncated/aborted Clore install flow or `sshd` not being launched after package installation.

Clore documents `autossh_entrypoint` as installing SSH and executing `/root/onstart.sh`. For the log's Rocky image, that path performed the broad runtime update. The derived image instead installs just `openssh-server` at image build time, validates Clore's public `SSH_KEY`, writes `/root/.ssh/authorized_keys` with restrictive permissions, generates per-rental host keys, then runs `sshd -D` directly as the container's main process. It does not use systemd or update packages at rental startup. ComfyUI starts asynchronously via the existing startup helper, so SSH remains available for diagnosis if ComfyUI fails.

## Configure each new rental

1. Select `ghcr.io/manglefurniture/hache-clore-comfyui:latest`. For repeatable deployment, prefer `:sha-<commit>` from a successful image workflow run.
2. Forward container port `22` as public `TCP`. Do not publish ComfyUI's `8188`; it listens only on loopback.
3. In Clore's SSH settings select your existing public SSH key, and confirm it is supplied inside the container as `SSH_KEY`. Clore's renter troubleshooting guide documents `SSH_KEY` as the public-key environment variable. Pass one public-key line only; never use a private key.
4. Turn **SSH auto-install / autossh_entrypoint off**. Do not set a startup command that replaces the image entrypoint.
5. Wait for Active/Deployed and connect using the host and forwarded port in My Orders:

~~~powershell
ssh -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -p <PUERTO_EXTERNO> root@<HOST_DE_MY_ORDERS>
~~~

6. After login, inspect ComfyUI startup and verify its local API:

~~~bash
tail -n 80 /var/log/hache-clore-comfyui-start.log
curl --noproxy '*' -fsS http://127.0.0.1:8188/system_stats
~~~

7. To use the UI, create a private tunnel from the laptop and open `http://127.0.0.1:18188/`:

~~~powershell
ssh -N -T -L 127.0.0.1:18188:127.0.0.1:8188 -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes -p <PUERTO_EXTERNO> root@<HOST_DE_MY_ORDERS>
~~~

## Failure handling

- SSH key missing/invalid: check that `SSH_KEY` contains one valid public key line and that Clore auto-install is off. The container emits a short startup error.
- SSH timeout: recheck the host and mapped TCP port 22 in My Orders. This image runs sshd directly and does not require systemd.
- ComfyUI health failure: inspect `/var/log/hache-clore-comfyui-start.log` and `/root/.cache/hache-youtube-start/comfyui.log`.
- Port occupied but API unhealthy: inspect the process; do not start a duplicate ComfyUI process.
- Missing GPU or bundle: check `nvidia-smi -L` and `/default-comfyui-bundle/ComfyUI/main.py`.

## Verification and limits

Run the offline checks:

~~~bash
bash -n scripts/clore-comfyui-start.sh scripts/test_clore_comfyui_start.sh
bash scripts/test_clore_comfyui_start.sh
bash -n scripts/clore-entrypoint.sh scripts/test_clore_entrypoint.sh
bash scripts/test_clore_entrypoint.sh
~~~

Tests mock SSH, the GPU, HTTP health, image bundle, and Python process. Pull requests build the image without publishing it; pushes to `main` publish `sha-<commit>` and `latest`. Offline tests and image builds cannot verify Clore's environment-variable injection, forwarded port, real SSH handshake, or GPU inference. Claim provider verification only after a separately authorized rental confirms it. This repository change does not modify the current Clore rental or the production VPS.

Clore references: [create_order API](https://docs.clore.ai/for-hosts/api) (`autossh_entrypoint`, `ssh_key`, `command`) and [renter troubleshooting](https://docs.clore.ai/guides/getting-started/clore-troubleshooting) (`SSH_KEY`).
