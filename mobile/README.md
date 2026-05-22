# JEJAK Mobile PWA

This folder contains a minimal PWA that scans QR codes using the device camera and calls the backend `POST /verify` endpoint with the scanned payload.

Local dev

Install dependencies and serve the `mobile/www` folder:

```bash
cd mobile
npm install
npm run start
```

Capacitor (Android)

To create the Android scaffold locally (already added in the repo for CI):

```bash
npx cap init "JEJAK Scanner" id.co.jejak.app --web-dir=www
npx cap add android
npx cap sync android
```

Open Android Studio: `npx cap open android` and build/sign there, or rely on our CI workflow which can build an APK when the `android/` folder exists and the signing secrets are configured.

CI notes

The workflow `.github/workflows/pwa-android-build.yml` will build the PWA and attempt to build an APK if `android/` is present. To enable signing, add the secrets described in `docs/ANDROID_SIGNING.md`.
