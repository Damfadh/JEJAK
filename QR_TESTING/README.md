# QR Testing

Folder ini berisi contoh QR untuk uji scan di HP.

Isi:
- `sample_payload.json` — payload signed contoh.
- `sample_qr_plain.png` — QR hitam biasa untuk baseline scan.
- `sample_qr_halftone.png` — QR halftone yang lebih samar untuk uji mode utama JEJAK.
- `sample_qr_detectable.png` — QR halftone yang lebih kuat untuk cek deteksi kamera.
- `generate_sample_qr.py` — script pembuat sample QR.

Cara pakai cepat:

```bash
cd QR_TESTING
python generate_sample_qr.py
```

Setelah file dibuat, buka app mobile JEJAK lalu:
- isi `API Base URL` bila ingin verifikasi ke backend
- tekan `Scan From Image`
- pilih `sample_qr_detectable.png` dulu kalau kamera masih sulit mendeteksi
- kalau sudah terbaca, coba `sample_qr_halftone.png` untuk mode stealth

Catatan:
- QR ini dibuat sebagai contoh testing, bukan dokumen produksi.
- Jika ingin verifikasi valid, register public key yang dipakai script ini ke backend JEJAK terlebih dahulu.
- Jika QR halftone terlalu samar, naikkan brightness layar atau gunakan file `sample_qr_detectable.png` sebagai baseline.