import json
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.current_song_card import CurrentSongCard
from gui.player_controls_card import PlayerControlsCard
from gui.playlist_card import PlaylistCard
from gui.shuffle_panel import ShufflePanel
from gui.web_dashboard_bridge import WebDashboardBridge


def format_duration(total_ms):
    total_ms = int(total_ms or 0)

    total_seconds = total_ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def format_time(ms):
    ms = int(ms or 0)

    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:02d}"


def get_time_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "good morning"

    if 12 <= hour < 17:
        return "good afternoon"

    if 17 <= hour < 22:
        return "good evening"

    return "late night"


def safe_song_dict(item):
    if isinstance(item, dict):
        song = item.get("song")
        score = item.get("score")
        reasons = item.get("reasons", [])
    else:
        song = item
        score = None
        reasons = []

    if song is None:
        return None

    return {
        "name": getattr(song, "name", "Unknown Song"),
        "artist": getattr(song, "artist", "Unknown Artist"),
        "album": getattr(song, "album", ""),
        "score": round(float(score or 0), 1) if score is not None else None,
        "reasons": list(reasons or [])[:4],
    }


def first_existing(data, *keys, default=None):
    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)

        if value not in (None, "", [], {}):
            return value

    return default


def as_number(value):
    try:
        if value is None:
            return None

        return float(value)

    except (TypeError, ValueError):
        return None


def as_percent(value):
    number = as_number(value)

    if number is None:
        return None

    if 0 <= number <= 1:
        number *= 100

    return round(number)


def as_rating(value):
    number = as_number(value)

    if number is None:
        return None

    return round(number, 1)


def extract_text(value):
    if value in (None, "", [], {}):
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        for key in [
            "value",
            "title",
            "name",
            "track",
            "track_name",
            "song",
            "song_name",
            "label",
            "text",
        ]:
            item = value.get(key)

            if item not in (None, "", [], {}):
                return extract_text(item)

        return ""

    if isinstance(value, list) and value:
        return extract_text(value[0])

    return str(value)


def normalize_badges(value):
    if value in (None, "", [], {}):
        return []

    if isinstance(value, dict):
        value = list(value.values())

    if not isinstance(value, list):
        value = [value]

    badges = []

    for badge in value:
        if isinstance(badge, dict):
            label = (
                badge.get("title")
                or badge.get("label")
                or badge.get("name")
                or badge.get("text")
                or badge.get("description")
                or ""
            )
        else:
            label = str(badge)

        if label:
            badges.append(label)

    return badges


def wrapped_card_name(card):
    if not isinstance(card, dict):
        return extract_text(card)

    for key in [
        "value",
        "title",
        "name",
        "track_name",
        "song_name",
        "song",
        "primary",
        "headline",
    ]:
        value = card.get(key)

        if value not in (None, "", [], {}):
            return extract_text(value)

    return ""


def normalize_identity_title(title):
    title = str(title or "").strip()

    if not title:
        return ""

    return title


