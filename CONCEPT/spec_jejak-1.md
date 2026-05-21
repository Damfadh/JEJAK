# Spesifikasi Teknis: JEJAK
**Document Forensics & Print Steganography Platform**

**Submission**: WRECK-IT 7.0 Hackathon 2026
**Kategori**: Hackathon General
**Tema**: Cyber Warfare — Silent War on The Fifth Domain

---

## Ringkasan Eksekutif

JEJAK adalah platform forensik dokumen pertama di Indonesia yang menggabungkan steganografi cetak dengan kriptografi modern. Setiap salinan dokumen yang dicetak menerima sidik unik tak terlihat yang tahan terhadap fotokopi, scan, dan foto. Aplikasi mobile companion memungkinkan verifikasi keaslian dan pelacakan asal-usul dokumen hanya dengan memotret.

**Tagline**: *Setiap Cetakan Punya Cerita*

**Problem statement**: Indonesia tidak memiliki infrastruktur untuk melacak kebocoran dokumen rahasia, memverifikasi keaslian sertifikat fisik, atau melawan pembajakan buku terbitan. Tools komersial seperti Digimarc tidak ada di Indonesia, mahal, dan proprietary.

**Solusi**: Platform open-source yang memadukan print-resilient steganography, signature digital, dan mobile reader app untuk forensik dokumen end-to-end.

---

## Daftar Isi

