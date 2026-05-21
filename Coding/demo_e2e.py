import os
import sys
import json
from datetime import datetime

# Ensure project root is on sys.path so PROGRESS package is importable
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from core.crypto import DocumentSigner, DocumentVerifier
    from core.qr_generator import PayloadEncoder
    from core.pdf_manipulator import PDFEncoder
except Exception:
    print("Missing required modules. Make sure you installed requirements in Coding/requirements.txt")
    raise

from PROGRESS.log_helper import append_progress_entry


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
OUTPUT_DIR = ROOT


def log_step(author: str, title: str, status: str, description: str = "", files_changed=None, next_steps: str = ""):
    append_progress_entry(author=author, title=title, status=status, description=description, files_changed=files_changed or [], next_steps=next_steps)


def main():
    author = "dev"
    log_step(author, "Start E2E demo", "in-progress", "Begin end-to-end demo flow")

    signer = DocumentSigner()
    pub_b64 = signer.get_public_key_base64()
    priv_bytes = signer.get_private_key_bytes()

    key_info_file = os.path.join(OUTPUT_DIR, "demo_key_public.b64.txt")
    with open(key_info_file, "w", encoding="utf-8") as f:
        f.write(pub_b64)

    log_step(author, "Generate keypair", "done", "Generated signing keypair and exported public key", files_changed=[key_info_file], next_steps="Create dummy PDF and sign payload")

    # Create dummy PDF
    dummy_pdf = os.path.join(OUTPUT_DIR, "dummy_rahasia_demo.pdf")
    PDFEncoder.create_dummy_pdf(dummy_pdf)
    log_step(author, "Create dummy PDF", "done", "Created dummy PDF for demo", files_changed=[dummy_pdf], next_steps="Sign payload and generate QR")

    # Prepare payload
    payload = signer.create_payload(doc_id="DOC-DEMO-001", recipient_id="RECIPIENT-123", publisher_id="DEMO-PUBLISHER")
    signed_payload, signature = signer.sign_payload(payload)

    payload_file = os.path.join(OUTPUT_DIR, "demo_signed_payload.json")
    with open(payload_file, "w", encoding="utf-8") as f:
        json.dump(signed_payload, f, indent=2)

    log_step(author, "Sign payload", "done", "Signed payload and saved to file", files_changed=[payload_file], next_steps="Generate QR image from payload")

    # Generate QR
    qr_path = os.path.join(OUTPUT_DIR, "demo_output_qr.png")
    PayloadEncoder.encode_payload_to_qr(signed_payload, output_path=qr_path)
    log_step(author, "Generate QR", "done", "Generated QR image from signed payload", files_changed=[qr_path], next_steps="Embed QR into PDF")

    # Embed QR into PDF
    signed_pdf = os.path.join(OUTPUT_DIR, "demo_signed.pdf")
    PDFEncoder.embed_qr_to_pdf(dummy_pdf, qr_path, signed_pdf)
    log_step(author, "Embed QR into PDF", "done", "Embedded QR into PDF and saved signed PDF", files_changed=[signed_pdf], next_steps="Verify payload locally")

    # Verify locally using public key
    verifier = DocumentVerifier(pub_b64)
    # read back payload
    with open(payload_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    ok = verifier.verify_payload(loaded)
    status_text = "done" if ok else "open"
    detail = "Verification OK" if ok else "Verification FAILED"

    log_step(author, "Verify payload", status_text, detail, files_changed=[], next_steps="Prepare demo artifacts and README")

    print("E2E demo finished. Signed PDF:", signed_pdf)
    print("QR image:", qr_path)
    print("Payload file:", payload_file)


if __name__ == "__main__":
    main()
