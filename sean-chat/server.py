"""Simple WebSocket relay server for SEAN messaging

- Clients authenticate with their `name` and `public_key` on connect
- Server stores public keys and messages in its own DB
- Server forwards encrypted packets to connected recipients
"""
import argparse
import asyncio
import json
import logging
import ssl
from typing import Dict, Optional, Tuple, List

import websockets

from storage import Storage

logger = logging.getLogger('sean.server')
logging.basicConfig(level=logging.INFO)

STORAGE = Storage()
CONNECTED: Dict[str, object] = {}


async def notify_presence(new_name: str, public_key: str):
    payload = json.dumps({"type": "presence", "name": new_name, "public_key": public_key})
    for name, ws in list(CONNECTED.items()):
        if name != new_name:
            try:
                await ws.send(payload)
            except Exception:
                logger.exception("Failed to notify %s of presence", name)


# Respond to plain HTTP requests to give a friendly message and avoid Upgrade errors
# process_request returns an HTTP status tuple when path is not a websocket handshake
async def process_request(path: str, request_headers) -> Optional[Tuple[int, List[Tuple[str, str]], bytes]]:
    if path == '/':
        body = b"SEAN WebSocket Relay Server. Connect with WebSocket to exchange encrypted packets."
        headers = [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))]
        return 200, headers, body
    # For other paths, return a helpful 426 response
    body = b"This endpoint is a WebSocket server. Use a WebSocket client to connect."
    headers = [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))]
    return 426, headers, body


async def send_status(to_name: str, packet_id: str, status: str):
    ws = CONNECTED.get(to_name)
    if not ws:
        return
    try:
        await ws.send(json.dumps({"type": "status", "packet_id": packet_id, "status": status}))
    except Exception:
        logger.exception("Failed to send status to %s", to_name)


async def handle_message(sender: str, data: dict):
    typ = data.get('type')
    if typ == 'send':
        to = data.get('to')
        packet = data.get('packet')
        try:
            pkt = json.loads(packet)
            packet_id = pkt.get('packet_id')
        except Exception:
            packet_id = None
        # store message on server side
        STORAGE.add_message(packet_id or '', to, 'sent', packet, data.get('ts') or '', 'pending', len(packet.encode()))

        # try to forward
        ws_to = CONNECTED.get(to)
        if ws_to:
            try:
                await ws_to.send(json.dumps({"type": "deliver", "from": sender, "packet": packet}))
                STORAGE.update_message_status(packet_id or '', 'delivered')
                await send_status(sender, packet_id, 'delivered')
            except Exception:
                logger.exception("Forward failed")
        else:
            logger.info("Recipient %s offline, stored as pending", to)

    elif typ == 'ack':
        packet_id = data.get('packet_id')
        status = data.get('status')
        STORAGE.update_message_status(packet_id, status)
        # forward to sender if present
        sender_of = data.get('for')
        if sender_of and sender_of in CONNECTED:
            try:
                await CONNECTED[sender_of].send(json.dumps({"type": "status", "packet_id": packet_id, "status": status}))
            except Exception:
                logger.exception("Failed to forward ack")


async def handler(ws, path: str):
    # Expect auth message first
    name = None
    try:
        msg = await ws.recv()
        data = json.loads(msg)
        if data.get('type') != 'auth' or not data.get('name'):
            await ws.send(json.dumps({"type": "error", "message": "Auth required"}))
            await ws.close()
            return
        name = data.get('name')
        pub = data.get('public_key')
        if name in CONNECTED:
            await ws.send(json.dumps({"type": "error", "message": "Name already connected"}))
            await ws.close()
            return
        CONNECTED[name] = ws
        # store contact public key on server
        STORAGE.add_contact(name, pub.encode(), None)
        logger.info("%s connected", name)
        # notify others
        await notify_presence(name, pub)

        # send roster to new client
        rows = STORAGE.list_contacts()
        roster = []
        for r in rows:
            roster.append({"name": r[0], "public_key": r[1].decode() if isinstance(r[1], (bytes, bytearray)) else r[1]})
        await ws.send(json.dumps({"type": "roster", "contacts": roster}))

        # process incoming messages
        async for raw in ws:
            try:
                data = json.loads(raw)
                await handle_message(name, data)
            except Exception:
                logger.exception("Error processing message from %s", name)

    except websockets.ConnectionClosed:
        logger.info("Connection closed for %s", name)
    except Exception:
        logger.exception("Connection error")
    finally:
        if name and name in CONNECTED:
            del CONNECTED[name]
            logger.info("%s disconnected", name)
            # notify others of departure
            await notify_presence(name, '')


async def _serve(host: str, port: int, certfile: Optional[str], keyfile: Optional[str]):
    ssl_ctx = None
    if certfile and keyfile:
        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_ctx.load_cert_chain(certfile=certfile, keyfile=keyfile)
        logger.info("TLS enabled for server")

    server = await websockets.serve(handler, host, port, ssl=ssl_ctx, process_request=process_request)
    logger.info("SEAN server running on %s:%d", host, port)
    await asyncio.Future()  # run forever


def main(host: str = 'localhost', port: int = 8765, certfile: Optional[str] = None, keyfile: Optional[str] = None):
    asyncio.run(_serve(host, port, certfile, keyfile))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SEAN relay server')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=8765, type=int)
    parser.add_argument('--certfile', default=None, help='Path to TLS cert (PEM)')
    parser.add_argument('--keyfile', default=None, help='Path to TLS key (PEM)')
    args = parser.parse_args()
    main(args.host, args.port, args.certfile, args.keyfile)
