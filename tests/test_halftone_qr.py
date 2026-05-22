import os

from Coding.core.crypto import DocumentSigner
from Coding.core.qr_generator import PayloadEncoder
from Coding.core.pdf_manipulator import PDFEncoder


def test_halftone_qr_and_embed_to_pdf(tmp_path):
    signer = DocumentSigner()
    payload = signer.create_payload(doc_id="DOC-HF-001", recipient_id="RECIPIENT-HF", publisher_id="PUB-HF")
    signed_payload, _ = signer.sign_payload(payload)

    qr_path = tmp_path / "hf_qr.png"
    out_qr = PayloadEncoder.encode_payload_to_halftone_qr(signed_payload, output_path=str(qr_path))
    assert os.path.exists(out_qr)

    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    PDFEncoder.create_dummy_pdf(str(input_pdf))
    PDFEncoder.embed_halftone_qr_to_pdf(str(input_pdf), str(qr_path), str(output_pdf))

    assert output_pdf.exists()
    assert output_pdf.stat().st_size > 0
