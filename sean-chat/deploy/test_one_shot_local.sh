#!/usr/bin/env bash
set -euo pipefail

BASE_DIR=$(pwd)
VENV_DIR=$BASE_DIR/.venv_test
CERT_DIR=$BASE_DIR/test_certs
PORT=8765

echo "[test] Base dir: $BASE_DIR"

if [ -d "$VENV_DIR" ]; then
  echo "[test] Removing existing venv at $VENV_DIR"
  rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
# shellcheck source=/dev/null
. "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install cryptography websockets

mkdir -p "$CERT_DIR"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -subj "/CN=localhost" \
  -keyout "$CERT_DIR/key.pem" -out "$CERT_DIR/cert.pem"

LOG=$BASE_DIR/test_server.log
rm -f "$LOG" alice_out.txt bob_out.txt

echo "[test] Starting server (background)..."
nohup "$VENV_DIR/bin/python" "$BASE_DIR/server.py" --host 127.0.0.1 --port $PORT --certfile "$CERT_DIR/cert.pem" --keyfile "$CERT_DIR/key.pem" > "$LOG" 2>&1 &
SERVER_PID=$!
echo "[test] Server PID: $SERVER_PID"
sleep 1

echo "[test] Running healthcheck (https)..."
./deploy/healthcheck.sh 127.0.0.1 $PORT https || true

echo "[test] Running alice client to send message..."
printf "add_contact bob
chat bob
Hello Bob from Alice (test)
exit
exit
" | "$VENV_DIR/bin/python" "$BASE_DIR/main.py" --name alice --connect --server-host 127.0.0.1 --server-port $PORT --server-wss --insecure > alice_out.txt 2>&1 &
ALICE_PID=$!

sleep 1

echo "[test] Running bob client to receive..."
printf "add_contact alice
list_contacts
chat alice
exit
exit
" | "$VENV_DIR/bin/python" "$BASE_DIR/main.py" --name bob --connect --server-host 127.0.0.1 --server-port $PORT --server-wss --insecure > bob_out.txt 2>&1 &
BOB_PID=$!

# Wait for clients
wait $ALICE_PID || true
wait $BOB_PID || true

sleep 1

echo "---- SERVER LOG ----"
tail -n 200 "$LOG" || true

echo "---- ALICE OUT ----"
cat alice_out.txt || true

echo "---- BOB OUT ----"
cat bob_out.txt || true

# Cleanup
kill "$SERVER_PID" || true
rm -rf "$VENV_DIR" "$CERT_DIR"

echo "[test] Finished"
