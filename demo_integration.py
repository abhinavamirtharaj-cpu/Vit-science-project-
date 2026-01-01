"""
Demo integration script showing how to import `storage.py` and use its API.
Usage:
  python demo_integration.py

This script appends a couple of test messages for a contact and prints the retrieved history.
"""
from storage import append_message, append_messages, get_history, get_csv_path
from datetime import datetime

CONTACT = {'id': 'demo_device', 'name': 'Demo Device'}

if __name__ == '__main__':
    now_iso = datetime.utcnow().isoformat()
    msg1 = {'dir': 'sent', 'iso': now_iso, 'date': datetime.utcnow().date().isoformat(), 'time': datetime.utcnow().time().strftime('%H:%M'), 'text': 'Hello from demo_integration - single append'}
    print('Appending single message...')
    append_message(CONTACT, msg1)

    msg2 = {'dir': 'sent', 'iso': now_iso, 'date': datetime.utcnow().date().isoformat(), 'time': datetime.utcnow().time().strftime('%H:%M'), 'text': 'Second message via append_messages'}
    print('Appending multiple messages...')
    append_messages(CONTACT, [msg2])

    print('\nSaved CSV path:', get_csv_path())

    print('\nHistory for contact', CONTACT['id'])
    hist = get_history(CONTACT['id'])
    for i,m in enumerate(hist[-10:], start=1):
        print(f"{i}. [{m['date']} {m['time']}] {m['dir']}: {m['text']}")