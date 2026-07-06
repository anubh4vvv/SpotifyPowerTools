from PySide6.QtCore import QObject, Signal

import keyboard


class HotkeyManager(QObject):

    play_pause_requested = Signal()
    next_requested = Signal()
    previous_requested = Signal()
    preview_shuffle_requested = Signal()
    queue_shuffle_requested = Signal()
    show_dashboard_requested = Signal()
    show_app_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_running = False
        self.handles = []

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

    def start(self):
        if self.is_running:
            return

        self.register(
            "ctrl+alt+space",
            self.play_pause_requested.emit
        )

        self.register(
            "ctrl+alt+right",
            self.next_requested.emit
        )

        self.register(
            "ctrl+alt+left",
            self.previous_requested.emit
        )

        self.register(
            "ctrl+alt+p",
            self.preview_shuffle_requested.emit
        )

        self.register(
            "ctrl+alt+q",
            self.queue_shuffle_requested.emit
        )

        self.register(
            "ctrl+alt+d",
            self.show_dashboard_requested.emit
        )

        self.register(
            "ctrl+alt+s",
            self.show_app_requested.emit
        )

        self.is_running = True

    def stop(self):
        for handle in self.handles:

            try:
                keyboard.remove_hotkey(
                    handle
                )

            except Exception:
                pass

        self.handles.clear()

        self.is_running = False