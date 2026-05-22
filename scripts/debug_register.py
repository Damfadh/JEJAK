import os
import sys
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from backend.app import app

def main():
    client = TestClient(app)
    pubfile = os.path.join(ROOT, 'Coding', 'demo_key_public.b64.txt')
    with open(pubfile, 'r', encoding='utf-8') as f:
        pub = f.read().strip()

    payload = {'publisher_id': 'DEMO-PUBLISHER', 'public_key_base64': pub}
    r = client.post('/register-key', json=payload)
    print('status:', r.status_code)
    try:
        print('json:', r.json())
    except Exception:
        print('text:', r.text)

if __name__ == '__main__':
    main()
