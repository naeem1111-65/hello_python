[app]
title = Link Downloader
package.name = linkdownloader
package.domain = org.local
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg
version = 0.1.0
requirements = python3,kivy,yt-dlp,certifi
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
