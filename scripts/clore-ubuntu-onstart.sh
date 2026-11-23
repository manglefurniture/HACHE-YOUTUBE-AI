#!/usr/bin/env bash
# Executed as /root/onstart.sh by Clore's autossh/S6 service.
# SSH lifecycle and public key are managed by Clore, exactly as with PRL mining.
# Also usable as a direct Docker entrypoint for local GPU smoke tests.
set -Eeuo pipefail
umask 077

PYTHON_BIN="${HACHE_COMFY_PYTHON:-/opt/hache-venv/bin/python}"
COMFY_DIR="${HACHE_COMFY_DIR:-/opt/ComfyUI}"
WORKSPACE="${HACHE_COMFY_WORKSPACE:-/workspace/hache-youtube}"
MODELS="${HACHE_MODELS_DIR:-/workspace/models}"
CONFIG_DIR="${HACHE_COMFY_CONFIG_DIR:-/run/hache-youtube}"
PORT="${HACHE_COMFY_PORT:-8188}"

[[ "$PORT" =~ ^[0-9]+$ ]] && (( PORT >= 1024 && PORT <= 65535 )) || {
  echo 'ERROR: invalid ComfyUI port' >&2; exit 2;
}
[[ -f "$COMFY_DIR/main.py" ]] || { echo 'ERROR: ComfyUI main.py missing' >&2; exit 1; }
[[ -x "$PYTHON_BIN" ]] || { echo 'ERROR: ComfyUI Python runtime missing' >&2; exit 1; }
command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1 || {
  echo 'ERROR: NVIDIA GPU unavailable; refusing to start ComfyUI' >&2; exit 1;
}

mkdir -p "$WORKSPACE/input" "$WORKSPACE/output" "$WORKSPACE/workflows" "$MODELS" "$CONFIG_DIR"
chmod 0700 "$CONFIG_DIR"
cat > "$CONFIG_DIR/extra-model-paths.yaml" <<YAML
hache_youtube:
  base_path: "$MODELS"
  checkpoints: checkpoints
  clip_vision: clip_vision
  ipadapter: ipadapter
  loras: loras
  diffusion_models: diffusion_models
  text_encoders: text_encoders
  vae: vae
  ultralytics: ultralytics
YAML

# Cloud credentials are only for provisioning models through separate audited
# commands; they are never inherited by the ComfyUI web process.
unset R2_ACCOUNT_ID AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

echo "HACHE_COMFYUI_START 127.0.0.1:$PORT (SSH managed separately by Clore)"
exec "$PYTHON_BIN" "$COMFY_DIR/main.py" \
  --listen 127.0.0.1 --port "$PORT" \
  --disable-auto-launch --enable-manager \
  --extra-model-paths-config "$CONFIG_DIR/extra-model-paths.yaml" \
  --input-directory "$WORKSPACE/input" --output-directory "$WORKSPACE/output"
