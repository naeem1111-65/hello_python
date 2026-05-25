# Link Downloader

A small Python/Kivy mobile-style app for downloading videos from links that yt-dlp supports, including many public YouTube and Facebook video links.

Use it only for videos you own, videos you created, or content you have permission to save. It does not bypass DRM, private pages, paywalls, or platform access controls.

## Run on Windows for testing

```powershell
cd tools\link_downloader_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Build an Android APK

Buildozer works best on Linux or WSL, not directly on Windows PowerShell.

```bash
cd tools/link_downloader_app
python3 -m pip install --user buildozer
buildozer android debug
```

The APK will be created under `bin/`. Install it on your Android phone, paste a video link, press `Check Link`, choose an option, then press `Download`.

## Download options

- `Best MP4`: best available single file with audio and video when possible.
- `Small MP4`: smaller single file with audio and video when possible.
- `Audio M4A`: downloads the best audio stream without converting it.

The app avoids requiring ffmpeg by default. That keeps the Android build simpler, but it also means some sites may not provide every quality as one merged file.
