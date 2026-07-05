import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout

from services.duplicate_service import analyze_duplicates


class DuplicatesBridge(QObject):
    cleanRequested = Signal()

    @Slot()
    def createCleanedCopy(self):
        self.cleanRequested.emit()


class DuplicatesPage(QWidget):
    clean_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("DuplicatesPage")

        self.is_busy = False
        self.web_ready = False
        self.latest_payload = self.empty_payload()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebDuplicatesView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.bridge = DuplicatesBridge()

        self.bridge.cleanRequested.connect(
            self.clean_requested.emit
        )

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("duplicatesBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(
            self.on_web_loaded
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "duplicates.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(self.web_view)

    def empty_payload(self):
        return {
            "stats": {
                "totalSongs": 0,
                "duplicateTracks": 0,
                "extraCopies": 0,
                "status": "No Playlist",
                "statusTone": "rose",
            },
            "hasPlaylist": False,
            "hasDuplicates": False,
            "isBusy": False,
            "duplicates": [],
        }

    def on_web_loaded(self, ok):
        self.web_ready = bool(ok)

        if self.web_ready:
            self.push_payload(
                self.latest_payload
            )

    def run_js_function(self, function_name, payload):
        if not self.web_ready:
            return

        js_payload = json.dumps(
            payload,
            ensure_ascii=False,
        )

        self.web_view.page().runJavaScript(
            f"{function_name}({js_payload});"
        )

    def push_payload(self, payload):
        self.latest_payload = payload

        self.run_js_function(
            "window.duplicatesPage.update",
            payload,
        )

    def set_busy(self, busy):
        self.is_busy = bool(busy)

        payload = dict(self.latest_payload or self.empty_payload())
        payload["isBusy"] = self.is_busy

        self.push_payload(payload)

    def update_duplicates(self, playlist, tracks):
        analysis = analyze_duplicates(
            tracks
        )

        self.update_from_analysis(
            playlist,
            analysis
        )

    def update_from_analysis(self, playlist, analysis):
        analysis = analysis or {}

        total_songs = analysis.get("total_songs", 0)
        duplicate_tracks = analysis.get("unique_duplicate_tracks", 0)
        extra_copies = analysis.get("extra_copies", 0)
        duplicates = analysis.get("duplicates", [])

        has_playlist = playlist is not None
        has_duplicates = extra_copies > 0

        if not has_playlist:
            status = "No Playlist"
            status_tone = "rose"
        elif has_duplicates:
            status = "Review"
            status_tone = "rose"
        else:
            status = "Clean"
            status_tone = "sage"

        payload = {
            "stats": {
                "totalSongs": total_songs,
                "duplicateTracks": duplicate_tracks,
                "extraCopies": extra_copies,
                "status": status,
                "statusTone": status_tone,
            },
            "hasPlaylist": has_playlist,
            "hasDuplicates": has_duplicates,
            "isBusy": self.is_busy,
            "duplicates": self.normalize_duplicates(duplicates),
        }

        self.push_payload(payload)

    def normalize_duplicates(self, duplicates):
        rows = []

        for item in duplicates or []:
            rows.append({
                "name": item.get("name", "Unknown Song"),
                "artist": item.get("artist", "Unknown Artist"),
                "album": item.get("album", "Unknown Album"),
                "releaseYear": item.get("release_year", "Unknown"),
                "duration": item.get("duration", "0:00"),
                "totalCopies": item.get("total_copies", 0),
                "extraCopies": item.get("extra_copies", 0),
            })

        return rows

    def format_duplicates(self, duplicates):
        if not duplicates:
            return (
                "No duplicate tracks found.\n\n"
                "Your playlist looks clean."
            )

        lines = []

        for index, item in enumerate(duplicates, start=1):
            lines.append(
                f"{index}. {item['name']} — {item['artist']}\n"
                f"   Album: {item['album']}\n"
                f"   Year: {item['release_year']}  •  Duration: {item['duration']}\n"
                f"   Total copies: {item['total_copies']}  •  Extra copies: {item['extra_copies']}\n"
            )

        return "\n".join(lines)