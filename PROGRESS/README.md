# PROGRESS — JEJAK

Tujuan: menyimpan catatan progres, masalah, dan solusi untuk proyek JEJAK.

Panduan singkat:
- Catat setiap perubahan, sekecil apa pun, di `progress_log.md`.
- Untuk setiap masalah, tambahkan entri di `issues.md` dan update ketika selesai beserta penjelasan solusinya.
- Gunakan format yang ada di template untuk konsistensi.

File penting:
- `progress_log.md` — kronologis kegiatan dan milestones.
- `issues.md` — daftar masalah, status, dan solusi.
- `template_entry.md` — template untuk membuat entri baru.

Contoh singkat penulisan entri di `progress_log.md`:

```
2026-05-21 | @nama | Created PROGRESS folder and initial tracker | status: done
- Keterangan: Membuat folder PROGRESS dan file README, progress_log, issues.
- Next: Tambahkan entri harian saat implementasi.
```

Jaga agar catatan singkat, jelas, dan selalu sertakan tanggal serta siapa yang membuat entri.

Current status highlights:
- Day 3: Batch signing CLI — in progress. Added `scripts/batch_sign.py` and `tests/test_batch_sign.py` (basic ZIP output and verification).

Usage example (Day 3):

```bash
# Generate a new key and sign CSV into out.zip
python scripts/batch_sign.py --csv tests/fixtures/sample_batch.csv --out out.zip --gen-key-out key.b64

# Use an existing private key (base64 file) and add prefix to filenames inside the ZIP
python scripts/batch_sign.py --csv tests/fixtures/sample_batch.csv --private-key-base64-file key.b64 --out signed.zip --prefix signed_
```

Sample fixture: `tests/fixtures/sample_batch.csv`.

CI artifact:

The CI workflow `day3-batch.yml` runs tests and produces `sample_signed.zip` (uploaded as a GitHub Actions artifact named `sample_signed_zip`). Use this artifact to preview signed payloads.

Day 4 (Compose demo)
---------------------

Added a multi-service compose demo in `docker-compose.yml` with services:
- `postgres` — Postgres database
- `backend` — JEJAK backend
- `signer` — demo signer that runs `scripts/batch_sign.py` against `tests/fixtures/sample_batch.csv` and writes artifacts to `./artifacts`

Run the demo locally:

```bash
docker-compose up --build
```

Artifacts will be available in the repository `./artifacts` folder as `sample_signed.zip` and `ci_key.b64`.

To stop after signer completes and exit: use

```bash
docker-compose up --build --abort-on-container-exit
```
