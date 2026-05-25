# Get An Installable APK Link

This project already has a GitHub Actions APK builder. If you upload the full `CODEER` folder as a repository, use the workflow at `.github/workflows/link-downloader-android.yml`.

## Option 1: Build APK on GitHub

1. Upload this folder/repository to GitHub.
2. Open the repository on GitHub.
3. Go to `Actions`.
4. Select `Build Android APK`.
5. Press `Run workflow`.
6. When it finishes, open the finished run.
7. Download the artifact named `link-downloader-apk`.
8. Extract the zip and send the `.apk` file to your phone.
9. On Android, enable install from unknown sources for your file manager/browser, then install the APK.

## Option 2: Build APK on your PC

Buildozer needs Linux/WSL. On Windows, install WSL first:

```powershell
wsl --install
```

After restart, open Ubuntu and run:

```bash
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk build-essential ccache libffi-dev libssl-dev libltdl-dev
cd /mnt/c/Users/DUBAI\ LAPTOP\ BAZAR/Desktop/CODEER/tools/link_downloader_app
python3 -m pip install --user buildozer cython virtualenv
~/.local/bin/buildozer android debug
```

Your APK will be inside:

```text
tools/link_downloader_app/bin/
```
