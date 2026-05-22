# JEJAK Backend (PKI Registry)

Minimal FastAPI service to register publisher public keys and verify signed payloads. Uses a local SQLite database `pki.db` for demo purposes.

Run (development):

```powershell
python -m pip install -r backend/requirements.txt
uvicorn backend.app:app --reload --port 8000
```

Run (Docker):

```bash
docker build -t jejak-backend:latest backend
docker run -p 8000:8000 -v $(pwd)/backend:/app/backend jejak-backend:latest
```

Endpoints:
- `POST /register-key` — body: `{ "publisher_id": "...", "public_key_base64": "..." }`
- `GET /key/{publisher_id}` — returns public key base64
- `POST /verify` — body: `{ "signed_payload": { ... } }` returns `{ "valid": true/false }` and writes audit entry to DB
- `GET /health` — returns service health
- `GET /ready` — returns readiness (database tables available)

Note: This is a demo implementation; for production use a real database, authentication, rate limiting, and secure key management. The Dockerfile uses SQLite — mount a volume for persistence.
