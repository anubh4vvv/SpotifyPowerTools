import webbrowser
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QStackedWidget,
)

from PySide6.QtCore import (
    QTimer,
    QThread,
)

from gui.dashboard import Dashboard
from gui.analytics_page import AnalyticsPage
from gui.duplicates_page import DuplicatesPage
from gui.sidebar import Sidebar
from gui.header import Header
from gui.app_status_bar import AppStatusBar
from gui.styles import APP_STYLE
from gui.settings_page import SettingsPage

from controllers.spotify_controller import SpotifyController

from workers.preview_worker import PreviewWorker
from workers.queue_shuffle_worker import QueueShuffleWorker
from workers.cleaner_worker import CleanerWorker

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = SpotifyController()

        self.preview_thread = None
        self.preview_worker = None

        self.queue_thread = None
        self.queue_worker = None

        self.cleaner_thread = None
        self.cleaner_worker = None

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

        self.stack = QStackedWidget()

        self.dashboard = Dashboard()
        self.analytics_page = AnalyticsPage()
        self.duplicates_page = DuplicatesPage()
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.analytics_page)
        self.stack.addWidget(self.duplicates_page)
        self.stack.addWidget(self.settings_page)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stack, 1)

        self.status_bar = AppStatusBar()

        root_layout.addWidget(self.header)
        root_layout.addWidget(body, 1)
        root_layout.addWidget(self.status_bar)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queue Smart Shuffle"
        )

        self.sidebar.dashboard_btn.clicked.connect(
            self.show_dashboard
        )

        self.sidebar.shuffle_btn.clicked.connect(
            self.show_dashboard
        )

        self.sidebar.analytics_btn.clicked.connect(
            self.show_analytics
        )

        self.sidebar.duplicates_btn.clicked.connect(
            self.show_duplicates
        )

        self.sidebar.settings_btn.clicked.connect(
            self.show_settings
        )

        self.settings_page.settings_saved.connect(
            self.apply_saved_settings
        )

        self.duplicates_page.clean_button.clicked.connect(
            self.create_cleaned_playlist
        )

        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self.dashboard.shuffle_panel.preview_button.clicked.connect(
            self.preview_shuffle
        )

        self.dashboard.shuffle_panel.apply_button.clicked.connect(
            self.queue_shuffle
        )

    def show_dashboard(self):

        self.stack.setCurrentWidget(
            self.dashboard
        )

        self.status_bar.set_message(
            "Dashboard"
        )

    def show_analytics(self):

        self.stack.setCurrentWidget(
            self.analytics_page
        )

        playlist, tracks = self.controller.current_playlist()

        self.analytics_page.update_analytics(
            playlist,
            tracks
        )

        if playlist is not None:
            self.status_bar.set_message(
                f"Analytics • {playlist['name']}"
            )
        else:
            self.status_bar.set_message(
                "Analytics • No playlist currently playing"
            )

    def show_duplicates(self):

        self.stack.setCurrentWidget(
            self.duplicates_page
        )

        playlist, tracks = self.controller.current_playlist()

        self.duplicates_page.update_duplicates(
            playlist,
            tracks
        )

        if playlist is not None:
            self.status_bar.set_message(
                f"Duplicates • {playlist['name']}"
            )
        else:
            self.status_bar.set_message(
                "Duplicates • No playlist currently playing"
            )

    def create_cleaned_playlist(self):

        self.duplicates_page.set_busy(True)

        self.status_bar.set_message(
            "Creating cleaned playlist copy..."
        )

        self.cleaner_thread = QThread()

        self.cleaner_worker = CleanerWorker(
            self.controller
        )

        self.cleaner_worker.moveToThread(
            self.cleaner_thread
        )

        self.cleaner_thread.started.connect(
            self.cleaner_worker.run
        )

        self.cleaner_worker.finished.connect(
            self.cleaner_finished
        )

        self.cleaner_worker.error.connect(
            self.cleaner_error
        )

        self.cleaner_worker.finished.connect(
            self.cleaner_thread.quit
        )

        self.cleaner_thread.finished.connect(
            self.cleaner_thread.deleteLater
        )

        self.cleaner_thread.start()

    def cleaner_finished(self, result):

        self.duplicates_page.set_busy(False)

        self.status_bar.set_message(
            f"Created cleaned playlist • Removed {result['removed_count']} duplicates"
        )

        message = (
            f"Created playlist:\n\n"
            f"{result['playlist_name']}\n\n"
            f"Original songs: {result['original_count']}\n"
            f"Cleaned songs: {result['cleaned_count']}\n"
            f"Removed duplicates: {result['removed_count']}\n\n"
            f"Your original playlist was not modified.\n\n"
            f"Open the cleaned playlist in Spotify?"
        )

        reply = QMessageBox.question(
            self,
            "Cleaned Playlist Created",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:

            playlist_url = result.get("playlist_url")

            if playlist_url:
                webbrowser.open(playlist_url)

                self.status_bar.set_message(
                    "Opened cleaned playlist in Spotify"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Spotify Link Missing",
                    "The playlist was created, but no Spotify link was returned."
                )

    def cleaner_error(self, message):

        self.duplicates_page.set_busy(False)

        self.status_bar.set_message(
            "Cleaned playlist creation failed"
        )

        QMessageBox.critical(
            self,
            "Playlist Cleaner Error",
            message
        )

    def show_settings(self):

        self.settings_page.load_from_saved()

        self.stack.setCurrentWidget(
            self.settings_page
        )

        self.status_bar.set_message(
            "Settings"
        )

    def apply_saved_settings(self, settings):

        self.dashboard.shuffle_panel.apply_settings(
            settings
        )

        self.status_bar.set_message(
            "Settings saved"
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

            self.analytics_page.update_analytics(
                playlist,
                tracks
            )

            self.duplicates_page.update_duplicates(
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

        self.dashboard.shuffle_panel.apply_button.setEnabled(False)

        shuffle_settings = self.dashboard.shuffle_panel.get_settings()

        self.status_bar.set_message(
            "Generating Smart Shuffle preview..."
        )

        self.preview_thread = QThread()

        self.preview_worker = PreviewWorker(
            self.controller,
            shuffle_settings
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

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queue Smart Shuffle"
        )

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

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queue Smart Shuffle"
        )

        self.status_bar.set_message(
            "Preview failed"
        )

    def queue_shuffle(self):

        self.dashboard.shuffle_panel.apply_button.setEnabled(False)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queueing..."
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(False)

        shuffle_settings = self.dashboard.shuffle_panel.get_settings()

        queue_limit = shuffle_settings["queue_size"]

        self.status_bar.set_message(
            f"Adding {queue_limit} smart-shuffled songs to Spotify queue..."
        )

        self.queue_thread = QThread()

        self.queue_worker = QueueShuffleWorker(
            self.controller,
            queue_limit,
            shuffle_settings
        )

        self.queue_worker.moveToThread(
            self.queue_thread
        )

        self.queue_thread.started.connect(
            self.queue_worker.run
        )

        self.queue_worker.finished.connect(
            self.queue_finished
        )

        self.queue_worker.error.connect(
            self.queue_error
        )

        self.queue_worker.finished.connect(
            self.queue_thread.quit
        )

        self.queue_thread.finished.connect(
            self.queue_thread.deleteLater
        )

        self.queue_thread.start()

    def queue_finished(self, result):

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queue Smart Shuffle"
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.status_bar.set_message(
            f"Queued {result['queued_count']} songs from {result['playlist_name']}"
        )

        QMessageBox.information(
            self,
            "Smart Shuffle Queued",
            (
                f"Queued {result['queued_count']} smart-shuffled songs.\n\n"
                f"Playlist: {result['playlist_name']}\n\n"
                f"Starting after: {result['current_song_name']}\n\n"
                f"Music will continue from your current Spotify playback."
            )
        )

    def queue_error(self, message):

        self.dashboard.shuffle_panel.apply_button.setEnabled(True)

        self.dashboard.shuffle_panel.apply_button.setText(
            "Queue Smart Shuffle"
        )

        self.dashboard.shuffle_panel.preview_button.setEnabled(True)

        self.status_bar.set_message(
            "Queue Smart Shuffle failed"
        )

        QMessageBox.critical(
            self,
            "Queue Smart Shuffle Error",
            message
        )