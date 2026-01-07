#!/usr/bin/env bash
set -e
# Simple health check: fetch root HTTP path and test websocket handshake using python
HOST=${1:-localhost}
PORT=${2:-8765}
SCHEME=${3:-http}

echo "Checking HTTP root: $SCHEME://$HOST:$PORT/"
if curl -ks "$SCHEME://$HOST:$PORT/" | grep -q "SEAN WebSocket"; then
  echo "HTTP root ok"
else
  echo "HTTP root may not be responding"
fi

# Export to python env
export HEALTH_HOST="$HOST"
export HEALTH_PORT="$PORT"
export HEALTH_SCHEME="$SCHEME"

python - <<'PY'
import asyncio, os, sys
import websockets

HOST = os.environ.get('HEALTH_HOST', 'localhost')
PORT = os.environ.get('HEALTH_PORT', '8765')
SCHEME = os.environ.get('HEALTH_SCHEME', 'http')

use_ssl = SCHEME.lower().startswith('https')
uri = f"{'wss' if use_ssl else 'ws'}://{HOST}:{PORT}"

try:
    async def test_conn():
        if use_ssl:
            import ssl as _ssl
            ssl_ctx = _ssl.SSLContext(_ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = _ssl.CERT_NONE
            async with websockets.connect(uri, ssl=ssl_ctx) as ws:
                print('WS handshake OK (wss)')
        else:
            async with websockets.connect(uri) as ws:
                print('WS handshake OK (ws)')
    asyncio.run(asyncio.wait_for(test_conn(), timeout=3))
except Exception as e:
    print('WS handshake failed:', e)
    sys.exit(2)
PY

echo "Healthcheck finished"
