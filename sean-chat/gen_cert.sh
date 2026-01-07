#!/usr/bin/env bash
# Generate self-signed cert and key for demo
set -e
CERT=sean_cert.pem
KEY=sean_key.pem
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY" -out "$CERT" -subj "/CN=sean.local"
ls -l "$CERT" "$KEY"
echo "Generated $CERT and $KEY"