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
