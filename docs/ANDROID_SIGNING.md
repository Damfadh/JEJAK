# Android APK signing (CI)

This document explains how to provide a signing keystore to GitHub Actions so the CI can produce a signed APK.

Secrets required (set in your repository Settings → Secrets):
- `ANDROID_KEYSTORE` — the JKS keystore file, base64-encoded (no newlines). Example: `base64 keystore.jks | tr -d '\n'` and copy the output.
- `ANDROID_KEYSTORE_PASSWORD` — the keystore password.
- `ANDROID_KEY_ALIAS` — the key alias inside the keystore.
- `ANDROID_KEY_PASSWORD` — the key password (often same as keystore password).

CI behavior
- The workflow `.github/workflows/pwa-android-build.yml` will:
  - decode `ANDROID_KEYSTORE` and write it to `android/keystore/keystore.jks` if present;
  - append `RELEASE_*` entries to `android/gradle.properties` for Gradle to pick up signing config;
  - run `./gradlew assembleRelease` to build the APK.

How to generate a keystore locally (example):

```bash
keytool -genkeypair -v -keystore release-keystore.jks -alias mykeyalias -keyalg RSA -keysize 2048 -validity 10000
```

Then create base64 string:

```bash
base64 release-keystore.jks | tr -d '\n' > keystore.b64.txt
```

Copy the contents of `keystore.b64.txt` into the `ANDROID_KEYSTORE` secret. Add the other secrets accordingly.

Security notes
- Keep keystore secrets private. Do not commit keystore files to the repository.
- Prefer using GitHub Actions `secrets` and required repository-level protection.