1. [Latar Belakang & Justifikasi](#1-latar-belakang)
2. [Use Cases & Stakeholder](#2-use-cases)
3. [Arsitektur Sistem](#3-arsitektur-sistem)
4. [Komponen Encoder](#4-encoder)
5. [Komponen Mobile Decoder](#5-mobile-decoder)
6. [Komponen Cryptographic Layer](#6-cryptographic-layer)
7. [Komponen Backend & Audit](#7-backend)
8. [Spesifikasi Steganografi](#8-steganografi)
9. [User Experience Flow](#9-ux-flow)
10. [Tech Stack](#10-tech-stack)
11. [Roadmap Pengembangan](#11-roadmap)
12. [Metrik Keberhasilan](#12-metrik)
13. [Risiko & Mitigasi](#13-risiko)

---

## 1. Latar Belakang

### Konteks Masalah di Indonesia

Indonesia menghadapi tiga tantangan dokumen yang saling terkait:

**Kebocoran Dokumen Rahasia**
- Dokumen kementerian sering bocor ke media tanpa cara melacak sumber
- Tidak ada infrastruktur forensik untuk attribution
- Whistleblower investigation tidak ter-streamline

**Pemalsuan Sertifikat & Ijazah**
- Industri pemalsuan ijazah adalah masalah kronis
- Verifikasi manual lambat dan tidak scalable
- Tidak ada sistem nasional terpadu

**Pembajakan Buku & Hak Kekayaan Intelektual**
- Industri penerbitan kehilangan triliunan rupiah karena pembajakan
- Foto buku dengan HP kemudian disebar PDF
- Penerbit tidak punya cara trace ke siapa yang mem-foto

### Gap di Ekosistem Indonesia

| Aspek | Kondisi Saat Ini | Gap |
|---|---|---|
| Tracking dokumen rahasia | Manual log book | Tidak forensik, tidak scalable |
| Verifikasi sertifikat | Manual stamp check | Tidak otomatis, mudah dipalsukan |
| Anti-pembajakan buku | DRM digital saja | Tidak cover print copies |
| Tools komersial | Digimarc (US, mahal) | Tidak ada di Indonesia, proprietary |
| Open source | Tidak ada equivalent | Total greenfield |

### Justifikasi WRECK-IT 7.0

Information warfare adalah komponen utama "Silent War on The Fifth Domain". Dokumen yang bocor adalah amunisi paling powerful dalam information warfare. JEJAK memberikan kemampuan attribution & verification yang selama ini tidak dimiliki Indonesia.

---

## 2. Use Cases & Stakeholder

### Use Case 1: Dokumen Pemerintah Rahasia 🏛️

**Skenario**: Kementerian distribusikan dokumen rahasia ke 50 staff. Dokumen bocor ke media.

**Solusi JEJAK**:
1. Setiap copy dicetak dengan unique fingerprint (staff ID + timestamp)
2. Saat dokumen bocor, foto dokumen → JEJAK identify sumber dalam detik
3. Audit trail menunjukkan kapan dokumen diakses & dicetak

**Stakeholder**: BSSN, Kemkominfo, Setneg, Kemhan, Kemlu

### Use Case 2: Anti-Pembajakan Buku 📚

**Skenario**: Penerbit luncurkan novel best-seller. Setelah 1 minggu, PDF beredar di Telegram.

**Solusi JEJAK**:
1. Setiap eksemplar buku punya unique embedded ID per copy
2. Saat PDF bajakan beredar, ambil foto → identify yang scan/foto
3. Penerbit punya legal evidence untuk pursue case

**Stakeholder**: Gramedia, Mizan, IKAPI, penulis independen

### Use Case 3: Verifikasi Ijazah & Sertifikat 🎓

**Skenario**: HRD perusahaan terima 100 ijazah pelamar, perlu verify cepat.

**Solusi JEJAK**:
1. Foto ijazah dengan aplikasi JEJAK
2. Aplikasi extract embedded data + verify signature universitas
3. Hasil: "ASLI - Diterbitkan oleh UI pada 2024-06-15 untuk [nama]"

**Stakeholder**: Kemendikbud-Ristek, kampus, perusahaan rekrutmen, BNSP

### Use Case 4: Akta & Dokumen Hukum 📋

**Skenario**: Notaris perlu prove keaslian akta dalam dispute hukum.

**Solusi JEJAK**:
1. Setiap akta yang dikeluarkan disisipkan crypto signature
2. Pengadilan/pihak terkait foto akta dengan JEJAK
3. Verifikasi instan: asli atau dipalsukan

**Stakeholder**: Ikatan Notaris Indonesia (INI), Kementerian ATR/BPN, Mahkamah Agung

### Use Case 5: Tiket & Boarding Pass Cetak 🎫

**Skenario**: Promotor konser khawatir tiket palsu.

**Solusi JEJAK**:
1. Setiap tiket cetak punya unique ID + signature
2. Petugas pintu masuk scan dengan JEJAK
3. Real-time validation tanpa internet (cache mode)

**Stakeholder**: Promotor konser (Java Festival, Synchronize), Garuda Indonesia, KAI

---

## 3. Arsitektur Sistem

```
┌──────────────────────────────────────────────────────────┐
│                    JEJAK PLATFORM                          │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  [PUBLISHER SIDE]                                          │
│  ┌────────────────────────────────────────────────┐       │
│  │  Web Dashboard / CLI / SDK                      │       │
│  │       ↓                                         │       │
│  │  Document Signer                                │       │
│  │  - Generate unique copy_id per recipient        │       │
│  │  - Sign with publisher private key (Ed25519)    │       │
│  │       ↓                                         │       │
│  │  Steganography Encoder                          │       │
│  │  - Embed payload via halftone modulation        │       │
│  │  - Add micro-QR backup layer                    │       │
│  │       ↓                                         │       │
│  │  PDF Output (signed_copy.pdf)                   │       │
│  │       ↓                                         │       │
│  │  Print → Physical Document                      │       │
│  └────────────────────────────────────────────────┘       │
│                            ↓                               │
│                   [PHYSICAL WORLD]                         │
│                   Document distributed                     │
│                            ↓                               │
│  [VERIFIER SIDE]                                           │
│  ┌────────────────────────────────────────────────┐       │
│  │  Mobile App (Android/iOS)                       │       │
│  │       ↓                                         │       │
│  │  Camera Capture                                 │       │
│  │       ↓                                         │       │
│  │  Image Preprocessing                            │       │
│  │  - Deskew, denoise, perspective correction     │       │
│  │       ↓                                         │       │
│  │  Steganography Decoder                          │       │
│  │  - Extract halftone pattern                     │       │
│  │  - Fallback: micro-QR detection                 │       │
│  │       ↓                                         │       │
│  │  Signature Verification                         │       │
│  │  - Fetch public key from registry              │       │
│  │  - Verify Ed25519 signature                     │       │
│  │       ↓                                         │       │
│  │  Result Display                                 │       │
│  │  ✅ ASLI - [metadata]                          │       │
│  └────────────────────────────────────────────────┘       │
│                            ↓                               │
│  [BACKEND]                                                 │
│  ┌────────────────────────────────────────────────┐       │
│  │  PostgreSQL: Document registry                  │       │
│  │  Redis: Cache untuk fast lookup                 │       │
│  │  Public Key Infrastructure (PKI)                │       │
│  │  Audit Log: Setiap verifikasi tercatat         │       │
│  │  REST API + GraphQL                             │       │
│  └────────────────────────────────────────────────┘       │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Komponen Encoder

### Fungsi Utama

Encoder adalah library Python/Rust yang mengambil PDF input dan menghasilkan PDF output dengan steganografi tersisip per copy.

### API Sederhana

```python
from jejak import DocumentSigner, Encoder

# Initialize publisher (sekali setup)
signer = DocumentSigner.from_keyfile("publisher_private.key")

# Encode per recipient
encoder = Encoder(signer=signer)

encoded_pdf = encoder.embed(
    pdf_input="dokumen_rahasia.pdf",
    payload={
        "doc_id": "DOC-2026-001",
        "recipient_id": "STAFF-4471",
        "recipient_name": "Budi Santoso",
        "timestamp": "2026-05-04T14:30:00+07:00",
        "publisher": "Kementerian XYZ",
        "classification": "RAHASIA"
    }
)

encoded_pdf.save("dokumen_rahasia_budi.pdf")
```

### Mode Encoding

| Mode | Karakteristik | Use Case |
|---|---|---|
| **Stealth** | Halftone only, totally invisible | Dokumen rahasia |
| **Hybrid** | Halftone + micro-QR (gold ink) | Sertifikat resmi |
| **Visible** | Watermark visible + hidden layer | Buku, anti-pembajakan |
| **Forensic** | Multiple redundant layers | High-stakes documents |

### Batch Processing

Untuk publisher yang distribute ke ribuan recipient:

```python
encoder.batch_embed(
    pdf_template="ijazah_template.pdf",
    recipients_csv="lulusan_2026.csv",
    output_dir="./ijazah_signed/",
    parallel_workers=8
)
# Output: ribuan PDF signed dalam beberapa menit
```

### Web Dashboard untuk Non-Developer

Untuk publisher yang tidak bisa coding:
- Upload PDF template
- Upload CSV recipient list
- Click "Generate Signed Copies"
- Download ZIP berisi semua signed PDFs

---

## 5. Komponen Mobile Decoder

### Aplikasi Mobile

**Platform target**: Android (primary), iOS (secondary)

### Capture Flow

```
1. User buka aplikasi JEJAK
2. Tap tombol "Verifikasi Dokumen"
3. Camera viewfinder muncul
4. Auto-detect document edges (real-time)
5. Capture saat dokumen terdeteksi
6. Tampilkan progress: "Memproses... 67%"
7. Display result dengan metadata
```

### Image Preprocessing Pipeline

```python
def preprocess_image(raw_capture):
    # 1. Detect & correct perspective
    corners = detect_document_corners(raw_capture)
    deskewed = perspective_correction(raw_capture, corners)
    
    # 2. Denoise
    denoised = bilateral_filter(deskewed)
    
    # 3. Normalize lighting
    normalized = adaptive_histogram_equalization(denoised)
    
    # 4. Resolution check
    if resolution < MIN_DPI_FOR_DECODING:
        raise InsufficientResolutionError()
    
    return normalized
```

### Decoder Algorithm

**Tahap 1**: Coba decode halftone steganography
- Apply DCT (Discrete Cosine Transform)
- Extract bits dari frequency domain
- Reed-Solomon error correction

**Tahap 2**: Fallback ke micro-QR
- Locate micro-QR position (typical: corner)
- Decode QR content
- Use as primary if halftone failed

**Tahap 3**: Verification
- Fetch public key dari registry (atau cached)
- Verify Ed25519 signature
- Display result

### Result Display

```
╔════════════════════════════════════════╗
║          ✅ DOKUMEN ASLI                ║
╠════════════════════════════════════════╣
║                                          ║
║  Penerbit  : Kementerian XYZ            ║
║  Doc ID    : DOC-2026-001               ║
║  Untuk     : Budi Santoso (STAFF-4471) ║
║  Tanggal   : 4 Mei 2026, 14:30 WIB     ║
║  Klasifikasi: RAHASIA                   ║
║                                          ║
║  🔐 Tanda Tangan: VALID                 ║
║  📊 Confidence : 98.2%                  ║
║                                          ║
║  [Lihat Detail]  [Laporkan]            ║
║                                          ║
╚════════════════════════════════════════╝
```

### Offline-First Capability

- Cache public keys popular publishers
- Verifikasi tanpa internet untuk dokumen common
- Sync audit log saat online

---

## 6. Komponen Cryptographic Layer

### Algoritma Pilihan

| Komponen | Algoritma | Alasan |
|---|---|---|
| **Signature** | Ed25519 | Modern, fast, kecil (64 byte) |
| **Hashing** | BLAKE3 | Lebih cepat dari SHA-256 |
| **Symmetric** | ChaCha20-Poly1305 | Untuk encrypted payload (optional) |
| **Key derivation** | Argon2id | Password-based key generation |

### Key Management

**Publisher Key Lifecycle**:
1. **Generate**: Ed25519 keypair on secure device
2. **Distribute public key**: Via PKI registry atau blockchain
3. **Store private key**: HSM atau encrypted file dengan Argon2
4. **Rotation**: Setiap 1-2 tahun, dengan grace period

**Public Key Distribution**:

```
Option A: Centralized PKI Registry (default)
- Backend JEJAK menyimpan public keys
- API endpoint: GET /api/v1/publisher/{publisher_id}/key
- Cached di mobile app

Option B: Blockchain Anchor (enterprise)
- Public key di-commit ke Ethereum/Polygon
- Tamper-proof, decentralized verification
- Lebih mahal tapi lebih trustless

Option C: DNS-based (lightweight)
- Public key di-publish via DNS TXT record
- Mirror Web of Trust model
```

### Payload Format

```json
{
  "version": "1.0",
  "doc_id": "uuid-v4",
  "publisher_id": "publisher-uuid",
  "recipient_id": "uuid-or-hashed-id",
  "timestamp": "ISO-8601",
  "metadata": {
    "title_hash": "blake3-hash",
    "page_count": 10,
    "classification": "PUBLIC|INTERNAL|CONFIDENTIAL|SECRET"
  },
  "signature": "ed25519-sig-base64"
}
```

Total: ~256-512 bytes setelah compression. Cukup untuk distribute via halftone steganography.

---

## 7. Komponen Backend & Audit

### Database Schema

**Publishers Table**
```sql
CREATE TABLE publishers (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    public_key BYTEA NOT NULL,
    domain VARCHAR(255) UNIQUE,
    verification_status ENUM('verified', 'pending', 'revoked'),
    created_at TIMESTAMP,
    metadata JSONB
);
```

**Documents Table**
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    publisher_id UUID REFERENCES publishers(id),
    title_hash CHAR(64),
    classification VARCHAR(20),
    total_copies_generated INT DEFAULT 0,
    created_at TIMESTAMP
);
```

**Document_Copies Table**
```sql
CREATE TABLE document_copies (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    recipient_id_hash CHAR(64),
    payload BYTEA,
    signature BYTEA,
    created_at TIMESTAMP,
    UNIQUE(document_id, recipient_id_hash)
);
```

**Verifications Audit Table**
```sql
CREATE TABLE verifications (
    id UUID PRIMARY KEY,
    document_copy_id UUID REFERENCES document_copies(id),
    verified_at TIMESTAMP,
    verifier_app_id VARCHAR(255),
    geo_country VARCHAR(2), -- privacy-preserving
    result ENUM('valid', 'invalid', 'unknown'),
    metadata JSONB
);
```

### REST API Endpoints

```
[Publisher Management]
POST   /api/v1/publisher/register
GET    /api/v1/publisher/{id}
GET    /api/v1/publisher/{id}/public-key
PUT    /api/v1/publisher/{id}/rotate-key

[Document Operations]
POST   /api/v1/document/sign        # Server-side signing (optional)
GET    /api/v1/document/{id}
GET    /api/v1/document/{id}/copies # Audit list

[Verification]
POST   /api/v1/verify               # Mobile app endpoint
GET    /api/v1/verify/history       # User's verification history

[Forensics]
POST   /api/v1/forensics/trace-leak # Identify leaked copy
GET    /api/v1/forensics/audit/{document_id}
```

### Audit Trail Features

- Setiap verifikasi tercatat (tanpa PII)
- Anomaly detection: copy yang verified excessive bisa indikasi leak
- Heatmap geografis verifikasi
- Export untuk legal proceeding

---

## 8. Spesifikasi Steganografi

### Tantangan Print-Resilient Steganography

Berbeda dengan steganografi digital biasa, JEJAK harus survive:

1. **Print process**: Toner dispersion, paper texture
2. **Photocopy**: Multiple generations of copying
3. **Photo capture**: Lens distortion, lighting variation, JPEG compression
4. **Aging**: Paper yellowing, folding, smudges

### Approach: Multi-Layer Hybrid

**Layer 1: Halftone Modulation (Primary)**
- Modulasi pola dot di area teks/gambar
- Domain: frequency (DCT)
- Robust terhadap print-scan-photo
- Tidak terlihat mata telanjang
- Capacity: 256-1024 bits per A4 page

**Layer 2: Geometric Glyph Variation (Secondary)**
- Karakter tertentu pakai font variant yang sangat mirip
- Setiap karakter encode 1-2 bits
- Survive OCR dengan baik
- Backup jika halftone rusak

**Layer 3: Micro-QR Code (Fallback)**
- QR code 1cm x 1cm di sudut dokumen
- Tinta gold/silver (semi-invisible di kertas warna)
- Last resort jika layer 1 & 2 gagal
- Capacity: hingga 4KB

### Error Correction

**Reed-Solomon Code (255, 223)**:
- Bisa recover sampai 16 byte error per 255 byte
- Sufficient untuk handle print noise
- Industry standard

**Redundant Encoding**:
- Payload encoded 3x di posisi berbeda
- Majority voting saat decode
- Survival rate >95% bahkan dengan 30% bit error

### Robustness Targets

| Skenario | Decode Success Target |
|---|---|
| Print + foto langsung | >98% |
| Print + 1x fotokopi + foto | >85% |
| Print + 3x fotokopi + foto | >70% |
| Print + scanner 300 DPI | >95% |
| Print + foto malam dengan flash | >75% |
| Print + foto outdoor terang | >90% |

---

## 9. User Experience Flow

### Publisher Flow (Web Dashboard)

```
1. Login ke dashboard JEJAK
   ↓
2. Klik "New Document"
   ↓
3. Upload PDF template
   ↓
4. Pilih klasifikasi (PUBLIC/INTERNAL/CONFIDENTIAL/SECRET)
   ↓
5. Upload CSV recipient list (atau input manual)
   ↓
6. Pilih encoding mode (Stealth/Hybrid/Visible/Forensic)
   ↓
7. Klik "Generate Signed Copies"
   ↓
8. Download ZIP dengan PDF per recipient
   ↓
9. (Optional) Print langsung dengan PrinterCloud integration
```

### Verifier Flow (Mobile App)

```
1. Buka aplikasi JEJAK
   ↓
2. Tap "Verifikasi Dokumen"
   ↓
3. Arahkan kamera ke dokumen
   ↓
4. Auto-detect & capture
   ↓
5. Tunggu processing (~3 detik)
   ↓
6. Lihat result:
   - ✅ ASLI + metadata, atau
   - ⚠️ TIDAK DIKENALI (no embedded data)
   - ❌ INVALID (tampered or fake)
   ↓
7. (Optional) Save ke history
   ↓
8. (Optional) Report jika suspicious
```

### Forensics Flow (Investigator)

```
1. Dapat foto/PDF dokumen yang bocor
   ↓
2. Login ke JEJAK Forensics Console
   ↓
3. Upload foto/PDF
   ↓
4. Sistem extract embedded payload
   ↓
5. Cross-reference dengan database
   ↓
6. Tampilkan:
   - Original publisher
   - Copy ID yang bocor
   - Recipient ID yang assigned
   - Timeline access dokumen
   ↓
7. Generate forensics report (PDF)
   ↓
8. (Optional) Submit sebagai evidence ke pihak berwenang
```

---

## 10. Tech Stack

### Backend

| Layer | Tech |
|---|---|
| **Language** | Rust (encoder), Python (orchestration), Go (API) |
| **Framework** | FastAPI (Python) atau Axum (Rust) |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **Object Storage** | MinIO atau S3-compatible |
| **Queue** | Celery + Redis (Python) atau native (Rust) |

### Mobile

| Platform | Tech |
|---|---|
| **Android** | Kotlin + Jetpack Compose |
| **iOS** | Swift + SwiftUI |
| **Cross-platform alternative** | Flutter (jika tim lebih familiar) |
| **Image processing** | OpenCV native, ML Kit |
| **Crypto** | libsodium |

### Web Dashboard

| Layer | Tech |
|---|---|
| **Frontend** | React + TypeScript + Vite |
| **State** | Zustand atau Redux Toolkit |
| **UI Library** | Shadcn/ui + Tailwind CSS |
| **Charts** | Recharts |
| **PDF Preview** | PDF.js |

### Crypto & Steganography Libraries

| Library | Purpose |
|---|---|
| **libsodium** | Ed25519, BLAKE3 |
| **OpenCV** | Image processing |
| **Pillow / Imagemagick** | PDF manipulation |
| **Stegano (Python)** | Reference implementation |
| **Custom halftone library** | Core innovation (build ourselves) |

### DevOps

| Need | Tool |
|---|---|
| **Container** | Docker + Docker Compose |
| **Orchestration** | Kubernetes (production) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Prometheus + Grafana |
| **Logging** | Loki |

---

## 11. Roadmap Pengembangan

### Hackathon Phase (Mei-Juli 2026)

**Minggu 1**: Riset literatur, prototype encoder dengan micro-QR
**Minggu 2**: Implement Ed25519 signature, mobile app skeleton
**Minggu 3**: Implement halftone steganography (basic)
**Minggu 4**: Backend API, web dashboard MVP
**Minggu 5**: End-to-end integration, testing
**Minggu 6**: Demo prep, video recording, submission

### Post-Hackathon Roadmap

**v1.0 (Hackathon Release)**
- Stealth mode + Hybrid mode
- Mobile app Android only
- Single publisher key support
- Manual key management

**v1.1 (Q3 2026)**
- iOS app launch
- Multi-publisher support
- Web dashboard polish
- Public key registry public API

**v2.0 (Q4 2026)**
- Visible & Forensic modes
- Batch processing 10K+ docs
- Enterprise SSO integration
- Advanced forensics dashboard

**v3.0 (2027)**
- Blockchain anchor option
- Multi-language UI (English, regional Indonesia)
- White-label SDK untuk integrasi pihak ke-3
- Compliance certifications (ISO 27001)

---

## 12. Metrik Keberhasilan

### Metrik Hackathon (Demo Quality)

- ✅ Encoder mampu sign 100 dokumen dalam <60 detik
- ✅ Mobile app decode rate >85% dalam controlled lighting
- ✅ Crypto signature verification 100% reliable
- ✅ Backend API <200ms response time
- ✅ Demo end-to-end <3 menit dari capture ke verify

### Metrik Adopsi (6 Bulan)

- 🎯 5+ publisher trial (kampus, penerbit kecil)
- 🎯 1.000+ dokumen ter-sign
- 🎯 100+ verifikasi via mobile app
- 🎯 1+ partnership dengan kementerian
- 🎯 Open source contributors: 10+

### Metrik Dampak (1 Tahun)

- 🎯 1+ kementerian pakai untuk dokumen rahasia
- 🎯 1+ penerbit besar (Gramedia tier) trial
- 🎯 100K+ dokumen ter-sign
- 🎯 Zero false positive critical
- 🎯 Recognition dari BSSN/Kominfo

---

## 13. Risiko & Mitigasi

| Risiko | Probabilitas | Dampak | Mitigasi |
|---|:---:|:---:|---|
| Halftone steganography tidak robust | Tinggi | Sangat Tinggi | Fallback micro-QR sebagai layer kedua |
| Mobile decode lambat | Sedang | Tinggi | Native libraries (OpenCV C++), GPU compute |
| Demo gagal saat presentasi | Sedang | Sangat Tinggi | Pre-recorded video backup, controlled lighting setup |
| PKI infrastructure complexity | Tinggi | Sedang | Start centralized, blockchain v2 |
| Adoption resistance ("why bother?") | Tinggi | Sedang | Jelas use cases ROI, pilot dengan early adopter |
| Legal/compliance issues | Rendah | Tinggi | Konsultasi UU PDP, opt-in untuk recipient hashing |
| Performance pada printer murah | Sedang | Sedang | Test multiple printer brands, document compatibility |
| Riset PhD-level dalam 41 hari | Tinggi | Tinggi | Scope down ke micro-QR + simple halftone, advanced di v2 |

---

## 14. Tim & Peran

### Komposisi Tim Optimal (5 orang)

| Peran | Tanggung Jawab | Skill yang Dibutuhkan |
|---|---|---|
| **Lead/Crypto Engineer** | Architecture, signature layer, koordinasi | Cryptography, Rust/Go |
| **CV/ML Engineer** | Steganography encoder & decoder | OpenCV, image processing, ML |
| **Mobile Developer** | Android/iOS app | Kotlin/Swift, mobile CV |
| **Backend/Web Developer** | API, dashboard, database | Python/Go, React |
| **Product/Pitch** | UX, proposal, video, presentation | Design thinking, communication |

### Skill Gap Assessment

Skill yang harus ada di tim:
- ✅ Cryptography (paling kritis)
- ✅ Computer Vision / Image Processing
- ✅ Mobile development (minimal Android)
- ✅ Backend development
- ✅ Public speaking untuk pitch

---

## 15. Anggaran Estimasi

### Development & Testing

| Item | Cost (IDR) |
|---|---:|
| Cloud hosting (AWS/GCP credits) | 0 (free tier) |
| Domain jejak.id | 200.000/tahun |
| Test printers (akses) | 0 (pakai office) |
| Various paper types untuk testing | 100.000 |
| Test devices (HP Android variations) | 0 (own devices) |
| **Subtotal Dev** | **300.000** |

### Production Video & Pitch

| Item | Cost |
|---|---:|
| Microphone | 350.000 |
| Lighting | 200.000 |
| Mockup props (sample documents) | 100.000 |
| **Subtotal Production** | **650.000** |

### Total Anggaran: **~Rp 950.000**

---

## 16. Pertimbangan Etika & Privasi

### Privasi by Design

- **Recipient ID hashed**: Tidak simpan PII langsung, hash dengan salt
- **Verifier anonymous**: Tidak track siapa yang verify
- **Audit minimal**: Hanya track event, tidak konten
- **Right to be forgotten**: Recipient bisa request data deletion

### Dual-Use Consideration

JEJAK bisa di-misuse untuk:
- Surveillance internal (employer track employee)
- Stalking (track distribution dokumen)

**Mitigasi**:
- Documentation jelas tentang use case yang acceptable
- Default opt-in dengan informed consent
- License clause melarang surveillance use

### Compliance

- **UU Perlindungan Data Pribadi (UU PDP)**: Compliance mandatory
- **GDPR**: Compliance untuk publisher internasional
- **ISO 27001**: Target certification untuk enterprise tier

---

## 17. Lampiran: Sample Workflow

### Skenario: Kementerian Distribusikan Dokumen Rahasia

```
[Hari 1, 09:00 WIB]
Sekjen perlu distribute briefing rahasia ke 50 staff
↓
[09:15] Login ke JEJAK Publisher Dashboard
↓
[09:20] Upload "Briefing-2026-Q2.pdf"
       Pilih klasifikasi: RAHASIA
       Upload CSV staff list (50 orang)
       Pilih mode: Stealth (full invisible)
↓
[09:25] Click "Generate" → Sistem buat 50 signed PDFs
↓
[09:30] Download ZIP → Print di kantor secure
↓
[10:00] Distribusikan ke 50 staff
↓
[Hari 5] Dokumen muncul di Twitter, viral
↓
[Hari 5, 14:00] Tim investigasi foto dokumen Twitter
              dengan JEJAK Forensics
↓
[14:01] Sistem identify: Copy ID 4471, 
        assigned to "Staff X" pada Hari 1
↓
[14:30] Internal investigation focused
↓
[Hari 6] Whistleblower / leaker identified
```

---

## Penutup

JEJAK adalah jawaban Indonesia untuk tantangan information warfare di era digital. Dengan menggabungkan steganografi cetak yang advanced, kriptografi modern, dan mobile-first verification, kami memberikan kemampuan attribution dan verification yang selama ini hanya dimiliki negara maju.

**Setiap cetakan punya cerita. JEJAK membantu Anda membaca cerita itu.**

---

**Repository**: github.com/[your-team]/jejak  
**Lisensi**: MIT License  
**Kontak**: [team email]  
**Submission**: WRECK-IT 7.0 Hackathon 2026
