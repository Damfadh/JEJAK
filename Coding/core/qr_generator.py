import json
import qrcode
from PIL import Image, ImageDraw

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

    @staticmethod
    def encode_payload_to_halftone_qr(
        signed_payload: dict,
        output_path: str = "output_qr_halftone.png",
        dot_scale: float = 0.42,
        gray_level: int = 245,
        alpha: int = 58,
        box_size: int = 10,
        border: int = 4,
    ):
        """
        Membuat QR halftone dengan titik sangat terang + transparansi,
        agar sulit dilihat kasat mata di atas kertas putih namun tetap
        memiliki struktur QR untuk proses scan yang baik.
        """
        payload_str = json.dumps(signed_payload, separators=(',', ':'))

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(payload_str)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        modules = len(matrix)
        size = modules * box_size

        # Transparan agar menyatu dengan background dokumen.
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        dot = max(1, int(box_size * dot_scale))
        pad = (box_size - dot) // 2

        # Titik lingkaran halftone untuk setiap modul hitam.
        for r, row in enumerate(matrix):
            y0 = r * box_size + pad
            y1 = y0 + dot
            for c, val in enumerate(row):
                if not val:
                    continue
                x0 = c * box_size + pad
                x1 = x0 + dot
                draw.ellipse((x0, y0, x1, y1), fill=(gray_level, gray_level, gray_level, alpha))

        img.save(output_path)
        return output_path
