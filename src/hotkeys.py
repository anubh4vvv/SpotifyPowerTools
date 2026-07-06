from PySide6.QtCore import QObject, Signal

import keyboard

from services.settings_service import (
    DEFAULT_HOTKEYS,
    VALID_HOTKEY_KEYS,
    HOTKEY_LABELS,
)


class HotkeyManager(QObject):

    play_pause_requested = Signal()
    next_requested = Signal()
    previous_requested = Signal()
    preview_shuffle_requested = Signal()
    queue_shuffle_requested = Signal()
    show_dashboard_requested = Signal()
    show_app_requested = Signal()

    ACTION_SIGNALS = {
        "hotkey_play_pause": "play_pause_requested",
        "hotkey_next": "next_requested",
        "hotkey_previous": "previous_requested",
        "hotkey_preview_shuffle": "preview_shuffle_requested",
        "hotkey_queue_shuffle": "queue_shuffle_requested",
        "hotkey_show_dashboard": "show_dashboard_requested",
        "hotkey_show_app": "show_app_requested",
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_running = False
        self.handles = []
        self.active_hotkeys = {}

    def normalize_shortcut(self, shortcut):
        return str(shortcut or "").strip().lower()

    def shortcut_label(self, action_key):
        return HOTKEY_LABELS.get(
            action_key,
            action_key
        )

    def validate_hotkeys(self, settings):
        seen = {}

        for action_key in VALID_HOTKEY_KEYS:

            shortcut = self.normalize_shortcut(
                settings.get(
                    action_key,
                    DEFAULT_HOTKEYS[action_key]
                )
            )

            if not shortcut:
                raise RuntimeError(
                    f"No shortcut set for {self.shortcut_label(action_key)}."
                )

            if shortcut in seen:
                first_action = self.shortcut_label(
                    seen[shortcut]
                )

                second_action = self.shortcut_label(
                    action_key
                )

                raise RuntimeError(
                    f"Duplicate shortcut '{shortcut}' used for "
                    f"{first_action} and {second_action}."
                )

            seen[shortcut] = action_key

    def register(self, shortcut, callback):
        handle = keyboard.add_hotkey(
            shortcut,
            callback,
            suppress=False,
            trigger_on_release=False,
        )

        self.handles.append(
            handle
        )

    def start(self, settings=None):
        settings = settings or {}

        if not settings.get("hotkeys_enabled", True):
            self.stop()
            return False

        if self.is_running:
            self.stop()

        resolved = {}

        for action_key in VALID_HOTKEY_KEYS:
            resolved[action_key] = self.normalize_shortcut(
                settings.get(
                    action_key,
                    DEFAULT_HOTKEYS[action_key]
                )
            )

        self.validate_hotkeys(
            resolved
        )

        try:
            for action_key, shortcut in resolved.items():

                signal_name = self.ACTION_SIGNALS.get(
                    action_key
                )

                signal = getattr(
                    self,
                    signal_name
                )

                self.register(
                    shortcut,
                    signal.emit
                )

            self.active_hotkeys = resolved
            self.is_running = True

            return True

        except Exception:
            self.stop()
            raise

    def stop(self):
        for handle in self.handles:

            try:
                keyboard.remove_hotkey(
                    handle
                )

            except Exception:
                pass

        self.handles.clear()
        self.active_hotkeys = {}
        self.is_running = False