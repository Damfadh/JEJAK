import tempfile
import zipfile
import json
import os
import base64

from Coding.core.crypto import DocumentSigner, DocumentVerifier

from scripts.batch_sign import sign_batch


def test_sign_batch_creates_zip(tmp_path):
    csv_content = "doc_id,recipient_id,publisher_id,meta\n" + "docA,rec1,pub1,hello\n" + "docB,rec2,pub1,world\n"
    csv_file = tmp_path / "in.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # generate a key
    signer = DocumentSigner()
    priv_bytes = signer.get_private_key_bytes()
    pub_b64 = signer.get_public_key_base64()

    out_zip = tmp_path / "out.zip"
    zip_path, returned_pub = sign_batch(str(csv_file), priv_bytes, str(out_zip))

    assert os.path.exists(zip_path)
    assert returned_pub == pub_b64

    # inspect zip
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert "docA.json" in namelist
        assert "docB.json" in namelist

        for name in namelist:
            data = zf.read(name).decode("utf-8")
            obj = json.loads(data)
            assert "signature" in obj

            # verify signature
            verifier = DocumentVerifier(pub_b64)
            assert verifier.verify_payload(obj)
