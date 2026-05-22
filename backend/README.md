# JEJAK Backend (PKI Registry)

Minimal FastAPI service to register publisher public keys and verify signed payloads. Uses a local SQLite database `pki.db` for demo purposes.

Run (development):

```powershell
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --reload --port 8000
```

Endpoints:
- `POST /register-key` — body: `{ "publisher_id": "...", "public_key_base64": "..." }`
- `GET /key/{publisher_id}` — returns public key base64
- `POST /verify` — body: `{ "signed_payload": { ... } }` returns `{ "valid": true/false }` and writes audit entry to DB

Note: This is a demo implementation; for production use a real database, authentication, rate limiting, and secure key management.
