import urllib.request
import sys

url = 'http://127.0.0.1:5000/'
try:
    r = urllib.request.urlopen(url, timeout=5)
    content = r.read(800).decode('utf-8', errors='replace')
    print('STATUS: OK')
    print('CONTENT PREVIEW (first 400 chars):')
    print(content[:400])
except Exception as e:
    print('STATUS: ERROR')
    print(repr(e))
    sys.exit(1)
