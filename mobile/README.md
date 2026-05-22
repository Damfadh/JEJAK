# JEJAK Mobile PWA

This folder contains a minimal PWA that scans QR codes using the device camera and calls the backend `POST /verify` endpoint with the scanned payload.

Local dev

Install dependencies and run local PWA server:

```bash
cd mobile
npm install
npm run start
```

Open `http://localhost:4173` and set:
- API Base URL: `http://127.0.0.1:8000` (or backend URL)
- API Key: optional, only if backend requires `x-api-key`

Scanner modes:
- Camera live scan
- Image upload fallback (`Scan From Image`) for difficult halftone QR captures

Startup consent

When the app opens for the first time, it will ask for consent before enabling the scanner. The consent covers:
- camera access for scanning
- sending scanned payloads to the JEJAK backend for verification
- storing API configuration locally on the device
- using the app only for authorized documents

If consent is declined, the scanner remains locked.

Capacitor (Android)

To create the Android scaffold locally (already added in the repo for CI):

```bash
npx cap init "JEJAK Scanner" id.co.jejak.app --web-dir=www
npx cap add android
npx cap sync android
```

Quick commands after first setup:

```bash
npm run cap:sync
npm run cap:open
```

Open Android Studio: `npx cap open android` and build/sign there, or rely on our CI workflow which can build an APK when the `android/` folder exists and the signing secrets are configured.

CI notes

The workflow `.github/workflows/pwa-android-build.yml` will build the PWA and attempt to build an APK if `android/` is present. To enable signing, add the secrets described in `docs/ANDROID_SIGNING.md`.
