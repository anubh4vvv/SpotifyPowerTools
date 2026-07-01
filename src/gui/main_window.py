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
from gui.about_page import AboutPage
from gui.sidebar import Sidebar
from gui.header import Header
from gui.app_status_bar import AppStatusBar
from gui.styles import APP_STYLE
from gui.settings_page import SettingsPage
from gui.queue_page import QueuePage
from gui.search_page import SearchPage

from controllers.spotify_controller import SpotifyController

from workers.preview_worker import PreviewWorker
from workers.queue_shuffle_worker import QueueShuffleWorker
from workers.cleaner_worker import CleanerWorker
from workers.queue_view_worker import QueueViewWorker
from workers.search_worker import SearchWorker

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

        self.queue_view_thread = None
        self.queue_view_worker = None

        self.search_thread = None
        self.search_worker = None

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
        self.queue_page = QueuePage()
        self.search_page = SearchPage()
        self.settings_page = SettingsPage()
        self.about_page = AboutPage()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.analytics_page)
        self.stack.addWidget(self.duplicates_page)
        self.stack.addWidget(self.queue_page)
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.about_page)

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
            self.show_smart_shuffle
        )

        self.sidebar.analytics_btn.clicked.connect(
            self.show_analytics
        )

        self.sidebar.queue_btn.clicked.connect(
            self.show_queue
        )

        self.sidebar.search_btn.clicked.connect(
            self.show_search
        )

        self.sidebar.duplicates_btn.clicked.connect(
            self.show_duplicates
        )

        self.sidebar.settings_btn.clicked.connect(
            self.show_settings
        )

        self.sidebar.about_btn.clicked.connect(
            self.show_about
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

        self.queue_page.refresh_button.clicked.connect(
            self.refresh_queue_page
        )

        self.search_page.search_requested.connect(
            self.search_tracks
        )

        self.search_page.add_to_queue_requested.connect(
            self.add_search_result_to_queue
        )

        self.dashboard.current_song_card.previous_button.clicked.connect(
            self.previous_song
        )

        self.dashboard.current_song_card.play_pause_button.clicked.connect(
            self.toggle_playback
        )

        self.dashboard.current_song_card.next_button.clicked.connect(
            self.next_song
        )

        self.dashboard.player_controls_card.volume_slider.sliderReleased.connect(
            self.set_volume_from_slider
        )

        self.dashboard.player_controls_card.shuffle_button.clicked.connect(
            self.toggle_shuffle
        )

        self.dashboard.player_controls_card.repeat_combo.currentTextChanged.connect(
            self.set_repeat_mode
        )

        self.dashboard.player_controls_card.refresh_devices_button.clicked.connect(
            self.refresh_devices
        )

        self.dashboard.player_controls_card.device_combo.activated.connect(
            self.transfer_playback_to_selected_device
        )



        self.dashboard.current_song_card.progress_slider.sliderReleased.connect(
            self.seek_from_progress_slider
        )

        self.refresh_devices()

    def show_dashboard(self):

        self.sidebar.set_active_button(
            self.sidebar.dashboard_btn
        )

        self.stack.setCurrentWidget(
            self.dashboard
        )

        self.status_bar.set_message(
            "Dashboard"
        )

    def show_smart_shuffle(self):

        self.sidebar.set_active_button(
            self.sidebar.shuffle_btn
        )

        self.stack.setCurrentWidget(
            self.dashboard
        )

        self.dashboard.shuffle_panel.highlight()

        self.dashboard.shuffle_panel.preview_button.setFocus()

        self.status_bar.set_message(
            "Smart Shuffle selected"
        )

    def show_analytics(self):

        self.sidebar.set_active_button(
            self.sidebar.analytics_btn
        )

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

        self.sidebar.set_active_button(
            self.sidebar.duplicates_btn
        )

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

    def show_queue(self):

        self.sidebar.set_active_button(
            self.sidebar.queue_btn
        )

        self.stack.setCurrentWidget(
            self.queue_page
        )

        self.refresh_queue_page()

    def show_search(self):

        self.sidebar.set_active_button(
            self.sidebar.search_btn
        )

        self.stack.setCurrentWidget(
            self.search_page
        )

        self.status_bar.set_message(
            "Search Spotify"
        )

    def search_tracks(self, query):

        self.search_page.set_loading(True)

        self.status_bar.set_message(
            f"Searching Spotify for '{query}'..."
        )

        self.search_thread = QThread()

        self.search_worker = SearchWorker(
            self.controller,
            query,
            limit=10
        )

        self.search_worker.moveToThread(
            self.search_thread
        )

        self.search_thread.started.connect(
            self.search_worker.run
        )

        self.search_worker.finished.connect(
            self.search_finished
        )

        self.search_worker.error.connect(
            self.search_error
        )

        self.search_worker.finished.connect(
            self.search_thread.quit
        )

        self.search_thread.finished.connect(
            self.search_thread.deleteLater
        )

        self.search_thread.start()

    def search_finished(self, songs):

        self.search_page.set_loading(False)

        self.search_page.show_results(
            songs
        )

        self.status_bar.set_message(
            f"Search complete • {len(songs)} results"
        )

    def search_error(self, message):

        self.search_page.set_loading(False)

        QMessageBox.critical(
            self,
            "Search Error",
            message
        )

        self.status_bar.set_message(
            "Search failed"
        )

    def add_search_result_to_queue(self, song):

        try:
            result = self.controller.add_song_to_queue(
                song
            )

            self.status_bar.set_message(
                result["message"]
            )

            QMessageBox.information(
                self,
                "Added to Queue",
                (
                    f"Added to Spotify queue:\n\n"
                    f"{result['song_name']} — {result['artist']}"
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Queue Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to add song to queue"
            )

    def refresh_queue_page(self):

        self.queue_page.set_loading(True)

        self.status_bar.set_message(
            "Loading Spotify queue..."
        )

        self.queue_view_thread = QThread()

        self.queue_view_worker = QueueViewWorker(
            self.controller,
            limit=25
        )

        self.queue_view_worker.moveToThread(
            self.queue_view_thread
        )

        self.queue_view_thread.started.connect(
            self.queue_view_worker.run
        )

        self.queue_view_worker.finished.connect(
            self.queue_view_finished
        )

        self.queue_view_worker.error.connect(
            self.queue_view_error
        )

        self.queue_view_worker.finished.connect(
            self.queue_view_thread.quit
        )

        self.queue_view_thread.finished.connect(
            self.queue_view_thread.deleteLater
        )

        self.queue_view_thread.start()

    def queue_view_finished(self, queue_data):

        self.queue_page.set_loading(False)

        self.queue_page.update_queue(
            queue_data
        )

        self.status_bar.set_message(
            f"Queue • Showing {len(queue_data['queue'])} upcoming songs"
        )

    def queue_view_error(self, message):

        self.queue_page.set_loading(False)

        QMessageBox.critical(
            self,
            "Queue Error",
            message
        )

        self.status_bar.set_message(
            "Failed to load Spotify queue"
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

        self.sidebar.set_active_button(
            self.sidebar.settings_btn
        )

        self.settings_page.load_from_saved()

        self.stack.setCurrentWidget(
            self.settings_page
        )

        self.status_bar.set_message(
            "Settings"
        )

    def show_about(self):

        self.sidebar.set_active_button(
            self.sidebar.about_btn
        )

        self.stack.setCurrentWidget(
            self.about_page
        )

        self.status_bar.set_message(
            "About Spotify Power Tools"
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

            self.dashboard.player_controls_card.update_playback_state(
                current
            )

            current_page = self.stack.currentWidget()

            playlist, tracks = (
                self.controller.current_playlist()
            )

            if current_page == self.dashboard:

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

            elif current_page == self.analytics_page:

                self.analytics_page.update_analytics(
                    playlist,
                    tracks
                )

            elif current_page == self.duplicates_page:

                if not self.duplicates_page.is_busy:
                    self.duplicates_page.update_duplicates(
                        playlist,
                        tracks
                    )

        except Exception as error:

            self.header.set_connected(False)

            self.status_bar.set_message(
                f"Error: {error}"
            )

    def previous_song(self):

        try:
            self.controller.previous_song()

            self.status_bar.set_message(
                "Skipped to previous song"
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Playback Error",
                str(error)
            )

    def next_song(self):

        try:
            self.controller.next_song()

            self.status_bar.set_message(
                "Skipped to next song"
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Playback Error",
                str(error)
            )

    def seek_from_progress_slider(self):

        try:
            position_ms = self.dashboard.current_song_card.progress_slider.value()

            result = self.controller.seek_to_position(
                position_ms
            )

            self.status_bar.set_message(
                result["message"]
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Seek Error",
                str(error)
            )

    def refresh_devices(self):

        try:
            devices = self.controller.get_available_devices()

            current = self.controller.current_playback()

            active_device_id = None

            if current is not None:
                device = current.get(
                    "device",
                    {}
                )

                active_device_id = device.get(
                    "id"
                )

            self.dashboard.player_controls_card.update_devices(
                devices,
                active_device_id
            )

            self.status_bar.set_message(
                f"Devices • {len(devices)} available"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Device Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to refresh devices"
            )

    def transfer_playback_to_selected_device(self, index=None):

        try:
            device_id = self.dashboard.player_controls_card.selected_device_id()

            if not device_id:
                return

            result = self.controller.transfer_playback(
                device_id
            )

            self.status_bar.set_message(
                result["message"]
            )

            self.refresh()

            self.refresh_devices()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Device Transfer Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to transfer playback"
            )

    def toggle_playback(self):

        try:
            result = self.controller.toggle_playback()

            self.status_bar.set_message(
                result["message"]
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Playback Error",
                str(error)
            )

    def set_volume_from_slider(self):

        try:
            volume = self.dashboard.player_controls_card.volume_slider.value()

            result = self.controller.set_volume(
                volume
            )

            self.status_bar.set_message(
                result["message"]
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Volume Error",
                str(error)
            )

    def toggle_shuffle(self):

        try:
            result = self.controller.toggle_shuffle()

            self.status_bar.set_message(
                result["message"]
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Shuffle Error",
                str(error)
            )

    def set_repeat_mode(self, text):

        try:
            state_map = {
                "Repeat Off": "off",
                "Repeat Track": "track",
                "Repeat Playlist": "context",
            }

            repeat_state = state_map.get(
                text,
                "off"
            )

            result = self.controller.set_repeat_mode(
                repeat_state
            )

            self.status_bar.set_message(
                result["message"]
            )

            self.refresh()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Repeat Error",
                str(error)
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