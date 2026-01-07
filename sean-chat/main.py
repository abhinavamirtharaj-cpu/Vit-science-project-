"""SEAN - Main CLI
Run: python main.py
"""
import sys
import threading
import time
import logging
import argparse
import asyncio
import json
from collections import deque, defaultdict
from pathlib import Path

import websockets

from config import Colors, STATUS_ICONS, LOG_FILE, SERVER_HOST, SERVER_PORT
from utils import now_ts, human_size, sanitize_name
from storage import Storage
import contacts as contacts_mod
import crypto

# Basic logger
logging.basicConfig(filename=str(LOG_FILE), level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('sean')

storage = Storage()

# Identity (default 'me'). Will be set from CLI args.
IDENTITY_NAME = 'me'

def ensure_my_identity(name: str = 'me'):
    me = storage.get_contact(name)
    if not me:
        pub, priv = crypto.generate_rsa_keypair()
        storage.add_contact(name, pub, crypto.encrypt_private_pem(priv))
        logger.info('Generated local identity `%s`', name)
    return storage.get_contact(name)

# Will be initialized after arg parsing

# Rate limiting: 5 messages per minute per contact
_rate_windows = defaultdict(lambda: deque())

# Simple in-memory "delivered" simulator
def mark_delivered_in_background(packet_id):
    def worker():
        time.sleep(0.6)
        storage.update_message_status(packet_id, 'delivered')
        time.sleep(1.0)
        storage.update_message_status(packet_id, 'read')
    t = threading.Thread(target=worker, daemon=True)
    t.start()


# WebSocket client for real-time messaging
class WSClient:
    def __init__(self, name: str, host: str = SERVER_HOST, port: int = SERVER_PORT, use_ssl: bool = False, insecure: bool = False):
        self.name = name
        scheme = 'wss' if use_ssl else 'ws'
        self.uri = f"{scheme}://{host}:{port}"
        self.ws = None
        self.loop = None
        self._thread = None
        self.running = False
        self.use_ssl = use_ssl
        self.insecure = insecure
        self._stop = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_loop())

    async def _connect_loop(self):
        delay = 0.5
        while not self._stop.is_set():
            try:
                await self._connect()
            except Exception:
                logger.exception("WebSocket _connect failed; retrying in %.1fs", delay)
                await asyncio.sleep(delay)
                delay = min(5.0, delay * 2)
            else:
                delay = 0.5
                await asyncio.sleep(0.5)

    async def _connect(self):
        ssl_ctx = None
        if self.use_ssl:
            import ssl as _ssl
            if self.insecure:
                ssl_ctx = _ssl.SSLContext(_ssl.PROTOCOL_TLS_CLIENT)
                ssl_ctx.check_hostname = False
                ssl_ctx.verify_mode = _ssl.CERT_NONE
            else:
                ssl_ctx = _ssl.create_default_context()
        try:
            async with websockets.connect(self.uri, ssl=ssl_ctx) as ws:
                self.ws = ws
                # send auth
                my = storage.get_contact(self.name)
                if not my:
                    ensure_my_identity(self.name)
                    my = storage.get_contact(self.name)
                pub = my[1].decode() if isinstance(my[1], (bytes, bytearray)) else my[1]
                await ws.send(json.dumps({"type": "auth", "name": self.name, "public_key": pub}))
                self.running = True
                async for raw in ws:
                    try:
                        data = json.loads(raw)
                        await self._handle(data)
                    except Exception:
                        logger.exception("Error handling incoming ws message")
        except Exception:
            logger.exception("WebSocket connection failed")
        finally:
            self.running = False

    async def _handle(self, data: dict):
        typ = data.get('type')
        if typ == 'deliver':
            frm = data.get('from')
            packet = data.get('packet')
            # store locally
            try:
                pkt = json.loads(packet)
                packet_id = pkt.get('packet_id')
            except Exception:
                packet_id = None
            storage.add_message(packet_id or '', frm, 'received', packet, time.strftime('%Y-%m-%dT%H:%M:%S'), 'delivered', len(packet.encode()))
            # notify server that we've delivered
            await self._send({"type": "ack", "packet_id": packet_id, "status": "delivered", "for": frm})
            # show message
            try:
                my_priv = crypto.decrypt_private_pem(storage.get_contact(self.name)[2])
                pt = crypto.decrypt_packet(packet, my_priv)
            except Exception as e:
                pt = f"[DECRYPT ERROR: {e}]"
            print_color(f"[{now_ts()}] {frm} → {pt} [🔓DECRYPTED]", Colors.OKBLUE)

        elif typ == 'presence':
            name = data.get('name')
            pub = data.get('public_key')
            if name and pub:
                storage.add_contact(name, pub.encode(), None)
                logger.info('Presence: %s', name)
        elif typ == 'roster':
            for c in data.get('contacts', []):
                if c.get('name') and c.get('public_key'):
                    storage.add_contact(c['name'], c['public_key'].encode(), None)
        elif typ == 'status':
            packet_id = data.get('packet_id')
            status = data.get('status')
            storage.update_message_status(packet_id, status)
            logger.info('Status update %s -> %s', packet_id, status)

    async def _send(self, obj: dict):
        if not self.ws:
            raise RuntimeError('Not connected')
        await self.ws.send(json.dumps(obj))

    def send_send(self, to: str, packet: str):
        if not self.running:
            return
        asyncio.run_coroutine_threadsafe(self._send({"type": "send", "to": to, "packet": packet, "ts": time.strftime('%Y-%m-%dT%H:%M:%S')}), self.loop)

    def is_connected(self) -> bool:
        return self.running

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)


