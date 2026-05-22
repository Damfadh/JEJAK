from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime
import json

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, "pki.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
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
    init_db()


@app.post("/register-key")
def register_key(payload: RegisterKey):
    try:
        conn = get_db()
        c = conn.cursor()
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
    c.execute("SELECT public_key FROM publishers WHERE publisher_id=?", (publisher_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="publisher not found")
    return {"publisher_id": publisher_id, "public_key_base64": row[0]}


@app.post("/verify")
def verify(req: VerifyRequest):
    signed_payload = req.signed_payload
    publisher = signed_payload.get("publisher_id") or signed_payload.get("publisher")
    if not publisher:
        raise HTTPException(status_code=400, detail="publisher_id missing")

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT public_key FROM publishers WHERE publisher_id=?", (publisher,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="publisher not found")

    pub_key = row[0]
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
    c.execute(
        "INSERT INTO audit(timestamp,publisher_id,doc_id,recipient_id,result,raw_payload) VALUES(?,?,?,?,?,?)",
        (datetime.utcnow().isoformat() + "Z", publisher, doc_id, recipient_id, "valid" if ok else "invalid", json.dumps(signed_payload)),
    )
    conn.commit()
    conn.close()

    return {"valid": ok}


@app.get("/debug/core-path")
def debug_core_path():
    try:
        import Coding.core.crypto as cc
        return {"core_crypto_file": getattr(cc, '__file__', None)}
    except Exception as e:
        return {"error": str(e)}
