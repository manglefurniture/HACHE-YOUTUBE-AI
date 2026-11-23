#!/usr/bin/env bash
# Offline smoke tests for Clore bootstrap. No GPU, network, or download required.
set -Eeuo pipefail
HERE="$(cd -- "$(dirname -- "\${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
cleanup() { if [[ -f "$TMP/run/comfyui.pid" ]]; then kill "$(cat "$TMP/run/comfyui.pid")" 2>/dev/null || true; fi; rm -rf "$TMP"; }
trap cleanup EXIT
mkdir -p "$TMP/bin" "$TMP/bundle" "$TMP/run"
printf 'print("mock")\n' > "$TMP/bundle/main.py"
cat > "$TMP/bin/nvidia-smi" <<'MOCK'
#!/usr/bin/env bash
exit 0
MOCK
cat > "$TMP/bin/curl" <<'MOCK'
#!/usr/bin/env bash
[[ -f "\${MOCK_READY}" ]]
MOCK
cat > "$TMP/bin/fake-python" <<'MOCK'
#!/usr/bin/env bash
if [[ "$1" == '-c' ]]; then
  exit 1 # port not occupied
fi
printf '%s\n' started >> "$MOCK_LAUNCHES"
touch "$MOCK_READY"
exec sleep 90
MOCK
chmod +x "$TMP/bin/"*
export PATH="$TMP/bin:$PATH"
export HACHE_COMFY_DIR="$TMP/comfy" HACHE_COMFY_BUNDLE_DIR="$TMP/bundle"
export HACHE_COMFY_RUNTIME_DIR="$TMP/run" HACHE_COMFY_PYTHON="$TMP/bin/fake-python"
export HACHE_COMFY_PORT=18189 HACHE_COMFY_TIMEOUT=3
export MOCK_LAUNCHES="$TMP/launches" MOCK_READY="$TMP/ready"

# Fail safely with missing ComfyUI bundle; no process is started.
rm -f "$TMP/bundle/main.py"
if bash "$HERE/clore-comfyui-start.sh" > "$TMP/no-bundle.log" 2>&1; then echo 'FAIL: missing bundle was accepted'; exit 1; fi
[[ ! -e "$MOCK_LAUNCHES" ]] || { echo 'FAIL: unexpected launch'; exit 1; }
printf 'print("mock")\n' > "$TMP/bundle/main.py"

bash "$HERE/clore-comfyui-start.sh" | grep -q 'COMFYUI_READY'
[[ -f "$TMP/comfy/main.py" ]] || { echo 'FAIL: bundle was not copied'; exit 1; }
[[ "$(wc -l < "$MOCK_LAUNCHES")" -eq 1 ]] || { echo 'FAIL: wrong launch count'; exit 1; }

# Healthy app is idempotent. Do not spawn twice or overwrite models.
bash "$HERE/clore-comfyui-start.sh" | grep -q 'COMFYUI_READY existing'
[[ "$(wc -l < "$MOCK_LAUNCHES")" -eq 1 ]] || { echo 'FAIL: duplicate launch'; exit 1; }

# GPU check fails closed.
cat > "$TMP/bin/nvidia-smi" <<'MOCK'
#!/usr/bin/env bash
exit 1
MOCK
chmod +x "$TMP/bin/nvidia-smi"
if bash "$HERE/clore-comfyui-start.sh" > "$TMP/no-gpu.log" 2>&1; then echo 'FAIL: missing GPU was accepted'; exit 1; fi

echo 'PASS: missing bundle, successful boot, idempotency, and GPU failure'
