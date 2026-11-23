#!/usr/bin/env bash
# Clore image entrypoint: install no packages at runtime and do not use systemd.
set -Eeuo pipefail
umask 077

SSH_KEYGEN_BIN="${HACHE_SSH_KEYGEN_BIN:-ssh-keygen}"
SSHD_BIN="${HACHE_SSHD_BIN:-/usr/sbin/sshd}"
START_SCRIPT="${HACHE_CLORE_START_SCRIPT:-/usr/local/bin/hache-clore-comfyui-start.sh}"
SSH_HOME="${HACHE_SSH_HOME:-/root/.ssh}"
RUN_DIR="${HACHE_CLORE_RUN_DIR:-/run/sshd}"
LOG_FILE="${HACHE_CLORE_LOG_FILE:-/var/log/hache-clore-comfyui-start.log}"

if [[ -z "${SSH_KEY:-}" ]]; then
  echo 'ERROR: Clore must provide the public key in SSH_KEY' >&2
  exit 2
fi
if [[ "$SSH_KEY" == *$'\n'* || "$SSH_KEY" == *$'\r'* \
  || ! "$SSH_KEY" =~ ^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp[0-9]+)[[:space:]]+[A-Za-z0-9+/=]+([[:space:]][[:print:]]*)?$ ]]; then
  echo 'ERROR: SSH_KEY must contain one supported OpenSSH public key on one line' >&2
  exit 2
fi
command -v "$SSH_KEYGEN_BIN" >/dev/null 2>&1 || { echo 'ERROR: ssh-keygen is missing' >&2; exit 1; }
[[ -x "$SSHD_BIN" ]] || { echo 'ERROR: sshd is missing or not executable' >&2; exit 1; }
[[ -f "$START_SCRIPT" ]] || { echo 'ERROR: ComfyUI startup helper is missing' >&2; exit 1; }

mkdir -p "$SSH_HOME" "$RUN_DIR" "$(dirname -- "$LOG_FILE")"
chmod 0700 "$SSH_HOME"
key_tmp="$SSH_HOME/.authorized_keys.$$"
trap 'rm -f -- "$key_tmp"' EXIT
printf '%s\n' "$SSH_KEY" > "$key_tmp"
"$SSH_KEYGEN_BIN" -l -f "$key_tmp" >/dev/null || { echo 'ERROR: SSH_KEY is not a valid OpenSSH public key' >&2; exit 2; }
install -m 0600 "$key_tmp" "$SSH_HOME/authorized_keys"
rm -f -- "$key_tmp"
trap - EXIT
unset SSH_KEY

# Generate host keys inside this rental. Do not invoke systemctl: this image
# runs a container process, not systemd as PID 1.
"$SSH_KEYGEN_BIN" -A
"$SSHD_BIN" -t -o PermitRootLogin=prohibit-password -o PubkeyAuthentication=yes \
  -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
  -o AuthorizedKeysFile="$SSH_HOME/authorized_keys" -o UsePAM=no

# Bring up ComfyUI in the background so SSH is available immediately, including
# when the app needs diagnosis. The helper is idempotent and logs its outcome.
bash "$START_SCRIPT" >>"$LOG_FILE" 2>&1 &

exec "$SSHD_BIN" -D -e -o PermitRootLogin=prohibit-password -o PubkeyAuthentication=yes \
  -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
  -o AuthorizedKeysFile="$SSH_HOME/authorized_keys" -o UsePAM=no
