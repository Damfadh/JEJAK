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

Postgres / Docker Compose
-------------------------

You can run a Postgres-backed development stack with the repository `docker-compose.yml`:

```bash
docker-compose up --build
```

By default `docker-compose.yml` sets `DATABASE_URL=postgres://jejak:jejak_pass@postgres:5432/jejak` for the `backend` service. Set `API_KEY` in your environment to protect the `POST /register-key` endpoint.

Metrics
-------

If `prometheus_client` is installed, the app exposes `/metrics` for Prometheus scraping.

Rate limiting
-------------

A simple in-memory rate limiter protects `POST /register-key` (default: 10 requests/minute per IP). For production use a distributed limiter (Redis) or API gateway.

Compose demo (multi-service)
----------------------------

A demo signer service is included in `docker-compose.yml` and builds from `demo/signer`. It runs the `scripts/batch_sign.py` CLI against `tests/fixtures/sample_batch.csv` and writes artifacts to the host `./artifacts` folder (sample_signed.zip and ci_key.b64).

To run the full demo stack:

```bash
docker-compose up --build
```

After startup the signed ZIP will be available in `./artifacts/sample_signed.zip` on the host.

Note: the signer runs once and exits; `docker-compose up` will keep other services running. Use `docker-compose up --build --abort-on-container-exit` to stop when signer finishes.
