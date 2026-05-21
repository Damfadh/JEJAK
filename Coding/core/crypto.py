import json
import base64
from datetime import datetime
from typing import Dict, Any, Tuple
import nacl.signing
import nacl.encoding

class DocumentSigner:
    def __init__(self, private_key_bytes: bytes = None):
        """
        Inisialisasi DocumentSigner. 
        Jika private_key_bytes tidak diberikan, akan membuat kunci baru.
        """
        if private_key_bytes:
            self.signing_key = nacl.signing.SigningKey(private_key_bytes)
        else:
            self.signing_key = nacl.signing.SigningKey.generate()
            
        self.verify_key = self.signing_key.verify_key

    def get_public_key_base64(self) -> str:
        """Mendapatkan public key dalam format Base64"""
        return self.verify_key.encode(encoder=nacl.encoding.Base64Encoder).decode('utf-8')

    def get_private_key_bytes(self) -> bytes:
        """Mendapatkan private key bytes untuk disimpan"""
        return bytes(self.signing_key)

    def create_payload(self, doc_id: str, recipient_id: str, publisher_id: str) -> Dict[str, Any]:
        """Membuat struktur dasar payload"""
        return {
            "version": "1.0",
            "doc_id": doc_id,
            "publisher_id": publisher_id,
            "recipient_id": recipient_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def sign_payload(self, payload: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        """
        Menandatangani payload JSON.
        Mengembalikan tuple (payload_yang_ditandatangani, signature_base64)
        """
        # Serialize payload to string consistently (no spaces, sorted keys)
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        payload_bytes = payload_str.encode('utf-8')
        
        # Sign the bytes
        signed = self.signing_key.sign(payload_bytes)
        
        # Get signature in base64
        signature_b64 = base64.b64encode(signed.signature).decode('utf-8')
        
        # Add signature to payload
        signed_payload = payload.copy()
        signed_payload["signature"] = signature_b64
        
        return signed_payload, signature_b64

class DocumentVerifier:
    def __init__(self, public_key_base64: str):
        """Inisialisasi verifier dengan public key (dari registry/database)"""
        pub_key_bytes = base64.b64decode(public_key_base64)
        self.verify_key = nacl.signing.VerifyKey(pub_key_bytes)

    def verify_payload(self, signed_payload: Dict[str, Any]) -> bool:
        """
        Memverifikasi payload yang memiliki signature.
        """
        try:
            # Extract signature
            if "signature" not in signed_payload:
                return False
                
            signature_b64 = signed_payload["signature"]
            signature_bytes = base64.b64decode(signature_b64)
            
            # Remove signature to recreate original payload string
            payload_copy = signed_payload.copy()
            del payload_copy["signature"]
            
            payload_str = json.dumps(payload_copy, sort_keys=True, separators=(',', ':'))
            payload_bytes = payload_str.encode('utf-8')
            
            # Verify
            self.verify_key.verify(payload_bytes, signature_bytes)
            return True
        except (nacl.exceptions.BadSignatureError, Exception):
            return False
