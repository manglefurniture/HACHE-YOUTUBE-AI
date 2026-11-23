#!/usr/bin/env bash
# Start the known-good YanWenKun ComfyUI image under Clore's SSH entrypoint.
# Does not expose the UI, download models, alter SSH, or modify Hache production.
set -Eeuo pipefail

COMFY_DIR="\${HACHE_COMFY_DIR:-/root/ComfyUI}"
BUNDLE_DIR="\${HACHE_COMFY_BUNDLE_DIR:-/default-comfyui-bundle/ComfyUI}"
RUNTIME_DIR="\${HACHE_COMFY_RUNTIME_DIR:-/root/.cache/hache-youtube-start}"
PYTHON_BIN="\${HACHE_COMFY_PYTHON:-python3.13}"
PORT="\${HACHE_COMFY_PORT:-8188}"
TIMEOUT="\${HACHE_COMFY_TIMEOUT:-120}"

if [[ ! "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1024 || PORT > 65535 )); then
  echo 'ERROR: invalid ComfyUI port' >&2; exit 2
fi
if [[ ! "$TIMEOUT" =~ ^[0-9]+$ ]] || (( TIMEOUT < 1 || TIMEOUT > 600 )); then
  echo 'ERROR: invalid startup timeout' >&2; exit 2
fi
for cmd in curl flock nvidia-smi "$PYTHON_BIN"; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: missing executable: $cmd" >&2; exit 1; }
done
nvidia-smi -L >/dev/null 2>&1 || { echo 'ERROR: NVIDIA GPU unavailable' >&2; exit 1; }

mkdir -p "$RUNTIME_DIR"
LOG="$RUNTIME_DIR/comfyui.log"
PID_FILE="$RUNTIME_DIR/comfyui.pid"
API="http://127.0.0.1:\${PORT}/system_stats"

# Avoid simultaneous invocations on the same rental.
exec 9>"$RUNTIME_DIR/start.lock"
flock -n 9 || { echo 'ERROR: another startup is in progress' >&2; exit 1; }

healthy() { curl --noproxy '*' --fail --silent --show-error --max-time 3 --output /dev/null "$API" 2>/dev/null; }

if healthy; then
  echo "COMFYUI_READY existing $API"; exit 0
fi

# A previous start of this script may still be initializing the application.
if [[ -f "$PID_FILE" ]]; then
  old_pid="$(cat "$PID_FILE")"
  if [[ "$old_pid" =~ ^[0-9]+$ ]] && kill -0 "$old_pid" 2>/dev/null \
    && ps -p "$old_pid" -o args= 2>/dev/null | grep -F -- "$COMFY_DIR/main.py" >/dev/null; then
    echo "COMFYUI_STARTING existing-pid=$old_pid"
    pid="$old_pid"
  else
    rm -f "$PID_FILE"
    pid=''
  fi
else
  pid=''
fi

if [[ -z "$pid" ]]; then
  # A service may already occupy this port; never launch a second process.
  if "$PYTHON_BIN" -c 'import socket,sys; s=socket.socket(); s.settimeout(1); code=s.connect_ex(("127.0.0.1",int(sys.argv[1]))); s.close(); sys.exit(0 if code==0 else 1)' "$PORT"; then
    echo "ERROR: port $PORT occupied, but ComfyUI health check failed; inspect existing process" >&2
    exit 1
  fi
  if [[ ! -f "$COMFY_DIR/main.py" ]]; then
    [[ -f "$BUNDLE_DIR/main.py" ]] || { echo 'ERROR: ComfyUI missing from image bundle' >&2; exit 1; }
    mkdir -p "$COMFY_DIR"
    cp -a -n "$BUNDLE_DIR/." "$COMFY_DIR/"
    [[ -f "$COMFY_DIR/main.py" ]] || { echo 'ERROR: failed to initialize ComfyUI' >&2; exit 1; }
  fi
  export PYTHONPYCACHEPREFIX="\${PYTHONPYCACHEPREFIX:-/root/.cache/pycache}"
  export PIP_USER=true PIP_ROOT_USER_ACTION=ignore
  export PATH="$PATH:/root/.local/bin"
  echo "COMFYUI_LAUNCH 127.0.0.1:$PORT log=$LOG"
  # Close the lock FD in the child; Clore's SSH entrypoint remains PID 1.
  nohup "$PYTHON_BIN" "$COMFY_DIR/main.py" --listen 127.0.0.1 --port "$PORT" --enable-manager \
    >"$LOG" 2>&1 < /dev/null 9>&- &
  pid=$!
  printf '%s\n' "$pid" > "$PID_FILE"
fi

for (( elapsed=0; elapsed<TIMEOUT; elapsed++ )); do
  if healthy; then
    echo "COMFYUI_READY $API pid=$pid"
    exit 0
  fi
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "ERROR: ComfyUI process exited before health check; see $LOG" >&2
    [[ -f "$LOG" ]] && tail -n 30 "$LOG" >&2
    exit 1
  fi
  sleep 1
done
echo "ERROR: ComfyUI did not become healthy within \${TIMEOUT}s; log=$LOG" >&2
[[ -f "$LOG" ]] && tail -n 30 "$LOG" >&2
exit 1
