#!/usr/bin/env bash
# Offline checks for SSH setup and non-systemd startup. No GPU or network needed.
set -Eeuo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/bin" "$TMP/run" "$TMP/home"

cat > "$TMP/bin/keygen" <<'MOCK'
#!/usr/bin/env bash
case "$1" in
  -l) [[ "$2" == '-f' ]] && grep -q '^ssh-ed25519 ' "$3" ;;
  -A) touch "$MOCK_HOST_KEYS" ;;
  *) exit 2 ;;
esac
MOCK
cat > "$TMP/bin/sshd" <<'MOCK'
#!/usr/bin/env bash
printf '%s\n' "$*" > "$MOCK_SSHD_ARGS"
MOCK
cat > "$TMP/start" <<'MOCK'
#!/usr/bin/env bash
touch "$MOCK_START_RAN"
MOCK
chmod +x "$TMP/bin/keygen" "$TMP/bin/sshd" "$TMP/start"
export MOCK_HOST_KEYS="$TMP/host-keys" MOCK_SSHD_ARGS="$TMP/sshd-args" MOCK_START_RAN="$TMP/start-ran"
export HACHE_SSH_KEYGEN_BIN="$TMP/bin/keygen" HACHE_SSHD_BIN="$TMP/bin/sshd"
export HACHE_CLORE_START_SCRIPT="$TMP/start" HACHE_SSH_HOME="$TMP/home"
export HACHE_CLORE_RUN_DIR="$TMP/run" HACHE_CLORE_LOG_FILE="$TMP/log/start.log"

if env -u SSH_KEY bash "$HERE/clore-entrypoint.sh" >"$TMP/no-key.log" 2>&1; then
  echo 'FAIL: missing SSH_KEY was accepted'; exit 1
fi
if SSH_KEY=$'ssh-ed25519 AAAA\ncommand=bad' bash "$HERE/clore-entrypoint.sh" >"$TMP/bad-key.log" 2>&1; then
  echo 'FAIL: multiline SSH_KEY was accepted'; exit 1
fi

SSH_KEY='ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZha2VwdWJsaWNrZXk= offline-test' \
  bash "$HERE/clore-entrypoint.sh"
grep -q '^ssh-ed25519 ' "$TMP/home/authorized_keys"
[[ "$(stat -c '%a' "$TMP/home")" == 700 ]]
[[ "$(stat -c '%a' "$TMP/home/authorized_keys")" == 600 ]]
for _ in {1..20}; do [[ -f "$MOCK_START_RAN" ]] && break; sleep 0.05; done
[[ -f "$MOCK_HOST_KEYS" && -f "$MOCK_START_RAN" ]]
grep -q -- '-t ' "$MOCK_SSHD_ARGS"
grep -q -- '-D -e ' "$MOCK_SSHD_ARGS"
grep -q 'PasswordAuthentication=no' "$MOCK_SSHD_ARGS"
echo 'PASS: key validation, permissions, host keys, foreground sshd, and app startup'
