import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout


def format_duration(ms):
    try:
        total_seconds = int(ms) // 1000
    except (TypeError, ValueError):
        return "—"

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:02d}"


def song_to_payload(song):
    if song is None:
        return None

    return {
        "name": getattr(song, "name", "Unknown Song"),
        "artist": getattr(song, "artist", "Unknown Artist"),
        "album": getattr(song, "album", ""),
        "duration": format_duration(getattr(song, "duration_ms", 0)),
        "imageUrl": getattr(song, "image_url", ""),
    }


class QueueBridge(QObject):
    refreshRequested = Signal()

    @Slot()
    def refreshQueue(self):
        self.refreshRequested.emit()


class QueuePage(QWidget):
    MAX_ITEMS = 25

    refresh_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("QueuePage")

        self.web_ready = False

        self.latest_payload = {
            "isLoading": False,
            "currentlyPlaying": None,
            "queue": [],
            "message": "No queue data yet.",
        }

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebQueueView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.bridge = QueueBridge()

        self.bridge.refreshRequested.connect(
            self.refresh_requested.emit
        )

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("queueBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(
            self.on_web_loaded
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "queue.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(self.web_view)

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
            "window.queuePage.update",
            payload,
        )

    def set_loading(self, loading):
        payload = dict(self.latest_payload)
        payload["isLoading"] = bool(loading)

        if loading:
            payload["message"] = "Loading Spotify queue..."

        self.push_payload(payload)

    def update_queue(self, queue_data):
        queue_data = queue_data or {}

        currently_playing = queue_data.get(
            "currently_playing"
        )

        queue = queue_data.get(
            "queue",
            []
        )

        limited_queue = queue[:self.MAX_ITEMS]

        payload = {
            "isLoading": False,
            "currentlyPlaying": song_to_payload(currently_playing),
            "queue": [
                song_to_payload(song)
                for song in limited_queue
                if song is not None
            ],
            "message": (
                "Your Spotify queue is currently empty, or Spotify did not return queue data."
                if not queue
                else ""
            ),
        }

        self.push_payload(payload)