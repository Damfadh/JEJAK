import os
import sys
import json
import sqlite3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi.testclient import TestClient
from backend.app import app


def test_register_and_verify(tmp_path):
    # ensure fresh DB for test
    db_path = os.path.join(ROOT, 'backend', 'pki.db')
    if os.path.exists(db_path):
        os.remove(db_path)

    with TestClient(app) as client:
        # load demo public key and signed payload
        pubfile = os.path.join(ROOT, 'Coding', 'demo_key_public.b64.txt')
        payload_file = os.path.join(ROOT, 'Coding', 'demo_signed_payload.json')
        with open(pubfile, 'r', encoding='utf-8') as f:
            pub = f.read().strip()
        with open(payload_file, 'r', encoding='utf-8') as f:
            sp = json.load(f)

        # register key
        r = client.post('/register-key', json={
            'publisher_id': sp.get('publisher_id'),
            'public_key_base64': pub,
        })
        if r.status_code != 200:
            try:
                print('register response json:', r.json())
            except Exception:
                print('register response text:', r.text)
        assert r.status_code == 200
        assert r.json().get('ok') is True

        # verify
        r2 = client.post('/verify', json={'signed_payload': sp})
        assert r2.status_code == 200
        assert r2.json().get('valid') is True

    # check audit DB
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    rows = c.execute("SELECT result FROM audit WHERE publisher_id=? ORDER BY id DESC", (sp.get('publisher_id'),)).fetchall()
    conn.close()
    assert rows and rows[0][0] == 'valid'
