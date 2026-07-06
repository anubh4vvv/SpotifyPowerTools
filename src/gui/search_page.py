import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout


def song_to_payload(song, index):
    return {
        "index": index,
        "name": getattr(song, "name", "Unknown Song"),
        "artist": getattr(song, "artist", "Unknown Artist"),
        "album": getattr(song, "album", ""),
        "durationMs": getattr(song, "duration_ms", 0),
        "imageUrl": getattr(song, "image_url", ""),
    }


class SearchBridge(QObject):
    searchRequested = Signal(str)
    addRequested = Signal(int)
    clearRequested = Signal()

    @Slot(str)
    def search(self, query):
        query = str(query or "").strip()

        if query:
            self.searchRequested.emit(query)

    @Slot(int)
    def addToQueue(self, index):
        self.addRequested.emit(int(index))

    @Slot()
    def clearSearch(self):
        self.clearRequested.emit()


class SearchPage(QWidget):
    search_requested = Signal(str)
    add_to_queue_requested = Signal(object)

    def __init__(self):
        super().__init__()

        self.setObjectName("SearchPage")

        self.web_ready = False
        self.current_results = []
        self.last_query = ""
        self.active_query = ""

        self.latest_payload = {
            "isLoading": False,
            "query": "",
            "results": [],
            "message": "No search yet. Type a song name and press Search.",
        }

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebSearchView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.bridge = SearchBridge()

        self.bridge.searchRequested.connect(
            self.emit_search
        )

        self.bridge.addRequested.connect(
            self.emit_add_to_queue
        )

        self.bridge.clearRequested.connect(
            self.clear_results
        )

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("searchBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(
            self.on_web_loaded
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "search.html"
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
            "window.searchPage.update",
            payload,
        )

    def emit_search(self, query=None):
        query = str(query or "").strip()

        if not query:
            self.clear_results()
            return

        if query == self.active_query and self.latest_payload.get("isLoading"):
            return

        self.last_query = query
        self.active_query = query

        self.search_requested.emit(
            query
        )

    def emit_add_to_queue(self, index):
        if index < 0 or index >= len(self.current_results):
            return

        self.add_to_queue_requested.emit(
            self.current_results[index]
        )

    def set_loading(self, loading, query=None):
        query = str(query or self.active_query or self.last_query or "").strip()

        payload = dict(self.latest_payload)
        payload["isLoading"] = bool(loading)
        payload["query"] = query

        if loading:
            payload["message"] = "Searching Spotify..."
            payload["results"] = []

        self.push_payload(
            payload
        )

    def clear_results(self):
        self.current_results = []
        self.last_query = ""
        self.active_query = ""

        self.push_payload({
            "isLoading": False,
            "query": "",
            "results": [],
            "message": "No search yet. Type a song name and press Search.",
        })

    def show_results(self, query, songs):
        query = str(query or "").strip()

        if query != self.active_query:
            return

        songs = songs or []

        self.last_query = query
        self.current_results = songs

        if not songs:
            self.push_payload({
                "isLoading": False,
                "query": query,
                "results": [],
                "message": "No tracks found. Try a different search.",
            })

            return

        self.push_payload({
            "isLoading": False,
            "query": query,
            "results": [
                song_to_payload(song, index)
                for index, song in enumerate(songs)
            ],
            "message": "",
        })

    def show_search_error(self, query, message):
        query = str(query or "").strip()

        if query != self.active_query:
            return

        self.push_payload({
            "isLoading": False,
            "query": query,
            "results": [],
            "message": message or "Search failed. Try again.",
        })