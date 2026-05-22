# Progress Log — JEJAK

Gunakan format ini untuk setiap entri (baris baru untuk entry baru):

Format:
`YYYY-MM-DD | @author | Short title | status: (open|in-progress|done)`

Detail: Jelaskan perubahan, file yang diubah, dan langkah selanjutnya.

---

2026-05-21 | @team | Create PROGRESS folder and initial tracker | status: done
- Files added: `README.md`, `progress_log.md`, `issues.md`, `template_entry.md`
- Keterangan: Folder dibuat untuk merekam semua progres dan issue. Template disediakan.
- Next: Setiap progress harian harus dicatat di sini.

2026-05-21 | @assistant | Connect to GitHub remote https://github.com/Damfadh/JEJAK.git | status: in-progress
- Keterangan: Perintah `git init`, `git add`, dan `git commit` berhasil secara lokal. Percobaan `git push` menemukan bahwa remote berisi commit lain dan meminta autentikasi.
- Output singkat: push ditolak (remote contains work) dan autentikasi perlu diselesaikan di browser.
- Next: Jalankan `git pull --rebase origin main` untuk menggabungkan perubahan remote, selesaikan konflik jika ada, lalu `git push`. Jika autentikasi diperlukan, lakukan `gh auth login` atau gunakan personal access token.


2026-05-21 | @assistant | Push to GitHub remote | status: done

- Deskripsi: Pulled remote, rebased, and pushed local commits to https://github.com/Damfadh/JEJAK.git
- Files changed: PROGRESS/progress_log.md
- Next steps: Continue Day 1 tasks and build demo script

2026-05-21 | @dev | Start E2E demo | status: in-progress

- Deskripsi: Begin end-to-end demo flow

2026-05-21 | @dev | Generate keypair | status: done

- Deskripsi: Generated signing keypair and exported public key
- Files changed: I:\Project\Jejak\Coding\demo_key_public.b64.txt
- Next steps: Create dummy PDF and sign payload

2026-05-21 | @dev | Create dummy PDF | status: done

- Deskripsi: Created dummy PDF for demo
- Files changed: I:\Project\Jejak\Coding\dummy_rahasia_demo.pdf
- Next steps: Sign payload and generate QR

2026-05-21 | @dev | Sign payload | status: done

- Deskripsi: Signed payload and saved to file
- Files changed: I:\Project\Jejak\Coding\demo_signed_payload.json
- Next steps: Generate QR image from payload

2026-05-21 | @dev | Generate QR | status: done

- Deskripsi: Generated QR image from signed payload
- Files changed: I:\Project\Jejak\Coding\demo_output_qr.png
- Next steps: Embed QR into PDF

2026-05-21 | @dev | Embed QR into PDF | status: done

- Deskripsi: Embedded QR into PDF and saved signed PDF
- Files changed: I:\Project\Jejak\Coding\demo_signed.pdf
- Next steps: Verify payload locally

2026-05-21 | @dev | Verify payload | status: done

- Deskripsi: Verification OK
- Next steps: Prepare demo artifacts and README

2026-05-21 | @assistant | Commit demo files; push failed | status: in-progress

- Deskripsi: Committed Coding/demo_e2e.py and PROGRESS/__init__.py locally, but git push returned 403 Permission denied.
- Files changed: Coding/demo_e2e.py, PROGRESS/__init__.py
- Next steps: Authenticate with GitHub (gh auth login) or configure PAT, then push origin main

2026-05-21 | @assistant | Push via SSH succeeded | status: done

- Deskripsi: Verified ssh -T git@github.com and pushed local commits to git@github.com:Damfadh/JEJAK.git
- Files changed: Coding/demo_e2e.py, PROGRESS/__init__.py, PROGRESS/progress_log.md
- Next steps: Continue Day 2: minimal backend PKI API

2026-05-21 | @dev | Start E2E demo | status: in-progress

- Deskripsi: Begin end-to-end demo flow

2026-05-21 | @dev | Generate keypair | status: done

- Deskripsi: Generated signing keypair and exported public key
- Files changed: I:\Project\Jejak\Coding\demo_key_public.b64.txt
- Next steps: Create dummy PDF and sign payload

2026-05-21 | @dev | Create dummy PDF | status: done

- Deskripsi: Created dummy PDF for demo
- Files changed: I:\Project\Jejak\Coding\dummy_rahasia_demo.pdf
- Next steps: Sign payload and generate QR

2026-05-21 | @dev | Sign payload | status: done

