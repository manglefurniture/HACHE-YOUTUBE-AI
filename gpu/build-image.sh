#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."
IMAGE="${1:-hache-youtube-ai-gpu:local}"
docker build -f gpu/Dockerfile -t "$IMAGE" .
