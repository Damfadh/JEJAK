from fastapi import FastAPI, HTTPException, Request, Depends, Response
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime
import json
import time
from typing import Optional

# optional deps
try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except Exception:
    HAS_PSYCOPG2 = False

try:
    from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
    HAS_PROM = True
except Exception:
    HAS_PROM = False

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, "pki.db")

# Database URL e.g. postgres://user:pass@postgres:5432/jejak
DATABASE_URL = os.getenv("DATABASE_URL")
USE_POSTGRES = bool(DATABASE_URL) and HAS_PSYCOPG2

# simple in-memory rate limiter {key: [timestamps]}
RATE_LIMIT = {}
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "10"))

# API key for protecting register endpoint
API_KEY = os.getenv("API_KEY")

# Prometheus metrics
if HAS_PROM:
    METRIC_REQUESTS = Counter("jejak_requests_total", "Total HTTP requests", ["path", "method"])
    METRIC_VERIFY_OK = Counter("jejak_verify_ok_total", "Verify success total")
    METRIC_VERIFY_FAIL = Counter("jejak_verify_fail_total", "Verify fail total")
else:
    METRIC_REQUESTS = METRIC_VERIFY_OK = METRIC_VERIFY_FAIL = None


def get_db():
    if USE_POSTGRES:
        # psycopg2 connection
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    if USE_POSTGRES:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id TEXT PRIMARY KEY,
                public_key TEXT,
                created_at TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS audit (
                id SERIAL PRIMARY KEY,
                timestamp TEXT,
                publisher_id TEXT,
                doc_id TEXT,
                recipient_id TEXT,
                result TEXT,
                raw_payload TEXT
            )
            """
        )
        conn.commit()
        conn.close()
    else:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS publishers (
                publisher_id TEXT PRIMARY KEY,
                public_key TEXT,
                created_at TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                publisher_id TEXT,
                doc_id TEXT,
                recipient_id TEXT,
                result TEXT,
                raw_payload TEXT
            )
            """
        )
        conn.commit()
        conn.close()


class RegisterKey(BaseModel):
    publisher_id: str
    public_key_base64: str


class VerifyRequest(BaseModel):
    signed_payload: dict


app = FastAPI(title="JEJAK PKI Registry")


@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception as exc:
        print(f"WARNING: database initialization failed: {exc}")


def check_rate_limit(key: str) -> bool:
    now = time.time()
    arr = RATE_LIMIT.get(key, [])
    # drop old
    arr = [t for t in arr if now - t < RATE_LIMIT_WINDOW]
    if len(arr) >= RATE_LIMIT_MAX:
        RATE_LIMIT[key] = arr
        return False
    arr.append(now)
    RATE_LIMIT[key] = arr
    return True


def require_api_key(request: Request):
    if not API_KEY:
        return True
    key = request.headers.get("x-api-key") or request.query_params.get("api_key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")
    return True


@app.post("/register-key")
def register_key(payload: RegisterKey, request: Request, auth: bool = Depends(require_api_key)):
    try:
        # rate limit per remote addr
        client_ip = request.client.host if request.client else "unknown"
        if not check_rate_limit(client_ip):
            raise HTTPException(status_code=429, detail="rate limit exceeded")
        conn = get_db()
        c = conn.cursor()
        if USE_POSTGRES:
            c.execute(
                "INSERT INTO publishers(publisher_id, public_key, created_at) VALUES (%s, %s, %s) ON CONFLICT (publisher_id) DO UPDATE SET public_key = EXCLUDED.public_key, created_at = EXCLUDED.created_at",
                (payload.publisher_id, payload.public_key_base64, datetime.utcnow().isoformat() + "Z"),
            )
        else:
            c.execute(
                "INSERT OR REPLACE INTO publishers(publisher_id, public_key, created_at) VALUES (?, ?, ?)",
                (payload.publisher_id, payload.public_key_base64, datetime.utcnow().isoformat() + "Z"),
            )
        conn.commit()
        conn.close()
        return {"ok": True, "publisher_id": payload.publisher_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/key/{publisher_id}")
def get_key(publisher_id: str):
    conn = get_db()
    c = conn.cursor()
    if USE_POSTGRES:
        c.execute("SELECT public_key FROM publishers WHERE publisher_id=%s", (publisher_id,))
        row = c.fetchone()
        # psycopg2 returns tuple by default
        pub = row[0] if row else None
    else:
        c.execute("SELECT public_key FROM publishers WHERE publisher_id=?", (publisher_id,))
        row = c.fetchone()
        pub = row[0] if row else None
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="publisher not found")
    return {"publisher_id": publisher_id, "public_key_base64": pub}


@app.post("/verify")
def verify(req: VerifyRequest):
    signed_payload = req.signed_payload
    publisher = signed_payload.get("publisher_id") or signed_payload.get("publisher")
    if not publisher:
        raise HTTPException(status_code=400, detail="publisher_id missing")

    conn = get_db()
    c = conn.cursor()
    if USE_POSTGRES:
        c.execute("SELECT public_key FROM publishers WHERE publisher_id=%s", (publisher,))
        row = c.fetchone()
        pub_key = row[0] if row else None
    else:
        c.execute("SELECT public_key FROM publishers WHERE publisher_id=?", (publisher,))
        row = c.fetchone()
        pub_key = row[0] if row else None
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="publisher not found")
    # lazy import of verifier to reuse core implementation
    try:
        from Coding.core.crypto import DocumentVerifier

        verifier = DocumentVerifier(pub_key)
        ok = verifier.verify_payload(signed_payload)
    except Exception:
        ok = False

    # store audit
    doc_id = signed_payload.get("doc_id")
    recipient_id = signed_payload.get("recipient_id")
    if USE_POSTGRES:
        c.execute(
            "INSERT INTO audit(timestamp,publisher_id,doc_id,recipient_id,result,raw_payload) VALUES(%s,%s,%s,%s,%s,%s)",
            (datetime.utcnow().isoformat() + "Z", publisher, doc_id, recipient_id, "valid" if ok else "invalid", json.dumps(signed_payload)),
        )
    else:
        c.execute(
            "INSERT INTO audit(timestamp,publisher_id,doc_id,recipient_id,result,raw_payload) VALUES(?,?,?,?,?,?)",
            (datetime.utcnow().isoformat() + "Z", publisher, doc_id, recipient_id, "valid" if ok else "invalid", json.dumps(signed_payload)),
        )
    conn.commit()
    conn.close()

    # metrics
    if HAS_PROM:
        if ok:
            METRIC_VERIFY_OK.inc()
        else:
            METRIC_VERIFY_FAIL.inc()

    return {"valid": ok}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    # basic readiness: db file exists and tables accessible
    try:
        conn = get_db()
        c = conn.cursor()
        if USE_POSTGRES:
            c.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE tablename IN ('publishers','audit')")
            rows = c.fetchall()
            ok = len(rows) >= 2
        else:
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('publishers','audit')")
            rows = c.fetchall()
            ok = len(rows) >= 2
        conn.close()
        return {"ready": ok}
    except Exception:
        return {"ready": False}


@app.get("/debug/core-path")
def debug_core_path():
    try:
        import Coding.core.crypto as cc
        return {"core_crypto_file": getattr(cc, '__file__', None)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/metrics")
def metrics():
    if not HAS_PROM:
        raise HTTPException(status_code=404, detail="metrics not enabled")
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
