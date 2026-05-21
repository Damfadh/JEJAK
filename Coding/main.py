import json
from core.crypto import DocumentSigner, DocumentVerifier
from core.qr_generator import PayloadEncoder
from core.pdf_manipulator import PDFEncoder

def run_crypto_test():
    print("=== JEJAK Cryptography Layer Test ===\n")
    
    # 1. Publisher generates keys
    print("[1] Publisher setup...")
    signer = DocumentSigner()
    pub_key = signer.get_public_key_base64()
    print(f"Public Key: {pub_key}")
    
    # 2. Publisher creates a document copy for a recipient
    print("\n[2] Creating document payload for recipient...")
    payload = signer.create_payload(
        doc_id="DOC-2026-001",
        recipient_id="STAFF-4471",
        publisher_id="KEMEN-XYZ-01"
    )
    print("Raw Payload:", json.dumps(payload, indent=2))
    
    # 3. Publisher signs the payload
    print("\n[3] Signing the payload...")
    signed_payload, sig = signer.sign_payload(payload)
    print("Signature:", sig)
    print("Signed Payload:", json.dumps(signed_payload, indent=2))
    
    # 4. Verifier (Mobile App) checks the payload
    print("\n[4] Verifier checks the signature...")
    verifier = DocumentVerifier(pub_key)
    is_valid = verifier.verify_payload(signed_payload)
    
    if is_valid:
        print("[SUCCESS] VERIFICATION SUCCESS: The document payload is authentic and untampered.")
    else:
        print("[FAILED] VERIFICATION FAILED: The document payload is invalid.")
        
    # 5. Tampering test
    print("\n[5] Tampering Test (Simulating hacker changing recipient ID)...")
    tampered_payload = signed_payload.copy()
    tampered_payload["recipient_id"] = "HACKER-9999"
    
    is_valid_tampered = verifier.verify_payload(tampered_payload)
    if is_valid_tampered:
        print("[FAILED] ERROR: Tampered payload was accepted!")
    else:
        print("[SUCCESS] TAMPER DETECTION SUCCESS: Tampered payload was correctly rejected.")

    # 6. Generate QR Code
    print("\n[6] Generating QR Code from signed payload...")
    qr_path = "test_qr.png"
    PayloadEncoder.encode_payload_to_qr(signed_payload, qr_path)
    print(f"[SUCCESS] QR Code successfully generated and saved to: {qr_path}")

    # 7. Embed QR to PDF
    print("\n[7] Embedding QR Code into PDF...")
    dummy_pdf_path = "dummy_rahasia.pdf"
    output_pdf_path = "dokumen_terproteksi_jejak.pdf"
    
    # Buat PDF dummy jika belum ada
    print("    -> Membuat dummy PDF mentah...")
    PDFEncoder.create_dummy_pdf(dummy_pdf_path)
    
    # Sisipkan QR
    print("    -> Menyisipkan QR Code ke PDF...")
    PDFEncoder.embed_qr_to_pdf(dummy_pdf_path, qr_path, output_pdf_path)
    print(f"[SUCCESS] PDF Akhir (dengan Stegano Layer) berhasil disimpan di: {output_pdf_path}")

if __name__ == "__main__":
    run_crypto_test()
