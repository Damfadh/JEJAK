"""Batch signing CLI.

Reads a CSV with headers: doc_id,recipient_id,publisher_id[,any other columns]
For each row creates a payload via `DocumentSigner.create_payload`, merges extra columns into payload,
signs it and writes a JSON file into a ZIP archive.

Usage: python scripts/batch_sign.py --csv input.csv --private-key-base64-file key.b64 --out out.zip
"""
import csv
import json
import base64
from pathlib import Path
import argparse
import zipfile
from typing import Optional

from Coding.core.crypto import DocumentSigner


def sign_batch(csv_path: str, private_key_bytes: bytes, out_zip: str, prefix: str = ""):
    csv_p = Path(csv_path)
    out_p = Path(out_zip)
    signer = DocumentSigner(private_key_bytes=private_key_bytes)

    with zipfile.ZipFile(out_p, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        with csv_p.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for i, row in enumerate(reader):
                doc_id = row.get("doc_id") or row.get("id") or f"doc-{i}"
                recipient_id = row.get("recipient_id") or row.get("recipient") or ""
                publisher_id = row.get("publisher_id") or row.get("publisher") or ""

                payload = signer.create_payload(doc_id=doc_id, recipient_id=recipient_id, publisher_id=publisher_id)

                # merge any extra columns
                for k, v in row.items():
                    if k in ("doc_id", "recipient_id", "publisher_id", "id", "recipient", "publisher"):
                        continue
                    payload[k] = v

                signed_payload, signature = signer.sign_payload(payload)

                filename = f"{prefix}{doc_id}.json"
                zf.writestr(filename, json.dumps(signed_payload, ensure_ascii=False))

    return str(out_p), signer.get_public_key_base64()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--private-key-base64-file", required=False)
    parser.add_argument("--out", required=True, help="Output zip filename")
    parser.add_argument("--out-dir", required=False, help="Directory to write output zip into")
    parser.add_argument("--prefix", required=False, default="", help="Prefix to add to filenames inside zip")
    parser.add_argument("--gen-key-out", required=False, help="Write generated private key base64 to this file")

    args = parser.parse_args()

    if args.private_key_base64_file:
        kb = Path(args.private_key_base64_file).read_text(encoding="utf-8").strip()
        private_key_bytes = base64.b64decode(kb)
    else:
        signer = DocumentSigner()
        private_key_bytes = signer.get_private_key_bytes()
        if args.gen_key_out:
            Path(args.gen_key_out).write_text(base64.b64encode(private_key_bytes).decode("utf-8"), encoding="utf-8")

    # determine out path
    out_path = Path(args.out)
    if args.out_dir:
        out_path = Path(args.out_dir) / out_path

    out_zip, pub_b64 = sign_batch(args.csv, private_key_bytes, str(out_path), prefix=args.prefix)
    print(f"Wrote {out_zip}")
    print(f"Public key (base64): {pub_b64}")


if __name__ == "__main__":
    main()
