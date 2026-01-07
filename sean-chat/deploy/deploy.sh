#!/usr/bin/env bash
set -euo pipefail

# Usage: sudo ./deploy.sh yourdomain.example.com
# Will install deps, create user, clone repo if missing, setup virtualenv and systemd service
DOMAIN=${1:-}
if [ -z "$DOMAIN" ]; then
  echo "Usage: sudo $0 yourdomain.example.com" && exit 1
fi

REPO_DIR=/opt/sean
SERVICE_FILE=/etc/systemd/system/sean-server.service

# Create service user
id -u sean >/dev/null 2>&1 || sudo useradd --system --group --no-create-home sean

# Ensure code in place
if [ ! -d "$REPO_DIR" ]; then
  echo "Cloning repository into $REPO_DIR"
  git clone https://github.com/your/repo.git "$REPO_DIR"
fi
cd "$REPO_DIR"

# Create venv and install deps
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install cryptography websockets

# Generate cert with certbot (assumes port 80 free); you may prefer DNS mode for cert issuance
if command -v certbot >/dev/null 2>&1; then
  certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN || true
  CERT=/etc/letsencrypt/live/$DOMAIN/fullchain.pem
  KEY=/etc/letsencrypt/live/$DOMAIN/privkey.pem
else
  echo "certbot not installed; you may manually provide cert at /etc/ssl/sean_cert.pem"
  CERT=/etc/ssl/sean_cert.pem
  KEY=/etc/ssl/sean_key.pem
fi

# Copy service file and enable
sudo mkdir -p /opt/sean
sudo chown -R sean:sean /opt/sean
sudo cp deploy/sean.service "$SERVICE_FILE"
# Replace cert path if certbot generated certs
if [ -f "$CERT" ]; then
  sudo sed -i "s|/etc/ssl/sean_cert.pem|$CERT|" "$SERVICE_FILE" || true
  sudo sed -i "s|/etc/ssl/sean_key.pem|$KEY|" "$SERVICE_FILE" || true
fi
sudo systemctl daemon-reload
sudo systemctl enable --now sean-server.service
sudo systemctl status --no-pager sean-server.service

# Open firewall port
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow 8765/tcp
fi

echo "Deployment finished. Check server logs: sudo journalctl -u sean-server.service -f"
