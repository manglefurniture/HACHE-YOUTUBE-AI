#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=/opt/ComfyUI
BASE=/workspace/models
INPUT=/workspace/hache-youtube/input
OUTPUT=/workspace/hache-youtube/output
WORKFLOWS=/workspace/hache-youtube/workflows
mkdir -p "$INPUT" "$OUTPUT" "$WORKFLOWS"
cat > /tmp/hache-youtube-extra-model-paths.yaml <<'YAML'
hache_youtube:
  base_path: /workspace/models
  checkpoints: checkpoints
  loras: loras
  diffusion_models: diffusion_models
  text_encoders: text_encoders
  vae: vae
YAML
# Bind loopback only: use an authenticated tunnel/proxy to access ComfyUI remotely.
exec python "$ROOT/main.py" --listen 127.0.0.1 --port 8188 --disable-auto-launch --extra-model-paths-config /tmp/hache-youtube-extra-model-paths.yaml --input-directory "$INPUT" --output-directory "$OUTPUT"
