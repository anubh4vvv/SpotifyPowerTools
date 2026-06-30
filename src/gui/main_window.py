from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QMessageBox,
)

from PySide6.QtCore import QTimer

from gui.dashboard import Dashboard
from gui.sidebar import Sidebar
from gui.styles import APP_STYLE

from controllers.spotify_controller import SpotifyController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = SpotifyController()

        self.setWindowTitle("Spotify Power Tools")

        self.resize(1400, 900)

        self.setStyleSheet(APP_STYLE)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.sidebar = Sidebar()

        self.dashboard = Dashboard()

        layout.addWidget(self.sidebar)

        layout.addWidget(
            self.dashboard,
            1
        )

        self.refresh()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.refresh
        )

        self.timer.start(5000)

        self.dashboard.shuffle_panel.preview_button.clicked.connect(
            self.preview_shuffle
        )

        self.dashboard.shuffle_panel.apply_button.clicked.connect(
            self.apply_shuffle
        )

    def refresh(self):

        current = self.controller.current_playback()

        self.dashboard.current_song_card.update_song(
            current
        )

        playlist, tracks = (
            self.controller.current_playlist()
        )

        self.dashboard.playlist_card.update_playlist(
            playlist,
            tracks
        )

    def preview_shuffle(self):

        preview = self.controller.preview_shuffle()

        self.dashboard.preview_panel.show_tracks(
            preview
        )

        self.dashboard.shuffle_panel.apply_button.setEnabled(
            True
        )

    def apply_shuffle(self):

        QMessageBox.information(
            self,
            "Spotify Power Tools",
            "Apply Shuffle will be implemented next."
        )