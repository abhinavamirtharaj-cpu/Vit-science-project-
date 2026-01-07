"""Integration test: two websocket clients (alice, bob) connect to server and exchange encrypted packet"""
import asyncio
import json
import time

import websockets
from crypto import generate_rsa_keypair, encrypt_packet, decrypt_packet

import argparse
import ssl as _ssl


parser = argparse.ArgumentParser()
parser.add_argument('--server', default='localhost', help='Server host')
parser.add_argument('--port', default=8765, type=int)
parser.add_argument('--wss', action='store_true')
parser.add_argument('--insecure', action='store_true')
args = parser.parse_args()

scheme = 'wss' if args.wss else 'ws'
URI = f"{scheme}://{args.server}:{args.port}"

async def client_behaviour(name, pub_pem, priv_pem, peer_name, peer_pub_pem, send_message=None):
    ssl_ctx = None
    if args.wss:
        if args.insecure:
            ssl_ctx = _ssl.SSLContext(_ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = _ssl.CERT_NONE
        else:
            ssl_ctx = _ssl.create_default_context()
    async with websockets.connect(URI, ssl=ssl_ctx) as ws:
        await ws.send(json.dumps({'type':'auth','name':name,'public_key':pub_pem.decode()}))
        # process some incoming initial messages
        await asyncio.sleep(0.2)
        if send_message:
            packet = encrypt_packet(peer_pub_pem, send_message, sender_pub_pem=pub_pem)
            await ws.send(json.dumps({'type':'send','to':peer_name,'packet':packet,'ts':time.strftime('%Y-%m-%dT%H:%M:%S')}))
            # wait for status
            await asyncio.sleep(0.5)
        # listen briefly
        try:
            while True:
                raw = await asyncio.wait_for(ws.recv(), timeout=1.0)
                data = json.loads(raw)
                print(f"{name} recv: {data}")
                if data.get('type')=='deliver':
                    pkt = data.get('packet')
                    pt = decrypt_packet(pkt, priv_pem)
                    print(f"{name} decrypted: {pt}")
                    # ack back
                    await ws.send(json.dumps({'type':'ack','packet_id':json.loads(pkt)['packet_id'],'status':'read','for':data.get('from')}))
        except asyncio.TimeoutError:
            pass

async def main():
    # generate keys
    a_pub, a_priv = generate_rsa_keypair()
    b_pub, b_priv = generate_rsa_keypair()
    # run both clients concurrently, with alice sending
    await asyncio.gather(
        client_behaviour('alice', a_pub, a_priv, 'bob', b_pub, send_message='Hello Bob (test)'),
        client_behaviour('bob', b_pub, b_priv, 'alice', a_pub)
    )

if __name__ == '__main__':
    asyncio.run(main())
