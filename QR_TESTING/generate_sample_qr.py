import base64
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Coding.core.crypto import DocumentSigner, DocumentVerifier
from Coding.core.qr_generator import PayloadEncoder


OUT_DIR = Path(__file__).resolve().parent


def main():
    signer = DocumentSigner()
    payload = signer.create_payload(
        doc_id="QR-TEST-001",
        recipient_id="RECIPIENT-TEST",
        publisher_id="PUBLISHER-TEST",
    )
    payload["purpose"] = "QR testing for JEJAK mobile scanner"
    signed_payload, _signature = signer.sign_payload(payload)

    sample_json = OUT_DIR / "sample_payload.json"
    sample_json.write_text(json.dumps(signed_payload, indent=2), encoding="utf-8")

    plain_qr = OUT_DIR / "sample_qr_plain.png"
    halftone_qr = OUT_DIR / "sample_qr_halftone.png"
    detect_qr = OUT_DIR / "sample_qr_detectable.png"

    PayloadEncoder.encode_payload_to_qr(signed_payload, output_path=str(plain_qr))
    PayloadEncoder.encode_payload_to_halftone_qr(signed_payload, output_path=str(halftone_qr))
    PayloadEncoder.encode_payload_to_halftone_qr(
        signed_payload,
        output_path=str(detect_qr),
        dot_scale=0.62,
        gray_level=220,
        alpha=130,
        box_size=12,
    )

    pub_b64 = signer.get_public_key_base64()
    pub_file = OUT_DIR / "sample_public_key.b64.txt"
    pub_file.write_text(pub_b64, encoding="utf-8")

    verify_ok = DocumentVerifier(pub_b64).verify_payload(signed_payload)

    print(f"Wrote: {sample_json}")
    print(f"Wrote: {plain_qr}")
    print(f"Wrote: {halftone_qr}")
    print(f"Wrote: {detect_qr}")
    print(f"Wrote: {pub_file}")
    print(f"Local signature verify: {verify_ok}")


if __name__ == "__main__":
    main()
