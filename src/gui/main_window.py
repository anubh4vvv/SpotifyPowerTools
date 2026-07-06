import webbrowser
import time
from datetime import datetime, timezone
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QStackedWidget,
    QGraphicsOpacityEffect,
)

from PySide6.QtCore import (
    QTimer,
    QThread,
    QPropertyAnimation,
    QEasingCurve,
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
from gui.share_card_widget import ShareCardWidget
from gui.film_grain_overlay import FilmGrainOverlay

from controllers.spotify_controller import SpotifyController

from workers.preview_worker import PreviewWorker
from workers.queue_shuffle_worker import QueueShuffleWorker
from workers.cleaner_worker import CleanerWorker
from workers.queue_view_worker import QueueViewWorker
from workers.search_worker import SearchWorker

from services.analytics_service import calculate_playlist_analytics
from services.duplicate_service import analyze_duplicates
from services.settings_service import load_settings

from services.listening_history_service import (
    export_listening_memory as export_listening_memory_service,
    clear_listening_memory as clear_listening_memory_service,
)

from services.playlist_intelligence_service import (
    export_playlist_report as export_playlist_report_service,
)

from gui.image_loader import (
    clear_image_cache,
    cache_size,
)

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

        self.current_track_id = None
        self.current_track_metadata = {}

        self.current_track_rating = 0

        self.history_active_track_key = None
        self.history_active_duration_ms = 0
        self.history_active_max_progress_ms = 0
        self.history_active_last_progress_ms = 0
        self.history_active_started_at = None
        self.history_previous_track_key = None

        self.last_current_playback = None

        self.cached_playlist = None
        self.cached_tracks = []
        self.last_playlist_refresh_at = 0
        self.playlist_refresh_interval = 8

        self.analytics_cache = {}
        self.duplicates_cache = {}
        self.max_page_cache_items = 10
        self.analytics_cache_ttl = 20

        self.search_thread = None
        self.search_worker = None

        self.page_animation = None
        self.page_animation_widget = None

        self.setWindowTitle("Spotify Power Tools")
        self.resize(1600, 950)
        self.setMinimumSize(1500, 900)
        self.setStyleSheet(APP_STYLE)

        central = QWidget()
        central.setObjectName("AppRoot")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.header = Header()
        self.header.setVisible(False)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.setVisible(False)


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
        self.status_bar.setVisible(False)

        root_layout.addWidget(self.header)
        root_layout.addWidget(body, 1)
        root_layout.addWidget(self.status_bar)

        self.film_grain_overlay = FilmGrainOverlay(
            central,
            opacity=0.14,
            tile_size=180
        )

        self.film_grain_overlay.raise_()

        self.dashboard.shuffle_panel.update_queue_button_text()
        self.apply_saved_settings(
            load_settings(),
            show_message=False
        )

        QTimer.singleShot(
            800,
            self.load_spotify_user_profile
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

        self.dashboard.bridge.pageRequested.connect(
            self.handle_web_page_request
        )

        self.settings_page.settings_saved.connect(
            self.apply_saved_settings
        )

        self.settings_page.memory_export_requested.connect(
            self.export_listening_memory
        )

        self.settings_page.memory_clear_requested.connect(
            self.clear_listening_memory
        )

        self.settings_page.image_cache_clear_requested.connect(
            self.clear_album_art_cache
        )

        self.analytics_page.profile_apply_requested.connect(
            self.apply_recommended_profile
        )

        self.analytics_page.report_export_requested.connect(
            self.export_playlist_report
        )

        self.analytics_page.share_card_export_requested.connect(
            self.export_share_card
        )

        self.duplicates_page.clean_requested.connect(
            self.create_cleaned_playlist
        )

        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self.slow_timer = QTimer(self)
        self.slow_timer.timeout.connect(self.slow_refresh)
        self.slow_timer.start(8000)

        QTimer.singleShot(
            300,
            self.slow_refresh
        )

        self.dashboard.shuffle_panel.preview_button.clicked.connect(
            self.preview_shuffle
        )

        self.dashboard.shuffle_panel.apply_button.clicked.connect(
            self.queue_shuffle
        )

        self.queue_page.refresh_requested.connect(
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

        self.dashboard.current_song_card.rating_changed.connect(
            self.set_song_rating
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

    def load_spotify_user_profile(self):
        try:
            profile = self.controller.get_current_user_profile()

            self.dashboard.update_user_profile(
                profile
            )

        except Exception as error:
            print(
                f"Could not load Spotify user profile: {error}"
            )

    def closeEvent(self, event):

        try:

            for index in range(self.stack.count()):

                page = self.stack.widget(index)

                if page is not None and hasattr(page, "web_view"):

                    try:
                        page.web_view.setHtml("")
                        page.web_view.setParent(None)
                        page.web_view.deleteLater()

                    except RuntimeError:
                        pass

        except RuntimeError:
            pass

        super().closeEvent(event)

    def show_dashboard(self):

        self.sidebar.set_active_button(
            self.sidebar.dashboard_btn
        )

        self.set_page(
            self.dashboard
        )

        self.status_bar.set_message(
            "Dashboard"
        )

        QTimer.singleShot(
            0,
            self.load_dashboard_playlist
        )

    def show_smart_shuffle(self):

        self.sidebar.set_active_button(
            self.sidebar.shuffle_btn
        )

        self.set_page(
            self.dashboard
        )

        self.dashboard.shuffle_panel.highlight()

        self.dashboard.shuffle_panel.preview_button.setFocus()

        self.status_bar.set_message(
            "Smart Shuffle selected"
        )

    def handle_web_page_request(self, page_name):

        page_name = str(page_name or "").lower().strip()

        handlers = {
            "dashboard": self.show_dashboard,
            "smart_shuffle": self.show_smart_shuffle,
            "shuffle": self.show_smart_shuffle,
            "analytics": self.show_analytics,
            "queue": self.show_queue,
            "search": self.show_search,
            "duplicates": self.show_duplicates,
            "settings": self.show_settings,
            "about": self.show_about,
        }

        handler = handlers.get(page_name)

        if handler is None:
            return

        handler()

    def show_analytics(self):

        self.sidebar.set_active_button(
            self.sidebar.analytics_btn
        )

        self.set_page(
            self.analytics_page
        )

        self.status_bar.set_message(
            "Analytics • Loading..."
        )

        QTimer.singleShot(
            0,
            self.load_analytics_page
        )

    def show_duplicates(self):

        self.sidebar.set_active_button(
            self.sidebar.duplicates_btn
        )

        self.set_page(
            self.duplicates_page
        )

        self.status_bar.set_message(
            "Duplicates • Loading..."
        )

        QTimer.singleShot(
            0,
            self.load_duplicates_page
        )

    def show_queue(self):

        self.sidebar.set_active_button(
            self.sidebar.queue_btn
        )

        self.set_page(
            self.queue_page
        )

        self.refresh_queue_page()

    def show_search(self):

        self.sidebar.set_active_button(
            self.sidebar.search_btn
        )

        self.set_page(
            self.search_page
        )

        self.status_bar.set_message(
            "Search Spotify"
        )

    def search_tracks(self, query):

        query = str(query or "").strip()

        if not query:
            self.search_page.clear_results()
            self.status_bar.set_message(
                "Search Spotify"
            )
            return

        self.search_page.set_loading(
            True,
            query=query
        )

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

        self.search_worker.error.connect(
            self.search_thread.quit
        )

        self.search_thread.finished.connect(
            self.search_thread.deleteLater
        )

        self.search_thread.start()

    def search_finished(self, query, songs):

        self.search_page.show_results(
            query,
            songs
        )

        if query != self.search_page.active_query:
            return

        self.status_bar.set_message(
            f"Search complete • {len(songs)} results"
        )

    def search_error(self, query, message):

        self.search_page.show_search_error(
            query,
            message
        )

        if query != self.search_page.active_query:
            return

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

        self.set_page(
            self.settings_page
        )

        self.status_bar.set_message(
            "Settings"
        )

    def show_about(self):

        self.sidebar.set_active_button(
            self.sidebar.about_btn
        )

        self.set_page(
            self.about_page
        )

        self.status_bar.set_message(
            "About Spotify Power Tools"
        )

    def apply_saved_settings(self, settings, show_message=True):

        self.dashboard.shuffle_panel.apply_settings(
            settings
        )

        if hasattr(
                self.dashboard.shuffle_panel,
                "update_queue_button_text"
        ):
            self.dashboard.shuffle_panel.update_queue_button_text()

        self.dashboard.update_active_profile(
            settings
        )

        if show_message:
            self.status_bar.set_message(
                "Settings saved"
            )

    def animate_page(self, widget):

        if self.page_animation is not None:

            self.page_animation.stop()

            if self.page_animation_widget is not None:
                self.page_animation_widget.setGraphicsEffect(None)

        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(0.0)

        widget.setGraphicsEffect(
            effect
        )

        animation = QPropertyAnimation(
            effect,
            b"opacity",
            self
        )

        animation.setDuration(
            230
        )

        animation.setStartValue(
            0.0
        )

        animation.setEndValue(
            1.0
        )

        animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        animation.finished.connect(
            lambda: widget.setGraphicsEffect(None)
        )

        self.page_animation = animation
        self.page_animation_widget = widget

        animation.start()

    def set_page(self, widget):

        if self.stack.currentWidget() != widget:
            self.stack.setCurrentWidget(
                widget
            )

        self.sidebar.setVisible(
            widget != self.dashboard
        )

        # Important:
        # QWebEngineView can crash with QGraphicsEffect / opacity animation.
        # Skip animation for any page that owns a web_view.
        if hasattr(widget, "web_view"):

            if hasattr(self, "film_grain_overlay"):
                self.film_grain_overlay.raise_()

            return

        self.animate_page(
            widget
        )

        if hasattr(self, "film_grain_overlay"):
            self.film_grain_overlay.raise_()

    def apply_recommended_profile(self, profile_name):

        applied = self.dashboard.shuffle_panel.set_profile(
            profile_name
        )

        if not applied:
            QMessageBox.warning(
                self,
                "Profile Not Found",
                f"Could not apply profile: {profile_name}"
            )

            return

        self.sidebar.set_active_button(
            self.sidebar.dashboard_btn
        )

        self.set_page(
            self.dashboard
        )

        self.dashboard.shuffle_panel.highlight()
        self.dashboard.update_active_profile(
            profile_name
        )

        self.status_bar.set_message(
            f"Applied recommended profile: {profile_name}"
        )

    def export_playlist_report(self):

        try:
            self.update_cached_playlist(
                force=False
            )

            playlist = self.cached_playlist
            tracks = self.cached_tracks

            analytics = self.get_cached_analytics(
                playlist,
                tracks
            )

            report_path = export_playlist_report_service(
                playlist,
                analytics
            )

            self.status_bar.set_message(
                f"Playlist report exported: {report_path}"
            )

            QMessageBox.information(
                self,
                "Playlist Report Exported",
                f"Exported playlist report to:\n\n{report_path}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Report Export Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to export playlist report"
            )

    def export_share_card(self, theme_name):

        try:
            self.update_cached_playlist(
                force=False
            )

            playlist = self.cached_playlist
            tracks = self.cached_tracks

            analytics = self.get_cached_analytics(
                playlist,
                tracks
            )

            project_root = Path(__file__).resolve().parents[2]

            output_dir = project_root / "data" / "share_cards"

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            timestamp = datetime.now(
                timezone.utc
            ).strftime("%Y%m%d_%H%M%S")

            output_path = output_dir / f"playlist_share_card_{timestamp}.png"

            share_card = ShareCardWidget(
                theme_name=theme_name
            )

            share_card.update_data(
                playlist,
                analytics
            )

            saved = share_card.save_to_png(
                str(output_path)
            )

            share_card.deleteLater()

            if not saved:
                raise RuntimeError(
                    "Could not save share card image."
                )

            self.status_bar.set_message(
                f"Share card exported: {output_path}"
            )

            reply = QMessageBox.question(
                self,
                "Share Card Exported",
                (
                    f"Exported share card to:\n\n"
                    f"{output_path}\n\n"
                    f"Open the image now?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                webbrowser.open(
                    output_path.as_uri()
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Share Card Export Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to export share card"
            )

    def clear_analysis_caches(self):

        self.analytics_cache.clear()

        QTimer.singleShot(
            0,
            self.slow_refresh
        )

        self.duplicates_cache.clear()

    def export_listening_memory(self):

        try:
            export_path = export_listening_memory_service()

            self.status_bar.set_message(
                f"Listening memory exported: {export_path}"
            )

            QMessageBox.information(
                self,
                "Listening Memory Exported",
                f"Exported listening memory to:\n\n{export_path}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to export listening memory"
            )

    def clear_listening_memory(self):

        reply = QMessageBox.question(
            self,
            "Clear Listening Memory",
            (
                "This will erase local listening memory, including skips, "
                "finishes, replays, and streak data.\n\n"
                "Spotify playlists and ratings will not be modified.\n\n"
                "Continue?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            clear_listening_memory_service()

            self.clear_analysis_caches()

            self.status_bar.set_message(
                "Listening memory cleared"
            )

            QMessageBox.information(
                self,
                "Listening Memory Cleared",
                "Local listening memory has been cleared."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Clear Memory Error",
                str(error)
            )

            self.status_bar.set_message(
                "           Failed to clear listening memory"
            )

    def clear_album_art_cache(self):

        try:
            size_before = cache_size()

            clear_image_cache()

            self.status_bar.set_message(
                "Album art cache cleared"
            )

            QMessageBox.information(
                self,
                "Album Art Cache Cleared",
                (
                    "Album art cache has been cleared.\n\n"
                    f"Original images cleared: {size_before.get('original', 0)}\n"
                    f"Scaled images cleared: {size_before.get('scaled', 0)}"
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Cache Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to clear album art cache"
            )

    def trim_page_cache(self, cache):

        while len(cache) > self.max_page_cache_items:
            oldest_key = next(iter(cache))
            del cache[oldest_key]

    def make_playlist_cache_key(self, playlist, tracks):

        tracks = tracks or []

        if playlist is None:
            return (
                "none",
                0
            )

        return (
            playlist.get("id", ""),
            playlist.get("snapshot_id", ""),
            len(tracks),
        )

    def get_cached_analytics(self, playlist, tracks):

        cache_key = self.make_playlist_cache_key(
            playlist,
            tracks
        )

        now = time.monotonic()

        cached = self.analytics_cache.get(
            cache_key
        )

        if cached is not None:

            age = now - cached["created_at"]

            if age < self.analytics_cache_ttl:
                return cached["analytics"]

        analytics = calculate_playlist_analytics(
            tracks
        )

        self.analytics_cache[cache_key] = {
            "created_at": now,
            "analytics": analytics,
        }

        self.trim_page_cache(
            self.analytics_cache
        )

        return analytics

    def get_cached_duplicates(self, playlist, tracks):

        cache_key = self.make_playlist_cache_key(
            playlist,
            tracks
        )

        if cache_key in self.duplicates_cache:
            return self.duplicates_cache[cache_key]

        analysis = analyze_duplicates(
            tracks
        )

        self.duplicates_cache[cache_key] = analysis

        self.trim_page_cache(
            self.duplicates_cache
        )

        return analysis

    def update_cached_playlist(self, force=False):

        now = time.monotonic()

        cache_is_fresh = (
                self.last_playlist_refresh_at > 0
                and now - self.last_playlist_refresh_at < self.playlist_refresh_interval
        )

        if not force and cache_is_fresh:
            return self.cached_playlist, self.cached_tracks

        current = self.last_current_playback

        if current is None:
            self.cached_playlist = None
            self.cached_tracks = []
            self.last_playlist_refresh_at = now

            return self.cached_playlist, self.cached_tracks

        playlist, tracks = self.controller.current_playlist(
            current
        )

        self.cached_playlist = playlist
        self.cached_tracks = tracks
        self.last_playlist_refresh_at = now

        return playlist, tracks

    def update_dashboard_playlist_from_cache(self):

        playlist = self.cached_playlist
        tracks = self.cached_tracks

        if hasattr(self.dashboard, "update_playlist_summary"):
            self.dashboard.update_playlist_summary(
                playlist,
                tracks
            )

        self.dashboard.playlist_card.update_playlist(
            playlist,
            tracks
        )

        if playlist is not None and tracks:

            analytics = self.get_cached_analytics(
                playlist,
                tracks
            )

            if hasattr(self.dashboard, "update_analytics_summary"):
                self.dashboard.update_analytics_summary(
                    analytics
                )

        else:

            if hasattr(self.dashboard, "update_analytics_summary"):
                self.dashboard.update_analytics_summary(
                    {}
                )

        if self.stack.currentWidget() != self.dashboard:
            return

        if playlist is not None:
            self.status_bar.set_message(
                f"Connected • Playlist: {playlist['name']} • {len(tracks)} songs"
            )
        else:
            self.status_bar.set_message(
                "Connected • No playlist currently playing"
            )

    def update_analytics_from_cache(self):

        playlist = self.cached_playlist
        tracks = self.cached_tracks

        analytics = self.get_cached_analytics(
            playlist,
            tracks
        )

        self.analytics_page.update_from_analytics(
            playlist,
            analytics
        )

        if hasattr(self.dashboard, "update_analytics_summary"):
            self.dashboard.update_analytics_summary(
                analytics
            )

        if playlist is not None:
            self.status_bar.set_message(
                f"Analytics • {playlist['name']}"
            )
        else:
            self.status_bar.set_message(
                "Analytics • No playlist currently playing"
            )

    def update_duplicates_from_cache(self):

        if self.duplicates_page.is_busy:
            return

        playlist = self.cached_playlist
        tracks = self.cached_tracks

        analysis = self.get_cached_duplicates(
            playlist,
            tracks
        )

        self.duplicates_page.update_from_analysis(
            playlist,
            analysis
        )

        if playlist is not None:
            self.status_bar.set_message(
                f"Duplicates • {playlist['name']}"
            )
        else:
            self.status_bar.set_message(
                "Duplicates • No playlist currently playing"
            )

    def load_dashboard_playlist(self):

        self.update_cached_playlist(
            force=False
        )

        self.update_dashboard_playlist_from_cache()

    def load_analytics_page(self):

        self.update_cached_playlist(
            force=False
        )

        self.update_analytics_from_cache()

    def load_duplicates_page(self):

        self.update_cached_playlist(
            force=False
        )

        self.update_duplicates_from_cache()

    def slow_refresh(self):

        try:
            self.update_cached_playlist(
                force=True
            )

            current_page = self.stack.currentWidget()

            if current_page == self.dashboard:

                self.update_dashboard_playlist_from_cache()

            elif current_page == self.analytics_page:

                self.update_analytics_from_cache()

            elif current_page == self.duplicates_page:

                self.update_duplicates_from_cache()

        except Exception as error:

            self.status_bar.set_message(
                f"Slow refresh error: {error}"
            )

    def record_listening_history(self, current):

        if current is None:
            return

        if not current.get("is_playing"):
            return

        track = current.get(
            "item"
        )

        if track is None:
            return

        track_key = (
                track.get("id")
                or track.get("uri")
                or ""
        )

        if not track_key:
            return

        progress_ms = current.get(
            "progress_ms",
            0
        )

        if progress_ms is None:
            progress_ms = 0

        duration_ms = track.get(
            "duration_ms",
            0
        )

        if duration_ms is None:
            duration_ms = 0

        now = time.monotonic()

        # First track seen by the memory engine
        if self.history_active_track_key is None:

            self.history_active_track_key = track_key
            self.history_active_duration_ms = duration_ms
            self.history_active_max_progress_ms = progress_ms
            self.history_active_last_progress_ms = progress_ms
            self.history_active_started_at = now

            try:
                self.controller.record_track_started(
                    track,
                    previous_track_key=self.history_previous_track_key
                )

            except Exception:
                pass

            return

        # Same track is still playing
        if track_key == self.history_active_track_key:

            # Detect repeat-track behavior:
            # progress drops from near the end back near the beginning.
            progress_dropped = (
                    self.history_active_last_progress_ms - progress_ms
            )

            repeated_same_track = (
                    duration_ms > 0
                    and progress_dropped > 10000
                    and self.history_active_last_progress_ms > duration_ms * 0.70
                    and progress_ms < duration_ms * 0.25
            )

            if repeated_same_track:

                played_ms = int(
                    (now - self.history_active_started_at) * 1000
                )

                try:
                    self.controller.finalize_track_play(
                        self.history_active_track_key,
                        duration_ms=self.history_active_duration_ms,
                        max_progress_ms=self.history_active_max_progress_ms,
                        last_progress_ms=self.history_active_last_progress_ms,
                        played_ms=played_ms
                    )

                    self.controller.record_track_started(
                        track,
                        previous_track_key=self.history_active_track_key
                    )

                except Exception:
                    pass

                self.history_previous_track_key = self.history_active_track_key
                self.history_active_track_key = track_key
                self.history_active_duration_ms = duration_ms
                self.history_active_max_progress_ms = progress_ms
                self.history_active_last_progress_ms = progress_ms
                self.history_active_started_at = now

                return

            self.history_active_max_progress_ms = max(
                self.history_active_max_progress_ms,
                progress_ms
            )

            self.history_active_last_progress_ms = progress_ms

            return

        # Song changed: finalize previous track, then start new track.
        played_ms = int(
            (now - self.history_active_started_at) * 1000
        )

        try:
            self.controller.finalize_track_play(
                self.history_active_track_key,
                duration_ms=self.history_active_duration_ms,
                max_progress_ms=self.history_active_max_progress_ms,
                last_progress_ms=self.history_active_last_progress_ms,
                played_ms=played_ms
            )

        except Exception:
            pass

        self.history_previous_track_key = self.history_active_track_key

        self.history_active_track_key = track_key
        self.history_active_duration_ms = duration_ms
        self.history_active_max_progress_ms = progress_ms
        self.history_active_last_progress_ms = progress_ms
        self.history_active_started_at = now

        try:
            self.controller.record_track_started(
                track,
                previous_track_key=self.history_previous_track_key
            )

        except Exception:
            pass

    def update_current_track_rating(self, current):

        if current is None:
            self.current_track_rating = 0

            return

        track = current.get(
            "item"
        )

        if track is None:
            self.current_track_rating = 0

            return

        track_id = (
                track.get("id")
                or track.get("uri")
                or ""
        )

        if not track_id:
            self.current_track_rating = 0

            return

        self.current_track_rating = self.controller.get_song_rating(
            track_id
        )

    def update_current_track_metadata(self, current):

        if current is None:
            self.current_track_id = None
            self.current_track_metadata = {}

            return

        track = current.get(
            "item"
        )

        if track is None:
            self.current_track_id = None
            self.current_track_metadata = {}

            return

        track_key = (
                track.get("id")
                or track.get("uri")
                or track.get("name")
        )

        if not track_key:
            self.current_track_id = None
            self.current_track_metadata = {}

            return

        if track_key == self.current_track_id:
            return

        self.current_track_id = track_key

        try:
            self.current_track_metadata = self.controller.get_track_metadata(
                track
            )



        except Exception as error:


            self.current_track_metadata = {}

    def refresh(self):

        try:
            current = self.controller.current_playback()

            self.last_current_playback = current

            self.header.set_connected(
                current is not None
            )

            self.record_listening_history(
                current
            )

            current_page = self.stack.currentWidget()

            if current_page != self.dashboard:
                return

            self.update_current_track_metadata(
                current
            )

            self.update_current_track_rating(
                current
            )

            if current is not None and current.get("item") is not None:

                popularity = self.current_track_metadata.get(
                    "popularity"
                )

                if popularity is not None and popularity != "Unavailable":
                    current["item"]["popularity"] = popularity

            self.dashboard.current_song_card.update_song(
                current,
                self.current_track_metadata,
                self.current_track_rating
            )

            self.dashboard.player_controls_card.update_playback_state(
                current
            )

            if current is None:
                self.status_bar.set_message(
                    "Spotify not currently playing"
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

            QTimer.singleShot(
                300,
                self.slow_refresh
            )

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

            QTimer.singleShot(
                300,
                self.slow_refresh
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Playback Error",
                str(error)
            )

    def set_song_rating(self, track_id, rating, song_name, artist):

        try:
            result = self.controller.set_song_rating(
                track_id,
                rating,
                song_name,
                artist
            )

            self.current_track_rating = result["rating"]

            self.dashboard.current_song_card.update_rating(
                result["rating"]
            )

            self.analytics_cache.clear()

            if result["rating"] == 0:

                self.status_bar.set_message(
                    f"Rating cleared • {song_name}"
                )

            else:

                self.status_bar.set_message(
                    f"Rated {song_name} • {result['rating']}/5"
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Rating Error",
                str(error)
            )

            self.status_bar.set_message(
                "Failed to save rating"
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

            QTimer.singleShot(
                300,
                self.slow_refresh
            )

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

            QTimer.singleShot(
                300,
                self.slow_refresh
            )

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

            QTimer.singleShot(
                300,
                self.slow_refresh
            )

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

        self.dashboard.shuffle_panel.set_preview_ready()

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

        self.dashboard.shuffle_panel.set_queue_idle()

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