from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


DOWNLOAD_OPTIONS = {
    "Best MP4": "best[ext=mp4][vcodec!=none][acodec!=none]/best[vcodec!=none][acodec!=none]/best",
    "Small MP4": "worst[ext=mp4][vcodec!=none][acodec!=none]/worst[vcodec!=none][acodec!=none]/worst",
    "Audio M4A": "bestaudio[ext=m4a]/bestaudio",
}


def request_android_permissions() -> None:
    try:
        from android.permissions import Permission, request_permissions

        request_permissions(
            [
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
            ]
        )
    except Exception:
        pass


def get_default_download_dir() -> Path:
    try:
        from android.storage import app_storage_path, primary_external_storage_path

        public_downloads = Path(primary_external_storage_path()) / "Download" / "LinkDownloader"
        try:
            public_downloads.mkdir(parents=True, exist_ok=True)
            return public_downloads
        except Exception:
            app_dir = Path(app_storage_path()) / "downloads"
            app_dir.mkdir(parents=True, exist_ok=True)
            return app_dir
    except Exception:
        desktop_downloads = Path.home() / "Downloads" / "LinkDownloader"
        desktop_downloads.mkdir(parents=True, exist_ok=True)
        return desktop_downloads


def seconds_to_text(value: int | None) -> str:
    if not value:
        return "unknown length"
    minutes, seconds = divmod(int(value), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:d}:{seconds:02d}"


def clean_text(value: Any, fallback: str = "Unknown") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text or fallback


class DownloaderRoot(BoxLayout):
    url_input = ObjectProperty(None)
    option_spinner = ObjectProperty(None)
    analyze_button = ObjectProperty(None)
    download_button = ObjectProperty(None)
    progress_bar = ObjectProperty(None)

    status_text = StringProperty("Paste a YouTube or Facebook link to begin.")
    info_text = StringProperty("")
    download_dir_text = StringProperty("")
    is_busy = BooleanProperty(False)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.download_dir = get_default_download_dir()
        self.download_dir_text = f"Save folder: {self.download_dir}"
        self.video_url = ""
        self.video_title = ""

    def analyze_url(self) -> None:
        url = self._input_url()
        if not url:
            self._show_error("Paste a video link first.")
            return

        self.video_url = url
        self._set_busy(True, "Checking link...")
        self.info_text = ""
        self.progress_bar.value = 0
        threading.Thread(target=self._extract_info, args=(url,), daemon=True).start()

    def download_selected(self) -> None:
        url = self.video_url or self._input_url()
        if not url:
            self._show_error("Paste a video link first.")
            return

        option = self.option_spinner.text
        if option not in DOWNLOAD_OPTIONS:
            option = "Best MP4"

        self._set_busy(True, f"Starting {option} download...")
        self.progress_bar.value = 0
        threading.Thread(target=self._download, args=(url, option), daemon=True).start()

    def _input_url(self) -> str:
        return self.url_input.text.strip()

    def _extract_info(self, url: str) -> None:
        try:
            from yt_dlp import YoutubeDL

            with YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True}) as ydl:
                info = ydl.extract_info(url, download=False)

            if info is None:
                raise RuntimeError("No video information was returned.")

            title = clean_text(info.get("title"), "Untitled video")
            uploader = clean_text(info.get("uploader") or info.get("channel"), "Unknown creator")
            duration = seconds_to_text(info.get("duration"))
            webpage_url = clean_text(info.get("webpage_url"), url)
            self.video_title = title

            Clock.schedule_once(
                lambda _dt: self._info_ready(title, uploader, duration, webpage_url),
                0,
            )
        except Exception as exc:
            error = str(exc)
            Clock.schedule_once(lambda _dt, error=error: self._show_error(error), 0)

    def _download(self, url: str, option: str) -> None:
        try:
            from yt_dlp import YoutubeDL

            output_template = str(self.download_dir / "%(title).120s-%(id)s.%(ext)s")
            ydl_options = {
                "format": DOWNLOAD_OPTIONS[option],
                "outtmpl": output_template,
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "restrictfilenames": True,
                "progress_hooks": [self._progress_hook],
            }

            with YoutubeDL(ydl_options) as ydl:
                ydl.download([url])

            Clock.schedule_once(
                lambda _dt: self._download_done(f"Downloaded to {self.download_dir}"),
                0,
            )
        except Exception as exc:
            error = str(exc)
            Clock.schedule_once(lambda _dt, error=error: self._show_error(error), 0)

    def _progress_hook(self, data: dict[str, Any]) -> None:
        status = data.get("status")
        if status == "downloading":
            downloaded = data.get("downloaded_bytes") or 0
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            percent = (downloaded / total * 100) if total else 0
            speed = data.get("_speed_str", "").strip()
            eta = data.get("_eta_str", "").strip()
            message = f"Downloading... {percent:.1f}%"
            if speed:
                message += f" at {speed}"
            if eta:
                message += f", ETA {eta}"
            Clock.schedule_once(lambda _dt: self._update_progress(percent, message), 0)
        elif status == "finished":
            Clock.schedule_once(lambda _dt: self._update_progress(100, "Finalizing file..."), 0)

    def _info_ready(self, title: str, uploader: str, duration: str, webpage_url: str) -> None:
        self._set_busy(False, "Ready to download.")
        self.info_text = f"{title}\n{uploader} - {duration}\n{webpage_url}"
        self.option_spinner.values = list(DOWNLOAD_OPTIONS.keys())
        self.option_spinner.text = "Best MP4"
        self.download_button.disabled = False

    def _update_progress(self, percent: float, message: str) -> None:
        self.progress_bar.value = max(0, min(100, percent))
        self.status_text = message

    def _download_done(self, message: str) -> None:
        self._set_busy(False, message)
        self.progress_bar.value = 100

    def _show_error(self, message: str) -> None:
        self._set_busy(False, f"Error: {message}")
        if not self.info_text:
            self.download_button.disabled = True

    def _set_busy(self, busy: bool, message: str) -> None:
        self.is_busy = busy
        self.status_text = message
        self.analyze_button.disabled = busy
        self.download_button.disabled = busy or not bool(self.video_url)


class LinkDownloaderApp(App):
    def build(self) -> DownloaderRoot:
        request_android_permissions()
        return Builder.load_file(str(Path(__file__).with_name("link_downloader.kv")))


if __name__ == "__main__":
    LinkDownloaderApp().run()