- Deskripsi: Signed payload and saved to file
- Files changed: I:\Project\Jejak\Coding\demo_signed_payload.json
- Next steps: Generate QR image from payload

2026-05-21 | @dev | Generate QR | status: done

- Deskripsi: Generated QR image from signed payload
- Files changed: I:\Project\Jejak\Coding\demo_output_qr.png
- Next steps: Embed QR into PDF

2026-05-21 | @dev | Embed QR into PDF | status: done

- Deskripsi: Embedded QR into PDF and saved signed PDF
- Files changed: I:\Project\Jejak\Coding\demo_signed.pdf
- Next steps: Verify payload locally

2026-05-21 | @dev | Verify payload | status: done

- Deskripsi: Verification OK
- Next steps: Prepare demo artifacts and README

2026-05-21 | @assistant | Add README, env example, and CI workflow | status: done

- Deskripsi: Added a fuller root README, .env.example template, and GitHub Actions workflow to run demo E2E on push/PR.
- Files changed: README.md, .env.example, .github/workflows/python-ci.yml
- Next steps: Continue Day 2: backend PKI API

2026-05-21 | @assistant | Start Day 2: Backend PKI API | status: in-progress

- Deskripsi: Scaffold FastAPI backend (backend/app.py) with endpoints for register key, get key, and verify; added backend README and requirements.
- Files changed: backend/app.py, backend/requirements.txt, backend/README.md
- Next steps: Install backend deps and run uvicorn for manual testing

2026-05-22 | @dev | Start E2E demo | status: in-progress

- Deskripsi: Begin end-to-end demo flow

2026-05-22 | @dev | Generate keypair | status: done

- Deskripsi: Generated signing keypair and exported public key
- Files changed: I:\Project\Jejak\Coding\demo_key_public.b64.txt
- Next steps: Create dummy PDF and sign payload

2026-05-22 | @dev | Create dummy PDF | status: done

- Deskripsi: Created dummy PDF for demo
- Files changed: I:\Project\Jejak\Coding\dummy_rahasia_demo.pdf
- Next steps: Sign payload and generate QR

2026-05-22 | @dev | Sign payload | status: done

- Deskripsi: Signed payload and saved to file
- Files changed: I:\Project\Jejak\Coding\demo_signed_payload.json
- Next steps: Generate QR image from payload

2026-05-22 | @dev | Generate Halftone QR | status: done

- Deskripsi: Generated near-invisible halftone QR image from signed payload
- Files changed: I:\Project\Jejak\Coding\demo_output_qr_halftone.png
- Next steps: Embed QR into PDF

2026-05-22 | @dev | Embed Halftone QR into PDF | status: done

- Deskripsi: Embedded near-invisible QR into PDF and saved signed PDF
- Files changed: I:\Project\Jejak\Coding\demo_signed.pdf
- Next steps: Verify payload locally

2026-05-22 | @dev | Verify payload | status: done

- Deskripsi: Verification OK
- Next steps: Prepare demo artifacts and README

2026-05-22 | @assistant | Add mobile consent gate and APK v1 | status: done

- Deskripsi: Added startup consent gate to the mobile app, required camera/backend/data consent before scanning, rebuilt APK, and saved a new versioned release artifact.
- Files changed: mobile/www/index.html, mobile/www/app.js, mobile/android/app/src/main/AndroidManifest.xml, mobile/README.md, Releases/jejak-v1.apk
- Next steps: Continue improving QR scan reliability and create additional test samples if needed.

2026-05-22 | @assistant | Create QR testing folder and samples | status: done

- Deskripsi: Added dedicated `QR_TESTING` folder with sample payload JSON, plain QR, halftone QR, and a more detectable QR sample for scan debugging.
- Files changed: QR_TESTING/README.md, QR_TESTING/generate_sample_qr.py, QR_TESTING/sample_payload.json, QR_TESTING/sample_public_key.b64.txt, QR_TESTING/sample_qr_plain.png, QR_TESTING/sample_qr_halftone.png, QR_TESTING/sample_qr_detectable.png
- Next steps: Use the detectable sample to validate scanner behavior on device, then tune halftone parameters if needed.

2026-05-22 | @assistant | Improve QR detection robustness | status: done

- Deskripsi: Updated the mobile scanner to preprocess frames with multiple thresholds before `jsQR`, improving detection of faint QR/halftone images.
- Files changed: mobile/www/app.js
- Next steps: If detection is still flaky on some phones, consider a stronger scanner engine or slightly less aggressive halftone settings.

