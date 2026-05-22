# JEJAK

JEJAK adalah platform forensik dokumen untuk menyisipkan fingerprint ke dokumen cetak, memverifikasi keaslian, dan membantu pelacakan kebocoran dokumen.

## Isi Repositori

- `Coding/` - kode utama, termasuk demo end-to-end
- `CONCEPT/` - spesifikasi dan catatan konsep
- `PROGRESS/` - log progres, issue, dan tracker pekerjaan

## Quick Start

Install dependensi Python:

```powershell
python -m pip install -r Coding/requirements.txt
```

Jalankan demo end-to-end:

```powershell
python Coding/demo_e2e.py
```

Output demo:

- `Coding/demo_signed.pdf`
- `Coding/demo_output_qr.png`
- `Coding/demo_signed_payload.json`

## Deploy Backend ke Render

Backend FastAPI ada di `backend/` dan sudah siap dipakai sebagai Web Service di Render.

Langkah cepat:

1. Buat Web Service baru di Render.
2. Hubungkan repo ini.
3. Set `Root Directory` ke `backend` jika Anda deploy dari repo utama.
4. Set environment variable:
	- `DATABASE_URL` = connection string Supabase/Postgres Anda
	- `API_KEY` = opsional, untuk mengunci endpoint `POST /register-key`
5. Gunakan Dockerfile di `backend/Dockerfile`.

Health check endpoint:

```text
/health
```

Readiness endpoint:

```text
/ready
```

Jika `health` sudah `ok` tapi `ready` masih `false`, biasanya masalahnya ada di koneksi database atau network access ke Supabase.

## Logging Progres

Catatan progres dan issue disimpan di folder `PROGRESS/`.

- `PROGRESS/progress_log.md` - kronologis progres
- `PROGRESS/issues.md` - daftar issue dan status solusi
- `PROGRESS/cli_log.py` - CLI sederhana untuk menambahkan entri

Contoh menambah progres:

```powershell
python PROGRESS/cli_log.py progress --author dev --title "Demo E2E" --status done --description "Demo berhasil dijalankan" --files "Coding/demo_e2e.py"
```

## GitHub

Repo ini menggunakan SSH untuk push/pull ke GitHub.

```powershell
ssh -T git@github.com
git remote -v
```

## Catatan Pengembangan

File sensitif seperti key privat, `.env`, dan artefak build sudah diabaikan melalui `.gitignore`.
