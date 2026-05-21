import json
import qrcode
from PIL import Image

class PayloadEncoder:
    @staticmethod
    def encode_payload_to_qr(signed_payload: dict, output_path: str = "output_qr.png"):
        """
        Mengubah signed payload JSON menjadi QR Code gambar.
        Menggunakan Error Correction tingkat tinggi (H - 30%) agar 
        tetap bisa dibaca meskipun tercetak dengan buruk atau kotor.
        """
        # Konversi dict ke string JSON yang padat (hilangkan spasi)
        payload_str = json.dumps(signed_payload, separators=(',', ':'))
        
        # Setup QR code
        qr = qrcode.QRCode(
            version=None, # Auto-size tergantung panjang data
            error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction (tahan banting)
            box_size=10,
            border=4,
        )
        
        qr.add_data(payload_str)
        qr.make(fit=True)
        
        # Buat image (Hitam Putih)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        return output_path
