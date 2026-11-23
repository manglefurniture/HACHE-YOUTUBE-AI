#!/usr/bin/env bash
# No GPU, SSH, network access, or models required.
set -Eeuo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/bin" "$TMP/comfy" "$TMP/run"
printf 'print("mock")\n' > "$TMP/comfy/main.py"
cat > "$TMP/bin/nvidia-smi" <<'SH'
#!/usr/bin/env bash
[[ ! -f "$MOCK_NO_GPU" ]]
SH
cat > "$TMP/bin/python" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$MOCK_PYTHON_ARGS"
printf '%s\n' "${AWS_ACCESS_KEY_ID:-}" > "$MOCK_AWS_ENV"
SH
chmod +x "$TMP/bin/"*
export PATH="$TMP/bin:$PATH"
export MOCK_PYTHON_ARGS="$TMP/args" MOCK_AWS_ENV="$TMP/aws"
export MOCK_NO_GPU="$TMP/no-gpu"
export HACHE_COMFY_PYTHON="$TMP/bin/python"
export HACHE_COMFY_DIR="$TMP/comfy"
export HACHE_COMFY_WORKSPACE="$TMP/workspace"
export HACHE_MODELS_DIR="$TMP/models"
export HACHE_COMFY_CONFIG_DIR="$TMP/run"
export AWS_ACCESS_KEY_ID='must-not-leak'

bash "$HERE/clore-ubuntu-onstart.sh" | grep -q HACHE_COMFYUI_START
grep -Fxq -- '--listen' "$TMP/args"
grep -Fxq -- '127.0.0.1' "$TMP/args"
grep -Fxq -- '--enable-manager' "$TMP/args"
grep -Fxq -- '--extra-model-paths-config' "$TMP/args"
grep -Fxq -- '--input-directory' "$TMP/args"
grep -Fxq -- '--output-directory' "$TMP/args"
[[ -s "$TMP/run/extra-model-paths.yaml" ]]
[[ -d "$TMP/workspace/output" && -d "$TMP/models" ]]
[[ "$(cat "$TMP/aws")" == "" ]] || { echo 'FAIL: credential leaked to ComfyUI'; exit 1; }

rm -f "$TMP/args"
touch "$TMP/no-gpu"
if bash "$HERE/clore-ubuntu-onstart.sh" > "$TMP/no-gpu.log" 2>&1; then
  echo 'FAIL: missing GPU accepted'; exit 1
fi
[[ ! -e "$TMP/args" ]] || { echo 'FAIL: launched without GPU'; exit 1; }

rm -f "$TMP/no-gpu" "$TMP/comfy/main.py"
if bash "$HERE/clore-ubuntu-onstart.sh" > "$TMP/no-comfy.log" 2>&1; then
  echo 'FAIL: missing ComfyUI accepted'; exit 1
fi
[[ ! -e "$TMP/args" ]] || { echo 'FAIL: launched without main.py'; exit 1; }

echo 'PASS: Clore onstart, local binding, model paths, credential isolation, and fail-closed checks'
