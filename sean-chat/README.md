# SEAN - 2-WAY ENCRYPTED CHAT (Console CLI)

Lightweight 2-way messaging CLI with RSA 2048-bit E2EE (ephemeral AES session keys), SQLite storage, and contact management.

Quick start

1. pip install cryptography websockets
2. python main.py
3. add_contact "Friend"
4. chat Friend


Real-time (two-device) quick demo (local):

1. Start the relay server on a machine accessible to both devices:
   - Optional: generate TLS cert/key for WSS:
     - ./gen_cert.sh
   - Start server (non-TLS):
     - python server.py --host 0.0.0.0 --port 8765
   - Or start with TLS:
     - python server.py --host 0.0.0.0 --port 8765 --certfile sean_cert.pem --keyfile sean_key.pem
   - Or use Docker Compose:
     - docker-compose up -d

2. On device A (Alice):
   - python main.py --name alice --connect --server-host <SERVER_IP_OR_HOSTNAME> --server-port 8765
   - If server uses TLS and self-signed cert: add --server-wss --insecure
   - If server uses real CA cert: add --server-wss (no --insecure)

3. On device B (Bob):
   - python main.py --name bob --connect --server-host <SERVER_IP_OR_HOSTNAME> --server-port 8765
   - Use --server-wss/--insecure if applicable

4. Testing & healthchecks
   - Run server healthcheck script on server: ./deploy/healthcheck.sh <host> <port> [http|https]
   - Use the included `test_realtime.py` (adjust --server/--wss/--insecure flags as needed)

4. On Alice: add_contact bob (or Bob add_contact alice), then: chat bob

Notes about networking:
- If server is behind NAT, forward port 8765 from router to server host.
- Use server's public IP or DNS for --server-host. Use --server-wss when server is configured with TLS.
- For production, provide a proper CA-signed cert and disable --insecure.

Docker-compose quick run (run server):
- docker-compose up -d

Files

- `main.py` - CLI
- `crypto.py` - RSA/AES packet handling
- `contacts.py` - Contact management
- `storage.py` - SQLite storage and backups
- `utils.py` - helper utilities
- `config.py` - settings and colors
- `contacts.json` - auto-generated contact backup

Features

- RSA 2048 for encrypting ephemeral AES session keys
- AES-GCM per-message encryption (Perfect forward secrecy)
- SHA-256 tamper detection
- Encrypted private keys (Fernet symmetric) stored in DB
- Message deduplication, rate-limiting, auto-backup

Notes

This demo stores a local symmetric master key in `master.key` to encrypt private keys in the database. For production, protect that key using OS-level keyrings or password-based encryption.
