#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 yourdomain.example.com" && exit 1
fi
DOMAIN=$1
sudo apt update && sudo apt install -y certbot
sudo certbot certonly --standalone -d $DOMAIN
echo "Certs should be in /etc/letsencrypt/live/$DOMAIN/"