import sqlite3
import json
import os
import sys

# ensure project root on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Coding.core.crypto import DocumentVerifier

DB = 'backend/pki.db'

def get_pub(publisher_id='DEMO-PUBLISHER'):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    row = c.execute('SELECT public_key FROM publishers WHERE publisher_id=?', (publisher_id,)).fetchone()
    conn.close()
    return row[0] if row else None

def main():
    pub = get_pub()
    print('pub from db:', pub)
    with open('Coding/demo_signed_payload.json','r',encoding='utf-8') as f:
        sp = json.load(f)
    v = DocumentVerifier(pub)
    print('verify with db pub:', v.verify_payload(sp))

if __name__ == '__main__':
    main()
