from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)

from PySide6.QtCore import (
    QTimer,
    QThread,
)

from gui.dashboard import Dashboard
from gui.sidebar import Sidebar
from gui.header import Header
from gui.app_status_bar import AppStatusBar
from gui.styles import APP_STYLE

from controllers.spotify_controller import SpotifyController
from workers.apply_shuffle_worker import ApplyShuffleWorker
from workers.preview_worker import PreviewWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = SpotifyController()

        # Background preview worker
        # Background preview worker
        self.preview_thread = None
        self.preview_worker = None

        # Background apply-shuffle worker
        self.apply_thread = None
        self.apply_worker = None

        self.setWindowTitle("Spotify Power Tools")
        self.resize(1600, 950)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.header = Header()

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.dashboard = Dashboard()

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.dashboard, 1)

        self.status_bar = AppStatusBar()

        root_layout.addWidget(self.header)
        root_layout.addWidget(body, 1)
        root_layout.addWidget(self.status_bar)

        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self.dashboard.shuffle_panel.preview_button.clicked.connect(
            self.preview_shuffle
        )

        self.dashboard.shuffle_panel.apply_button.clicked.connect(
            self.apply_shuffle
        )

    def refresh(self):

        try:
            current = self.controller.current_playback()

            self.header.set_connected(
                current is not None
            )

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

            if playlist is not None:
                self.status_bar.set_message(
                    f"Connected • Playlist: {playlist['name']} • {len(tracks)} songs"
                )
            else:
                self.status_bar.set_message(
                    "Connected • No playlist currently playing"
                )

        except Exception as error:

            self.header.set_connected(False)

            self.status_bar.set_message(
                f"Error: {error}"
            )

    def preview_shuffle(self):

        self.dashboard.shuffle_panel.preview_button.setEnabled(False)

        self.dashboard.shuffle_panel.preview_button.setText(
            "Generating..."
        )

        self.status_bar.set_message(
            "Generating Smart Shuffle preview..."
        )

        self.preview_thread = QThread()

        self.preview_worker = PreviewWorker(
            self.controller
        )

        self.preview_worker.moveToThread(
            self.preview_thread
        )

        self.preview_thread.started.connect(
            self.preview_worker.run
        )

        self.preview_worker.finished.connect(
            self.preview_finished
        )

        self.preview_worker.error.connect(
            self.preview_error
        )

        self.preview_worker.finished.connect(
            self.preview_thread.quit
        )

        self.preview_thread.finished.connect(
            self.preview_thread.deleteLater
        )

        self.preview_thread.start()

    def preview_finished(self, preview):

        self.dashboard.preview_panel.show_tracks(
            preview
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.dashboard.shuffle_panel.preview_button.setText(
            "Preview Shuffle"
        )

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.status_bar.set_message(
            f"Preview ready • Showing {len(preview)} upcoming songs"
        )

    def preview_error(self, message):

        QMessageBox.critical(
            self,
            "Preview Error",
            message
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.dashboard.shuffle_panel.preview_button.setText(
            "Preview Shuffle"
        )

        self.status_bar.set_message(
            "Preview failed"
        )

    def apply_shuffle(self):

        self.dashboard.shuffle_panel.apply_button.setEnabled(False)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Applying..."
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(False)

        self.status_bar.set_message(
            "Creating Smart Shuffle playlist..."
        )

        self.apply_thread = QThread()

        self.apply_worker = ApplyShuffleWorker(
            self.controller
        )

        self.apply_worker.moveToThread(
            self.apply_thread
        )

        self.apply_thread.started.connect(
            self.apply_worker.run
        )

        self.apply_worker.finished.connect(
            self.apply_finished
        )

        self.apply_worker.error.connect(
            self.apply_error
        )

        self.apply_worker.finished.connect(
            self.apply_thread.quit
        )

        self.apply_thread.finished.connect(
            self.apply_thread.deleteLater
        )

        self.apply_thread.start()

    def apply_finished(self, result):

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Apply Shuffle"
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.status_bar.set_message(
            f"Smart Shuffle applied • {result['track_count']} songs"
        )

        QMessageBox.information(
            self,
            "Smart Shuffle Applied",
            (
                f"Created/updated playlist:\n\n"
                f"{result['playlist_name']}\n\n"
                f"Songs added: {result['track_count']}\n\n"
                f"Your original playlist was not modified."
            )
        )

    def apply_error(self, message):

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Apply Shuffle"
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.status_bar.set_message(
            "Apply Shuffle failed"
        )

        QMessageBox.critical(
            self,
            "Apply Shuffle Error",
            message
        )