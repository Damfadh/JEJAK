# Issues — JEJAK

Catat setiap masalah, status, siapa yang menindaklanjuti, dan ringkasan solusi ketika diselesaikan.

Format entri:

```
ID: ISSUE-001
Tanggal: 2026-05-21
Pelapor: @nama
Judul: Short description
Status: open | in-progress | resolved
Prioritas: P0 | P1 | P2
Deskripsi: Detail masalah
Langkah reproduksi: 1) ... 2) ...
Assigned: @nama
Solusi: (isi saat resolved)
Komentar: ...
```

Contoh:

ID: ISSUE-001
Tanggal: 2026-05-21
Pelapor: @team
Judul: Create PROGRESS folder
Status: resolved
Prioritas: P2
Deskripsi: Menambahkan folder PROGRESS untuk tracking
Langkah reproduksi: N/A
Assigned: @team
Solusi: Folder dan file template dibuat pada 2026-05-21
Komentar: -

ID: ISSUE-SSH-001
Tanggal: 2026-05-21
Pelapor: @assistant
Judul: SSH public key not registered on GitHub
Status: resolved
Prioritas: P1
Deskripsi: Local SSH key exists at %USERPROFILE%\\.ssh\\id_ed25519, but ssh -T git@github.com returns 'Permission denied (publickey)'.
Langkah reproduksi: 1) Add local public key to GitHub 2) Retry ssh -T 3) Switch git remote to SSH if needed
Assigned: @assistant
Solusi: SSH public key was added to GitHub Settings > SSH and GPG keys. `ssh -T git@github.com` then returned the success message and git push over SSH succeeded.
Komentar: Public key content has been extracted and is ready to be pasted into GitHub Settings > SSH and GPG keys.

