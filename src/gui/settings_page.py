import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout

from services.settings_service import (
    load_settings,
    save_settings,
    reset_settings,
    reset_hotkeys,
    hotkey_items_from_settings,
    VALID_PROFILES,
    VALID_QUEUE_SIZES,
)


class SettingsBridge(QObject):

    saveRequested = Signal(
        str,
        int,
        int,
        int,
        int,
        bool,
        bool,
        str,
    )

    resetRequested = Signal()
    resetHotkeysRequested = Signal()
    memoryExportRequested = Signal()
    memoryClearRequested = Signal()
    imageCacheClearRequested = Signal()

    @Slot(str, int, int, int, int, bool, bool, str)
    def saveSettings(
        self,
        profile,
        queue_size,
        artist_weight,
        album_weight,
        randomness,
        hotkeys_enabled,
        gaming_mode_enabled,
        hotkeys_json,
    ):
        self.saveRequested.emit(
            str(profile),
            int(queue_size),
            int(artist_weight),
            int(album_weight),
            int(randomness),
            bool(hotkeys_enabled),
            bool(gaming_mode_enabled),
            str(hotkeys_json or "{}"),
        )

    @Slot()
    def resetSettings(self):
        self.resetRequested.emit()

    @Slot()
    def resetHotkeys(self):
        self.resetHotkeysRequested.emit()

    @Slot()
    def exportMemory(self):
        self.memoryExportRequested.emit()

    @Slot()
    def clearMemory(self):
        self.memoryClearRequested.emit()

    @Slot()
    def clearImageCache(self):
        self.imageCacheClearRequested.emit()


class SettingsPage(QWidget):

    settings_saved = Signal(dict)
    memory_export_requested = Signal()
    memory_clear_requested = Signal()
    image_cache_clear_requested = Signal()

    def __init__(self):
        super().__init__()

        self.setObjectName("SettingsPage")

        self.web_ready = False
        self.current_settings = load_settings()
        self.latest_message = ""

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebSettingsView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        self.bridge = SettingsBridge()

        self.bridge.saveRequested.connect(
            self.save_from_web
        )

        self.bridge.resetRequested.connect(
            self.reset_to_defaults
        )

        self.bridge.resetHotkeysRequested.connect(
            self.reset_hotkeys_to_defaults
        )

        self.bridge.memoryExportRequested.connect(
            self.memory_export_requested.emit
        )

        self.bridge.memoryClearRequested.connect(
            self.memory_clear_requested.emit
        )

        self.bridge.imageCacheClearRequested.connect(
            self.image_cache_clear_requested.emit
        )

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("settingsBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(
            self.on_web_loaded
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "settings.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(self.web_view)

    def on_web_loaded(self, ok):
        self.web_ready = bool(ok)

        if self.web_ready:
            self.push_settings()
            self.push_message(self.latest_message)

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

    def build_payload(self):
        return {
            "settings": self.current_settings,
            "profiles": VALID_PROFILES,
            "queueSizes": VALID_QUEUE_SIZES,
            "hotkeys": hotkey_items_from_settings(
                self.current_settings
            ),
        }

    def push_settings(self):
        self.run_js_function(
            "window.settingsPage.update",
            self.build_payload(),
        )

    def push_message(self, message):
        self.latest_message = message or ""

        self.run_js_function(
            "window.settingsPage.setMessage",
            {
                "message": self.latest_message,
            },
        )

    def load_from_saved(self):
        self.current_settings = load_settings()
        self.push_settings()

    def get_settings(self):
        return dict(
            self.current_settings
        )

    def decode_hotkeys(self, hotkeys_json):
        try:
            data = json.loads(
                hotkeys_json or "{}"
            )

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        return {}

    def save_from_web(
        self,
        profile,
        queue_size,
        artist_weight,
        album_weight,
        randomness,
        hotkeys_enabled,
        gaming_mode_enabled,
        hotkeys_json,
    ):
        hotkeys = self.decode_hotkeys(
            hotkeys_json
        )

        settings = {
            "shuffle_profile": profile,
            "queue_size": queue_size,
            "artist_weight": artist_weight,
            "album_weight": album_weight,
            "randomness": randomness,
            "hotkeys_enabled": hotkeys_enabled,
            "gaming_mode_enabled": gaming_mode_enabled,
        }

        settings.update(
            hotkeys
        )

        self.current_settings = save_settings(
            settings
        )

        self.push_settings()
        self.push_message("Settings saved.")

        self.settings_saved.emit(
            self.current_settings
        )

    def save_current_settings(self):
        self.current_settings = save_settings(
            self.current_settings
        )

        self.push_settings()
        self.push_message("Settings saved.")

        self.settings_saved.emit(
            self.current_settings
        )

    def reset_hotkeys_to_defaults(self):
        self.current_settings = reset_hotkeys(
            self.current_settings
        )

        self.push_settings()
        self.push_message("Hotkeys restored to defaults.")

        self.settings_saved.emit(
            self.current_settings
        )

    def reset_to_defaults(self):
        self.current_settings = reset_settings()

        self.push_settings()
        self.push_message("Defaults restored.")

        self.settings_saved.emit(
            self.current_settings
        )