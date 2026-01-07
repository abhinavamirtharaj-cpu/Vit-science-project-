#!/usr/bin/env bash
# One-shot SEAN relay server deploy (Ubuntu 22.04/24.04)
# Usage (as root): sudo bash deploy/one_shot_deploy.sh [selfsigned|letsencrypt] [domain-for-letsencrypt]
set -euo pipefail
CERT_TYPE="${1:-selfsigned}"
DOMAIN="${2:-}"
REPO_URL="${REPO_URL:-https://github.com/abhinavamirtharaj-cpu/Vit-science-project-.git}"
SERVER_DIR="/opt/sean"
WORK_DIR="$SERVER_DIR/sean-chat"
VENV_DIR="$SERVER_DIR/.venv"
SEAN_USER="sean"
CERT_DIR="$SERVER_DIR/certs"
CERT_PEM="$CERT_DIR/sean_cert.pem"
KEY_PEM="$CERT_DIR/sean_key.pem"
SERVICE_PATH="/etc/systemd/system/sean-server.service"
PORT=8765

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root: sudo $0"
  exit 1
fi

echo "[1/9] Installing system packages..."
apt update
apt install -y python3-venv python3-pip git openssl curl ufw || true

echo "[2/9] Creating server dir and cloning repo..."
mkdir -p "$SERVER_DIR"
chown "$SUDO_USER":"$SUDO_USER" "$SERVER_DIR" || true
if [ -d "$SERVER_DIR/.git" ]; then
  git -C "$SERVER_DIR" pull || true
else
  git clone "$REPO_URL" "$SERVER_DIR"
fi

echo "[3/9] Creating venv and installing Python deps..."
python3 -m venv "$VENV_DIR"
# shellcheck source=/dev/null
. "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install cryptography websockets

echo "[4/9] Generating certificates ($CERT_TYPE)..."
mkdir -p "$CERT_DIR"
if [ "$CERT_TYPE" = "selfsigned" ]; then
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -subj "/CN=${DOMAIN:-localhost}" \
    -keyout "$KEY_PEM" -out "$CERT_PEM"
  echo "Self-signed certs created at $CERT_DIR"
else
  if [ -z "$DOMAIN" ]; then
    echo "Let’s Encrypt selected but no domain provided. Usage: $0 letsencrypt example.com"
    exit 1
  fi
  apt install -y snapd
  snap install core; snap refresh core
  snap install --classic certbot
  certbot certonly --standalone -d "$DOMAIN" --noninteractive --agree-tos -m "admin@$DOMAIN"
  if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    echo "Certbot failed to obtain certs for $DOMAIN"
    exit 1
  fi
  ln -sf "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" "$CERT_PEM"
  ln -sf "/etc/letsencrypt/live/$DOMAIN/privkey.pem" "$KEY_PEM"
  echo "Let's Encrypt certs linked to $CERT_DIR"
fi

echo "[5/9] Creating system user and setting permissions..."
id -u "$SEAN_USER" >/dev/null 2>&1 || useradd --system --no-create-home --shell /usr/sbin/nologin "$SEAN_USER"
chown -R "$SEAN_USER":"$SEAN_USER" "$SERVER_DIR"

echo "[6/9] Installing systemd service..."
cat > "$SERVICE_PATH" <<SERVICE
[Unit]
Description=SEAN relay server
After=network.target

[Service]
User=$SEAN_USER
WorkingDirectory=$WORK_DIR
ExecStart=$VENV_DIR/bin/python $WORK_DIR/server.py --host 0.0.0.0 --port $PORT --certfile $CERT_PEM --keyfile $KEY_PEM
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable --now sean-server.service

echo "[7/9] Opening firewall port $PORT (ufw)..."
if command -v ufw >/dev/null 2>&1; then
  ufw allow "$PORT"/tcp || true
fi

echo "[8/9] Basic health check..."
sleep 2
if systemctl is-active --quiet sean-server.service; then
  echo "Service started successfully."
else
  echo "Service did not start. Check: sudo journalctl -u sean-server.service -b"
fi

echo "[9/9] Done."
echo ""
echo "Client connect example (on each device):"
echo "python main.py --name <you> --connect --server-host <SERVER_IP_or_DOMAIN> --server-port $PORT --server-wss --insecure"
echo ""
echo "Notes:"
echo "- For production use Let's Encrypt and remove --insecure on clients."
echo "- If using Let’s Encrypt, ensure ports 80/443 are reachable before running this script."
exit 0