def print_color(text: str, color: str = ''):
    end = Colors.ENDC if color else ''
    print(f"{color}{text}{end}")


def cmd_help():
    help_text = '''Commands:
  help                    - Show this help
  add_contact <name>      - Add contact (auto-generates keys)
  list_contacts           - Show all contacts
  chat <name>             - Start 2-way chat session
  history <name> [search] - Show chat history (search optional)
  clear_history <name>    - Delete chat history
  delete_contact <name>   - Remove contact + history
  generate_keys           - Regenerate my key pair
  backup                  - Backup contacts + messages
  restore <path>          - Restore from backup DB file
  exit                    - Quit SEAN
'''
    print(help_text)


def cmd_add_contact(name: str):
    if not name:
        print_color('Name required', Colors.FAIL)
        return
    info = contacts_mod.add_contact(name)
    print_color(f"Added contact {info['name']}", Colors.OKGREEN)


def cmd_list_contacts():
    rows = contacts_mod.list_contacts()
    if not rows:
        print('No contacts')
        return
    for r in rows:
        name = r['name']
        public = r['public_key'][:40] + '...' if r['public_key'] else 'N/A'
        print(f"- {name}  {Colors.OKBLUE}{public}{Colors.ENDC}")


def decrypt_message_for_display(row):
    encrypted_packet = row['encrypted_packet']
    direction = row['direction']
    try:
        if direction == 'received':
            # decrypt with my private key
            my_priv = crypto.decrypt_private_pem(storage.get_contact(IDENTITY_NAME)[2])
            pt = crypto.decrypt_packet(encrypted_packet, my_priv)
            state = '🔓DECRYPTED'
        else:
            # sent messages: decrypt with my private key (sender copy)
            my_priv = crypto.decrypt_private_pem(storage.get_contact(IDENTITY_NAME)[2])
            pt = crypto.decrypt_packet(encrypted_packet, my_priv)
            state = '🔒SENT'
    except Exception as e:
        pt = f"[DECRYPT ERROR: {e}]"
        state = '⚠️ERROR'
    return pt, state


def cmd_history(name: str, search: str = None):
    row_contact = storage.get_contact(name)
    if not row_contact:
        print_color('Contact not found', Colors.FAIL)
        return
    rows = storage.get_history(name)
    # decrypt and filter if search
    hits = []
    for r in rows:
        pt, state = decrypt_message_for_display(r)
        if search:
            if search.lower() in pt.lower():
                hits.append((r, pt, state))
        else:
            hits.append((r, pt, state))
    for r, pt, state in hits:
        ts = r['timestamp'][:16].replace('T', ' ')
        direction = r['direction']
        who = 'You' if direction == 'sent' else name
        size = human_size(r['size_bytes'])
        color = Colors.OKGREEN if direction == 'sent' else Colors.OKBLUE
        print_color(f"[{ts}] {who} → {pt} [{state}][{size}]", color)


def cmd_clear_history(name: str):
    if not storage.get_contact(name):
        print_color('Contact not found', Colors.FAIL)
        return
    storage.clear_history(name)
    print_color('History cleared', Colors.OKGREEN)


def cmd_delete_contact(name: str):
    if not storage.get_contact(name):
        print_color('Contact not found', Colors.FAIL)
        return
    storage.delete_contact(name)
    print_color('Contact deleted', Colors.OKGREEN)


def cmd_generate_keys():
    # regenerate local keys for this identity
    pub, priv = crypto.generate_rsa_keypair()
    storage.add_contact(IDENTITY_NAME, pub, crypto.encrypt_private_pem(priv))
    print_color('New local key pair generated', Colors.OKGREEN)


def cmd_backup():
    dest = storage.backup_db()
    print_color(f'Backup created: {dest}', Colors.OKGREEN)


def cmd_restore(path: str):
    pathp = Path(path)
    if not pathp.exists():
        print_color('Backup file not found', Colors.FAIL)
        return
    storage.restore_db(pathp)
    print_color('DB restored. Restart may be required.', Colors.WARNING)


