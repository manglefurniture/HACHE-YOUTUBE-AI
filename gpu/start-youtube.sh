#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=/opt/ComfyUI
BASE="${HACHE_MODELS_DIR:-/workspace/models}"
if [[ ! -f "$ROOT/main.py" ]]; then
  echo "ERROR: ComfyUI main.py missing: $ROOT/main.py" >&2
  exit 1
fi
if [[ ! -d "$BASE" ]]; then
  echo "ERROR: model mount missing: $BASE (provision models before starting)" >&2
  exit 1
fi
if [[ ! -r "$BASE" ]]; then
  echo "ERROR: model mount unreadable: $BASE" >&2
  exit 1
fi
if ! command -v nvidia-smi >/dev/null 2>&1 || ! nvidia-smi -L >/dev/null 2>&1; then
  echo "ERROR: NVIDIA GPU is unavailable; refusing to download the model set" >&2
  exit 1
fi
python /opt/hache-youtube/bin/provision_models.py
python /opt/hache-youtube/bin/verify-shared-models.py --models-dir "$BASE" --hash
# Credentials are needed only by the provisioner; ComfyUI and custom nodes never inherit them.
unset R2_ACCOUNT_ID AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
INPUT=/workspace/hache-youtube/input
OUTPUT=/workspace/hache-youtube/output
WORKFLOWS=/workspace/hache-youtube/workflows
mkdir -p "$INPUT" "$OUTPUT" "$WORKFLOWS"
cat > /tmp/hache-youtube-extra-model-paths.yaml <<YAML
hache_youtube:
  base_path: $BASE
  checkpoints: checkpoints
  clip_vision: clip_vision
  ipadapter: ipadapter
  loras: loras
  diffusion_models: diffusion_models
  text_encoders: text_encoders
  vae: vae
  ultralytics: ultralytics
YAML
# Bind loopback only: use an authenticated tunnel/proxy to access ComfyUI remotely.
exec python "$ROOT/main.py" --listen 127.0.0.1 --port 8188 --disable-auto-launch --extra-model-paths-config /tmp/hache-youtube-extra-model-paths.yaml --input-directory "$INPUT" --output-directory "$OUTPUT"
