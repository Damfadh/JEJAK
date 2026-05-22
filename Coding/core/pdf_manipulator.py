import fitz  # PyMuPDF
import os

class PDFEncoder:
    @staticmethod
    def embed_qr_to_pdf(
        input_pdf_path: str,
        qr_image_path: str,
        output_pdf_path: str,
        qr_size: int = 70,
        margin: int = 30,
    ):
        """
        Menyisipkan gambar QR Code ke halaman pertama PDF pada posisi pojok kanan bawah.
        """
        # Buka dokumen PDF input
        doc = fitz.open(input_pdf_path)
        
        if len(doc) == 0:
            raise ValueError("PDF tidak memiliki halaman")
            
        page = doc[0]  # Ambil halaman pertama
        
        # Ambil dimensi halaman (points)
        rect = page.rect
        
        # Ukuran dan margin bisa dituning sesuai kebutuhan visibilitas/scanability
        
        # Hitung koordinat pojok kanan bawah (x0, y0, x1, y1)
        x0 = rect.width - qr_size - margin
        y0 = rect.height - qr_size - margin
        x1 = rect.width - margin
        y1 = rect.height - margin
        
        image_rect = fitz.Rect(x0, y0, x1, y1)
        
        # Sisipkan gambar QR Code
        page.insert_image(image_rect, filename=qr_image_path)
        
        # Simpan ke file baru
        doc.save(output_pdf_path)
        doc.close()
        
        return output_pdf_path
        
    @staticmethod
    def create_dummy_pdf(output_path: str):
        """Membuat PDF dummy rahasia untuk keperluan testing."""
        doc = fitz.open()
        page = doc.new_page()
        
        # Tambahkan teks
        page.insert_text((50, 50), "DOKUMEN RAHASIA KEMENTERIAN XYZ", fontsize=20, color=(0.8, 0, 0))
        page.insert_text((50, 90), "Dokumen ini bersifat konfidensial dan hanya diperuntukkan", fontsize=12)
        page.insert_text((50, 110), "kepada penerima yang sah.", fontsize=12)
        page.insert_text((50, 150), "Segala bentuk penggandaan tanpa izin adalah pelanggaran hukum.", fontsize=12)
        
        doc.save(output_path)
        doc.close()
        return output_path

    @staticmethod
    def embed_halftone_qr_to_pdf(
        input_pdf_path: str,
        qr_image_path: str,
        output_pdf_path: str,
        qr_size: int = 72,
        margin: int = 28,
    ):
        """
        Menyisipkan QR halftone (PNG transparan) agar nyaris tidak terlihat.
        Gunakan bersama `encode_payload_to_halftone_qr`.
        """
        return PDFEncoder.embed_qr_to_pdf(
            input_pdf_path=input_pdf_path,
            qr_image_path=qr_image_path,
            output_pdf_path=output_pdf_path,
            qr_size=qr_size,
            margin=margin,
        )