def send_message(to_name: str, message: str):
    contact = storage.get_contact(to_name)
    if not contact:
        print_color('No such contact', Colors.FAIL)
        return
    # rate limit
    q = _rate_windows[to_name]
    now = time.time()
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= 5:
        print_color('Rate limit exceeded (5 msg/min)', Colors.FAIL)
        return
    q.append(now)

    # encrypt packet (include sender's pub so sender can later decrypt)
    my = storage.get_contact('me')
    my_pub = my[1]
    packet = crypto.encrypt_packet(contact[1], message, sender_pub_pem=my_pub)
    size = len(packet.encode())
    packet_json = packet
    # store as sent
    packet_obj = json.loads(packet_json)
    packet_id = packet_obj['packet_id']
    storage.add_message(packet_id, to_name, 'sent', packet_json, time.strftime('%Y-%m-%dT%H:%M:%S'), 'sent', size)
    print_color(f"[{now_ts()}] You → {message} [🔒SENT][{human_size(size)}]", Colors.OKGREEN)

    # If we are connected to a server, send via real-time relay
    if 'ws_client' in globals() and ws_client and ws_client.is_connected():
        ws_client.send_send(to_name, packet_json)
    else:
        # mark delivered/read asynchronously (local simulation)
        mark_delivered_in_background(packet_id)

        # auto-backup every 10 messages
        if storage.count_messages() % 10 == 0:
            storage.backup_db()

        # Simulate friend auto-reply (for demo only)
        def auto_reply():
            time.sleep(0.8)
            reply = f"Echo: {message}"
            # encrypt reply for me with my public key, but mark sender as contact (friend)
            # Friend encrypts to me: use my public key
            my_pub = storage.get_contact(IDENTITY_NAME)[1]
            # Friend's public key used as sender identifier
            friend_pub = contact[1]
            packet_reply = crypto.encrypt_packet(my_pub, reply, sender_pub_pem=friend_pub)
            size2 = len(packet_reply.encode())
            pkt = json.loads(packet_reply)
            storage.add_message(pkt['packet_id'], to_name, 'received', packet_reply, time.strftime('%Y-%m-%dT%H:%M:%S'), 'delivered', size2)
            print_color(f"[{now_ts()}] {to_name} → {reply} [🔓DECRYPTED][{human_size(size2)}]", Colors.OKBLUE)
        t = threading.Thread(target=auto_reply, daemon=True)
        t.start()


def chat_session(name: str):
    contact = storage.get_contact(name)
    if not contact:
        print_color('Contact not found', Colors.FAIL)
        return
    print_color(f"=== CHAT WITH {name.upper()} ===", Colors.HEADER)
    # show last few messages
    cmd_history(name)
    print("Type 'exit' to end chat...")
    while True:
        try:
            msg = input('> ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not msg:
            continue
        if msg.strip().lower() == 'exit':
            break
        send_message(name, msg)


def repl():
    print_color('SEAN - 2-way encrypted chat (console). Type "help" for commands.', Colors.HEADER)
    while True:
        try:
            line = input(f'{IDENTITY_NAME}$ ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == 'help':
            cmd_help()
        elif cmd == 'add_contact':
            name = ' '.join(args).strip('"') if args else ''
            cmd_add_contact(name)
        elif cmd == 'list_contacts':
            cmd_list_contacts()
        elif cmd == 'chat':
            if not args:
                print_color('Specify contact', Colors.FAIL)
            else:
                chat_session(' '.join(args))
        elif cmd == 'history':
            if not args:
                print_color('Usage: history <name> [search]', Colors.FAIL)
            else:
                name = args[0]
                search = ' '.join(args[1:]) if len(args) > 1 else None
                cmd_history(name, search)
        elif cmd == 'clear_history':
            if not args:
                print_color('Specify contact', Colors.FAIL)
            else:
                cmd_clear_history(' '.join(args))
        elif cmd == 'delete_contact':
            if not args:
                print_color('Specify contact', Colors.FAIL)
            else:
                cmd_delete_contact(' '.join(args))
        elif cmd == 'generate_keys':
            cmd_generate_keys()
        elif cmd == 'backup':
            cmd_backup()
        elif cmd == 'restore':
            if not args:
                print_color('Specify backup path', Colors.FAIL)
            else:
                cmd_restore(args[0])
        elif cmd == 'exit' or cmd == 'quit':
            print_color('Goodbye!', Colors.WARNING)
            break
        else:
            print_color('Unknown command; type help', Colors.FAIL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='me', help='Identity name for this client')
    parser.add_argument('--connect', action='store_true', help='Connect to real-time relay server')
    parser.add_argument('--server-host', default=SERVER_HOST, help='Server host')
    parser.add_argument('--server-port', default=SERVER_PORT, type=int, help='Server port')
    parser.add_argument('--server-wss', action='store_true', help='Use WSS/TLS to connect')
    parser.add_argument('--insecure', action='store_true', help='Skip TLS verification (for self-signed certs)')
    args = parser.parse_args()

    # set identity and ensure keys
    IDENTITY_NAME = args.name
    ensure_my_identity(IDENTITY_NAME)

    ws_client = None
    if args.connect:
        ws_client = WSClient(IDENTITY_NAME, args.server_host, args.server_port, use_ssl=args.server_wss, insecure=args.insecure)
        ws_client.start()
        # allow a moment to connect
        time.sleep(0.6)

    try:
        repl()
    finally:
        if ws_client:
            ws_client.stop()
        storage.close()
        print_color('Session saved. Bye!', Colors.WARNING)
