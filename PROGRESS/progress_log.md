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


