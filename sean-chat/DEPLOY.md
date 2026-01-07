SEAN - Deployment & Two-Device Test Guide

This guide shows how to deploy the SEAN real-time relay server on a cloud VM and connect two devices (Alice and Bob) to test real 2-person encrypted messaging.

Prerequisites (server)
- A VM or server with a public IP or DNS name (Ubuntu 22.04+ recommended).
- Open port 8765 TCP for the SEAN WebSocket server (or port you choose).
- Optional: domain name for the server (recommended for TLS/Let's Encrypt).

Quick summary (high level)
1. Provision VM and clone repository to `/opt/sean`.
2. Install Python 3.x and dependencies (`pip install -r requirements` or `pip install websockets cryptography`).
3. Obtain TLS cert (recommended: certbot/Let's Encrypt) or use `gen_cert.sh` for testing.
4. Install systemd service (`sean-server.service`) to run `server.py` and enable/start it.
5. Open firewall ports (ufw/iptables) and ensure port forwarding if behind NAT.
6. On Device A and B: run `python main.py --name alice --connect --server-host <SERVER_HOST> --server-port 8765 [--server-wss --insecure]`.

Detailed commands (Ubuntu example)

1) Create a deployment user and clone project

    sudo adduser --system --group --no-create-home sean
    sudo mkdir -p /opt/sean
    sudo chown $USER:$USER /opt/sean
    cd /opt
    git clone <repo-url> sean
    cd sean

2) Set up virtualenv and install deps

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install cryptography websockets

3) TLS certificate (production recommended)

- Using Let's Encrypt (certbot):

    sudo apt update && sudo apt install -y certbot
    sudo certbot certonly --standalone -d yourdomain.example.com

  Generated certpaths:
    - /etc/letsencrypt/live/yourdomain.example.com/fullchain.pem
    - /etc/letsencrypt/live/yourdomain.example.com/privkey.pem

- For testing (self-signed):

    ./gen_cert.sh
    # produces sean_cert.pem and sean_key.pem in repo root

4) Systemd service (example created in repo as `deploy/sean.service`) — install

    sudo cp deploy/sean.service /etc/systemd/system/sean-server.service
    # Edit ExecStart paths if you used a venv or different paths
    sudo systemctl daemon-reload
    sudo systemctl enable --now sean-server.service
    sudo journalctl -u sean-server.service -f

5) Firewall

    sudo ufw allow 8765/tcp
    sudo ufw enable

6) Connect from Device A (Alice) and Device B (Bob)

- If server uses TLS (WSS) with a public CA cert:

    python main.py --name alice --connect --server-host yourdomain.example.com --server-port 8765 --server-wss

- If server uses self-signed cert (testing):

    python main.py --name alice --connect --server-host <SERVER_IP> --server-port 8765 --server-wss --insecure

7) Test flow

- On Alice: `add_contact bob`, `chat bob`, send message.
- On Bob: `add_contact alice`, `chat alice`, you should receive it (decrypts locally).

Health checks & quick commands
- Verify server HTTP root response (HTTP response given by process_request):
    curl -k https://yourdomain.example.com:8765/
- Check listening port:
    ss -ltn | grep 8765
- Use the included `test_realtime.py` for scripted integration checks.

Notes & troubleshooting
- Ensure the server has port 8765 open in any cloud security groups (e.g., AWS Security Group).
- For NAT: forward external port 8765 to the VM internal IP.
- For production: use a proper CA-signed TLS cert; never use `--insecure` in production.
- If a client cannot connect, test from another machine on the same network or run `telnet SERVER_IP 8765`.

If you want, I can (pick one):
- Provide a `cloud-init` snippet to bootstrap a VM automatically, or
- Create a `docker-compose` TLS-enabled service with certbot automation, or
- SSH into a test VM and provision it for you (requires access).