def normalize_identity_subtitle(subtitle):
    subtitle = str(subtitle or "").strip()

    if not subtitle:
        return ""

    return subtitle


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("Dashboard")

        self.web_ready = False

        self.latest_now_playing = None
        self.latest_playlist_summary = None
        self.latest_preview_tracks = []
        self.latest_identity_summary = None
        self.latest_stats_summary = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebDashboardView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True
        )

        self.bridge = WebDashboardBridge()

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("dashboardBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(self.on_web_loaded)

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "dashboard.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(self.web_view)

        self.create_compatibility_widgets()
        self.connect_bridge()

    def create_compatibility_widgets(self):
        self.current_song_card = CurrentSongCard()
        self.current_song_card.setVisible(False)

        self.player_controls_card = PlayerControlsCard()
        self.player_controls_card.setVisible(False)

        self.playlist_card = PlaylistCard()
        self.playlist_card.setVisible(False)

        self.shuffle_panel = ShufflePanel()
        self.shuffle_panel.setVisible(False)

        self.preview_panel = self.shuffle_panel

        self.wrap_current_song_methods()
        self.wrap_playlist_methods()
        self.wrap_shuffle_methods()

    def connect_bridge(self):
        self.bridge.previousRequested.connect(
            self.current_song_card.previous_button.click
        )

        self.bridge.playPauseRequested.connect(
            self.current_song_card.play_pause_button.click
        )

        self.bridge.nextRequested.connect(
            self.current_song_card.next_button.click
        )

        self.bridge.previewRequested.connect(
            self.shuffle_panel.preview_button.click
        )

        self.bridge.queueRequested.connect(
            self.shuffle_panel.apply_button.click
        )

        self.bridge.ratingRequested.connect(
            self.current_song_card.emit_rating_changed
        )

        self.bridge.seekRequested.connect(
            self.seek_from_web
        )

    def seek_from_web(self, fraction):
        fraction = max(0.0, min(1.0, float(fraction or 0)))

        slider = self.current_song_card.progress_slider
        maximum = slider.maximum()

        if maximum <= 0:
            return

        slider.setValue(
            int(maximum * fraction)
        )

        slider.sliderReleased.emit()

    def wrap_current_song_methods(self):
        original_update_song = self.current_song_card.update_song
        original_update_rating = self.current_song_card.update_rating

        def update_song_proxy(current, track_metadata=None, rating=0):
            original_update_song(
                current,
                track_metadata,
                rating
            )

            self.update_web_now_playing(
                current,
                track_metadata or {},
                rating
            )

        def update_rating_proxy(rating):
            original_update_rating(rating)

            self.run_js_function(
                "window.dashboard.setRating",
                int(rating or 0)
            )

        self.current_song_card.update_song = update_song_proxy
        self.current_song_card.update_rating = update_rating_proxy

    def wrap_playlist_methods(self):
        original_update_playlist = self.playlist_card.update_playlist

        def update_playlist_proxy(playlist, tracks):
            original_update_playlist(
                playlist,
                tracks
            )

            self.update_playlist_summary(
                playlist,
                tracks
            )

        self.playlist_card.update_playlist = update_playlist_proxy

    def wrap_shuffle_methods(self):
        original_show_tracks = self.shuffle_panel.show_tracks

        def show_tracks_proxy(tracks):
            original_show_tracks(tracks)
            self.update_web_preview(tracks)

        self.shuffle_panel.show_tracks = show_tracks_proxy

        if hasattr(self.shuffle_panel, "set_preview_loading"):
            original_loading = self.shuffle_panel.set_preview_loading

            def loading_proxy():
                original_loading()

                self.run_js_function(
                    "window.dashboard.setPreviewState",
                    {
                        "state": "loading",
                        "buttonText": "generating...",
                        "queueEnabled": False,
                    }
                )

            self.shuffle_panel.set_preview_loading = loading_proxy

        if hasattr(self.shuffle_panel, "set_preview_ready"):
            original_ready = self.shuffle_panel.set_preview_ready

            def ready_proxy():
                original_ready()

                self.run_js_function(
                    "window.dashboard.setPreviewState",
                    {
                        "state": "ready",
                        "buttonText": "preview",
                        "queueEnabled": True,
                    }
                )

            self.shuffle_panel.set_preview_ready = ready_proxy

        if hasattr(self.shuffle_panel, "set_preview_failed"):
            original_failed = self.shuffle_panel.set_preview_failed

            def failed_proxy():
                original_failed()

                self.run_js_function(
                    "window.dashboard.setPreviewState",
                    {
                        "state": "failed",
                        "buttonText": "preview",
                        "queueEnabled": False,
                    }
                )

            self.shuffle_panel.set_preview_failed = failed_proxy

        if hasattr(self.shuffle_panel, "set_queue_idle"):
            original_idle = self.shuffle_panel.set_queue_idle

            def idle_proxy():
                original_idle()

                self.run_js_function(
                    "window.dashboard.setPreviewState",
                    {
                        "state": "ready",
                        "buttonText": "preview",
                        "queueEnabled": True,
                    }
                )

            self.shuffle_panel.set_queue_idle = idle_proxy

    def on_web_loaded(self, ok):
        self.web_ready = bool(ok)

        if not self.web_ready:
            return

        if self.latest_playlist_summary is not None:
            self.run_js_function(
                "window.dashboard.updatePlaylistSummary",
                self.latest_playlist_summary
            )

        if self.latest_stats_summary is not None:
            self.run_js_function(
                "window.dashboard.updateStats",
                self.latest_stats_summary
            )

        if self.latest_identity_summary is not None:
            self.run_js_function(
                "window.dashboard.updateIdentity",
                self.latest_identity_summary
            )

        if self.latest_now_playing is not None:
            self.run_js_function(
                "window.dashboard.updateNowPlaying",
                self.latest_now_playing
            )

        self.run_js_function(
            "window.dashboard.updatePreview",
            self.latest_preview_tracks
        )

    def run_js_function(self, function_name, payload):
        if not self.web_ready:
            return

        js_payload = json.dumps(
            payload,
            ensure_ascii=False
        )

        self.web_view.page().runJavaScript(
            f"{function_name}({js_payload});"
        )

    def update_playlist_summary(self, playlist, tracks):
        tracks = tracks or []

        duration_ms = sum(
            getattr(track, "duration_ms", 0)
            for track in tracks
        )

        artists = len({
            getattr(track, "artist", "")
            for track in tracks
            if getattr(track, "artist", "")
        })

        albums = len({
            getattr(track, "album", "")
            for track in tracks
            if getattr(track, "album", "")
        })

        summary = {
            "greeting": get_time_greeting(),
            "playlistName": "<3",
            "trackCount": len(tracks),
            "duration": format_duration(duration_ms),
            "lastSynced": "just now",
            "artists": artists,
            "albums": albums,
        }

        stats = {
            "items": [
                {
                    "value": len(tracks),
                    "label": "TRACKS",
                },
                {
                    "value": artists,
                    "label": "ARTISTS",
                },
                {
                    "value": albums,
                    "label": "ALBUMS",
                },
                {
                    "value": format_duration(duration_ms),
                    "label": "DURATION",
                },
            ]
        }

        self.latest_playlist_summary = summary
        self.latest_stats_summary = stats

        self.run_js_function(
            "window.dashboard.updatePlaylistSummary",
            summary
        )

        self.run_js_function(
            "window.dashboard.updateStats",
            stats
        )

    def update_analytics_summary(self, analytics):
        analytics = analytics or {}

        glow = analytics.get(
            "analytics_glow",
            {}
        )

        intelligence = analytics.get(
            "playlist_intelligence",
            {}
        )

        listening = analytics.get(
            "listening_analytics",
            {}
        )

        personality = glow.get(
            "personality",
            {}
        )

        wrapped_cards = glow.get(
            "wrapped_cards",
            {}
        )

        identity_title = ""

        if isinstance(personality, dict):
            identity_title = first_existing(
                personality,
                "title",
                "name",
                "label",
                default=""
            )
        elif isinstance(personality, str):
            identity_title = personality

        identity_subtitle = ""

        if isinstance(personality, dict):
            identity_subtitle = first_existing(
                personality,
                "subtitle",
                "description",
                "summary",
                default=""
            )

        if not identity_subtitle:
            identity_subtitle = first_existing(
                glow,
                "subtitle",
                "description",
                "summary",
                default=""
            )

        aura_score = first_existing(
            glow,
            "aura_score",
            "score",
            default=None
        )

        aura_number = as_number(aura_score)

        if aura_number is not None:
            aura_number = round(aura_number)

        badges = normalize_badges(
            glow.get("badges", [])
        )

        hidden_favorite = wrapped_card_name(
            wrapped_cards.get("hidden_favorite", {})
        )

        if not hidden_favorite:
            hidden_favorite = extract_text(
                first_existing(
                    intelligence,
                    "hidden_favorite",
                    "hidden_favorites",
                    default=""
                )
            )

        playlist_villain = wrapped_card_name(
            wrapped_cards.get("playlist_villain", {})
        )

        if not playlist_villain:
            playlist_villain = extract_text(
                first_existing(
                    intelligence,
                    "playlist_villain",
                    "villain",
                    "most_skipped",
                    "cleanup_target",
                    default=""
                )
            )

        has_identity = any([
            identity_title,
            identity_subtitle,
            aura_number is not None,
            badges,
            hidden_favorite,
            playlist_villain,
        ])

        identity_payload = {
            "hasIdentity": has_identity,
            "identityTitle": normalize_identity_title(identity_title),
            "identitySubtitle": normalize_identity_subtitle(identity_subtitle),
            "auraScore": aura_number,
            "badges": badges[:3],
            "hiddenFavorite": hidden_favorite,
            "playlistVillain": playlist_villain,
        }

        self.latest_identity_summary = identity_payload

        self.run_js_function(
            "window.dashboard.updateIdentity",
            identity_payload
        )

        total_songs = analytics.get(
            "total_songs"
        )

        unique_artists = analytics.get(
            "unique_artists"
        )

        completion_rate = as_percent(
            first_existing(
                listening,
                "completion_rate",
                "finish_rate",
                "average_completion_rate",
                "avg_completion_rate",
                default=None
            )
        )

        avg_rating = as_rating(
            first_existing(
                analytics,
                "average_rating",
                "avg_rating",
                default=None
            )
        )

        stats_items = []

        if total_songs is not None:
            stats_items.append({
                "value": total_songs,
                "label": "TRACKS",
            })

        if completion_rate is not None:
            stats_items.append({
                "value": f"{completion_rate}%",
                "label": "COMPLETION RATE",
            })

        if avg_rating is not None:
            stats_items.append({
                "value": avg_rating,
                "label": "AVG RATING",
            })

        if unique_artists is not None:
            stats_items.append({
                "value": unique_artists,
                "label": "UNIQUE ARTISTS",
            })

        if len(stats_items) >= 4:
            stats_payload = {
                "items": stats_items[:4]
            }

            self.latest_stats_summary = stats_payload

            self.run_js_function(
                "window.dashboard.updateStats",
                stats_payload
            )

    def update_web_now_playing(self, current, track_metadata, rating):
        if current is None or current.get("item") is None:
            data = {
                "isPlaying": False,
                "title": "Nothing Playing",
                "artist": "",
                "album": "",
                "imageUrl": "",
                "progress": 0,
                "duration": 0,
                "progressFraction": 0,
                "progressLabel": "0:00",
                "durationLabel": "0:00",
                "rating": 0,
                "meta": "",
            }

            self.latest_now_playing = data

            self.run_js_function(
                "window.dashboard.updateNowPlaying",
                data
            )

            return

        track = current.get("item", {})
        album = track.get("album", {})
        artists = track.get("artists", [])

        image_url = ""

        images = album.get("images", [])

        if images:
            image_url = images[0].get("url", "")

        artist_name = "Unknown Artist"

        if artists:
            artist_name = artists[0].get(
                "name",
                "Unknown Artist"
            )

        duration_ms = track.get("duration_ms", 0) or 0
        progress_ms = current.get("progress_ms", 0) or 0

        explicit = "Explicit" if track.get("explicit", False) else "Clean"

        release = album.get("release_date", "")
        year = release[:4] if release else "Unknown"

        data = {
            "isPlaying": bool(current.get("is_playing")),
            "title": track.get("name", "Unknown Song"),
            "artist": artist_name,
            "album": album.get("name", "Unknown Album"),
            "imageUrl": image_url,
            "progress": progress_ms,
            "duration": duration_ms,
            "progressFraction": (
                progress_ms / duration_ms
                if duration_ms > 0
                else 0
            ),
            "progressLabel": format_time(progress_ms),
            "durationLabel": format_time(duration_ms),
            "rating": int(rating or 0),
            "meta": f"{explicit} • {year}",
        }

        self.latest_now_playing = data

        self.run_js_function(
            "window.dashboard.updateNowPlaying",
            data
        )

    def update_web_preview(self, tracks):
        items = []

        for item in tracks or []:
            song_data = safe_song_dict(item)

            if song_data is not None:
                items.append(song_data)

        self.latest_preview_tracks = items

        self.run_js_function(
            "window.dashboard.updatePreview",
            items
        )