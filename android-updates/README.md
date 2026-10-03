# JARVIS Android Auto-Update

- version.json stores the latest published version metadata.
- APK files should be attached to GitHub Releases.
- The Android app must check versionCode, download the APK over HTTPS, verify SHA-256, and request installation through Android's package installer.
- Keep the existing signing key unchanged for compatible updates.
