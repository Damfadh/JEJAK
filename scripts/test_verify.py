import os
import sys
import json

# ensure project root in sys.path so `core` package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Coding.core.crypto import DocumentVerifier

PUBFILE = "Coding/demo_key_public.b64.txt"
PAYLOAD = "Coding/demo_signed_payload.json"

def main():
    with open(PUBFILE, 'r', encoding='utf-8') as f:
        pub = f.read().strip()

    with open(PAYLOAD, 'r', encoding='utf-8') as f:
        sp = json.load(f)

    v = DocumentVerifier(pub)
    ok = v.verify_payload(sp)
    print('verify result:', ok)

if __name__ == '__main__':
    main()
