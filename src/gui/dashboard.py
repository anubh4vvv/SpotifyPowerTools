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
from services.settings_service import load_settings


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
        self.latest_shuffle_settings = {
            "queueSize": 25,
            "profile": "Balanced",
        }
        saved_settings = load_settings()

        self.latest_app_context = {
            "profileName": "Spotify User",
            "profileImageUrl": "",
            "activeProfile": saved_settings.get(
                "shuffle_profile",
                "Balanced"
            ),
        }

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
        self.run_js_function(
            "window.dashboard.updateAppContext",
            self.latest_app_context
        )

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

        self.apply_dashboard_cleanup()
        self.push_shuffle_settings_to_web()

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

    def run_raw_js(self, code):
        if not self.web_ready:
            return

        self.web_view.page().runJavaScript(
            code
        )

    def apply_dashboard_cleanup(self):
        """
        Removes redundant dashboard-side navigation entries that no longer
        represent standalone pages.
        """

        self.run_raw_js(
            """
            (function () {
                const navItems = Array.from(
                    document.querySelectorAll(".nav-item")
                );

                navItems.forEach((item) => {
                    const text = String(
                        item.textContent || ""
                    ).toLowerCase();

                    if (text.includes("smart shuffle")) {
                        item.remove();
                    }
                });
            })();
            """
        )

    def update_shuffle_settings(self, settings):
        settings = settings or {}

        queue_size = settings.get(
            "queue_size",
            25
        )

        profile = settings.get(
            "shuffle_profile",
            "Balanced"
        )

        try:
            queue_size = int(
                queue_size
            )

        except Exception:
            queue_size = 25

        self.latest_shuffle_settings = {
            "queueSize": queue_size,
            "profile": str(profile or "Balanced"),
        }

        self.push_shuffle_settings_to_web()

    def push_shuffle_settings_to_web(self):
        if not self.web_ready:
            return

        payload = json.dumps(
            self.latest_shuffle_settings,
            ensure_ascii=False
        )

        self.run_raw_js(
            f"""
            (function () {{
                const data = {payload};

                const queueSize = Number(
                    data.queueSize || 25
                );

                const profile = String(
                    data.profile || "Balanced"
                );

                const queueButton = document.getElementById("queueBtn");

                if (queueButton) {{
                    queueButton.textContent =
                        `queue ${{queueSize}} tracks into spotify`;
                }}

                const badge = document.getElementById("shuffleBadge");

                if (badge) {{
                    badge.textContent = profile.toLowerCase();
                }}
            }})();
            """
        )

    def update_app_context(
            self,
            profile_name=None,
            profile_image_url=None,
            active_profile=None
    ):
        context = dict(
            self.latest_app_context or {}
        )

        if profile_name is not None:
            context["profileName"] = (
                    str(profile_name).strip()
                    or "Spotify User"
            )

        if profile_image_url is not None:
            context["profileImageUrl"] = (
                str(profile_image_url).strip()
            )

        if active_profile is not None:
            context["activeProfile"] = (
                    str(active_profile).strip()
                    or "Balanced"
            )

        self.latest_app_context = context

        self.run_js_function(
            "window.dashboard.updateAppContext",
            context
        )

    def update_user_profile(self, profile):
        profile = profile or {}

        self.update_app_context(
            profile_name=profile.get(
                "display_name",
                "Spotify User"
            ),
            profile_image_url=profile.get(
                "image_url",
                ""
            )
        )

    def update_active_profile(self, settings_or_profile):
        if isinstance(settings_or_profile, dict):
            profile_name = settings_or_profile.get(
                "shuffle_profile",
                "Balanced"
            )
        else:
            profile_name = settings_or_profile

        self.update_app_context(
            active_profile=profile_name
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

        def clean_text(value, fallback="—"):
            text = extract_text(
                value
            ).strip()

            if not text:
                return fallback

            blocked = {
                "n/a",
                "none",
                "not enough memory yet",
                "keep listening to unlock this",
                "unknown",
            }

            if text.lower() in blocked:
                return fallback

            return text

        def number_or_zero(value):
            number = as_number(
                value
            )

            if number is None:
                return 0

            return number

        def rounded_percent(value):
            number = number_or_zero(
                value
            )

            return round(
                max(0, min(100, number))
            )

        def first_named_item(items):
            if not items:
                return ""

            if isinstance(items, dict):
                items = list(
                    items.values()
                )

            if not isinstance(items, list):
                items = [
                    items
                ]

            if not items:
                return ""

            first = items[0]

            if isinstance(first, dict):
                name = (
                        first.get("name")
                        or first.get("song_name")
                        or first.get("track_name")
                        or first.get("title")
                        or first.get("value")
                        or ""
                )

                artist = (
                        first.get("artist")
                        or first.get("artist_name")
                        or ""
                )

                if name and artist:
                    return f"{name} — {artist}"

                if name:
                    return str(name)

                return clean_text(
                    first,
                    fallback=""
                )

            if isinstance(first, (list, tuple)) and first:
                return str(
                    first[0]
                )

            return str(
                first
            )

        def first_count_item(items):
            if not items:
                return "", 0

            if isinstance(items, dict):
                items = list(
                    items.items()
                )

            if not isinstance(items, list):
                return str(items), 0

            if not items:
                return "", 0

            first = items[0]

            if isinstance(first, dict):
                name = (
                        first.get("name")
                        or first.get("artist")
                        or first.get("album")
                        or first.get("title")
                        or first.get("value")
                        or ""
                )

                count = (
                        first.get("count")
                        or first.get("songs")
                        or first.get("total")
                        or 0
                )

                return str(name), int(count or 0)

            if isinstance(first, (list, tuple)):
                name = first[0] if len(first) >= 1 else ""
                count = first[1] if len(first) >= 2 else 0

                try:
                    count = int(
                        count
                    )

                except (TypeError, ValueError):
                    count = 0

                return str(name), count

            return str(first), 0

        total_songs = int(
            number_or_zero(
                analytics.get("total_songs")
            )
        )

        unique_artists = int(
            number_or_zero(
                analytics.get("unique_artists")
            )
        )

        health_score = rounded_percent(
            analytics.get("health_score")
        )

        diversity_score = rounded_percent(
            first_existing(
                analytics,
                "diversity_score",
                "artist_entropy_score",
                default=0
            )
        )

        variety_score = rounded_percent(
            first_existing(
                glow,
                "variety_score",
                default=diversity_score
            )
        )

        aura_score = rounded_percent(
            first_existing(
                glow,
                "aura_score",
                "score",
                default=health_score
            )
        )

        top_artist_name = clean_text(
            analytics.get("top_artist_name"),
            fallback=""
        )

        top_artist_count = int(
            number_or_zero(
                analytics.get("top_artist_count")
            )
        )

        if not top_artist_name:
            top_artist_name, top_artist_count = first_count_item(
                analytics.get("top_artists", [])
            )

        top_artist_percentage = rounded_percent(
            analytics.get("top_artist_percentage")
        )

        top_album_name = clean_text(
            analytics.get("top_album_name"),
            fallback=""
        )

        top_album_percentage = rounded_percent(
            analytics.get("top_album_percentage")
        )

        recommended_profile = clean_text(
            intelligence.get("recommended_profile"),
            fallback="Balanced"
        )

        recommendation_confidence = clean_text(
            intelligence.get("recommendation_confidence"),
            fallback="Low"
        )

        recommendation_reason = clean_text(
            intelligence.get("recommendation_reason"),
            fallback=""
        )

        completion_rate = rounded_percent(
            first_existing(
                listening,
                "global_completion_rate",
                "completion_rate",
                "finish_rate",
                default=0
            )
        )

        skip_rate = rounded_percent(
            first_existing(
                listening,
                "global_skip_rate",
                "skip_rate",
                default=0
            )
        )

        average_rating = as_rating(
            analytics.get("average_rating")
        )

        rated_percentage = rounded_percent(
            analytics.get("rated_percentage")
        )

        identity_title = ""

        if isinstance(personality, dict):
            identity_title = clean_text(
                first_existing(
                    personality,
                    "title",
                    "name",
                    "label",
                    default=""
                ),
                fallback=""
            )

        elif isinstance(personality, str):
            identity_title = personality

        if not identity_title:
            identity_title = "Playlist Intelligence"

        identity_subtitle = ""

        if isinstance(personality, dict):
            identity_subtitle = clean_text(
                first_existing(
                    personality,
                    "subtitle",
                    "description",
                    "summary",
                    default=""
                ),
                fallback=""
            )

        if not identity_subtitle:
            identity_subtitle = "Real playlist signals are being used to tune shuffle behavior."

        insight_parts = []

        if recommended_profile:
            insight_parts.append(
                f"Recommended: {recommended_profile} · {recommendation_confidence} confidence"
            )

        if top_artist_name:
            if top_artist_percentage > 0:
                insight_parts.append(
                    f"Top artist: {top_artist_name} · {top_artist_percentage}%"
                )
            elif top_artist_count > 0:
                insight_parts.append(
                    f"Top artist: {top_artist_name} · {top_artist_count} songs"
                )
            else:
                insight_parts.append(
                    f"Top artist: {top_artist_name}"
                )

        if variety_score > 0:
            insight_parts.append(
                f"Variety: {variety_score}%"
            )

        if completion_rate > 0 or skip_rate > 0:
            insight_parts.append(
                f"Completion {completion_rate}% · Skip {skip_rate}%"
            )

        if average_rating is not None and average_rating > 0:
            insight_parts.append(
                f"Rating: {average_rating}/5 across {rated_percentage}% rated"
            )

        if insight_parts:
            identity_subtitle = (
                    f"{identity_subtitle}\n"
                    + " · ".join(
                insight_parts[:3]
            )
            )

        hidden_favorite = first_named_item(
            intelligence.get("hidden_favorites", [])
        )

        if not hidden_favorite:
            hidden_favorite = clean_text(
                wrapped_card_name(
                    wrapped_cards.get("hidden_favorite", {})
                ),
                fallback="—"
            )

        playlist_villain = first_named_item(
            intelligence.get("cleanup_suggestions", [])
        )

        if not playlist_villain:
            playlist_villain = first_named_item(
                listening.get("most_skipped", [])
            )

        if not playlist_villain:
            playlist_villain = clean_text(
                wrapped_card_name(
                    wrapped_cards.get("playlist_villain", {})
                ),
                fallback="—"
            )

        badges = normalize_badges(
            glow.get("badges", [])
        )

        if not badges:
            if health_score >= 85:
                badges = [
                    "Excellent Health"
                ]
            elif diversity_score >= 70:
                badges = [
                    "Strong Variety"
                ]
            elif skip_rate >= 30:
                badges = [
                    "Skip Sensitive"
                ]
            elif recommended_profile:
                badges = [
                    f"{recommended_profile} Ready"
                ]

        has_identity = total_songs > 0 or any([
            identity_title,
            identity_subtitle,
            aura_score,
            badges,
            hidden_favorite != "—",
            playlist_villain != "—",
        ])

        identity_payload = {
            "hasIdentity": has_identity,
            "identityTitle": normalize_identity_title(
                identity_title
            ),
            "identitySubtitle": normalize_identity_subtitle(
                identity_subtitle
            ),
            "auraScore": aura_score if has_identity else None,
            "badges": badges[:3],
            "hiddenFavorite": hidden_favorite,
            "playlistVillain": playlist_villain,
            "recommendedProfile": recommended_profile,
            "recommendedConfidence": recommendation_confidence,
        }

        self.latest_identity_summary = identity_payload

        self.run_js_function(
            "window.dashboard.updateIdentity",
            identity_payload
        )

        rating_value = "—"

        if average_rating is not None and average_rating > 0:
            rating_value = average_rating

        stats_payload = {
            "items": [
                {
                    "value": total_songs,
                    "label": "TRACKS",
                },
                {
                    "value": f"{completion_rate}%",
                    "label": "COMPLETION RATE",
                },
                {
                    "value": rating_value,
                    "label": "AVG RATING",
                },
                {
                    "value": unique_artists,
                    "label": "UNIQUE ARTISTS",
                },
            ]
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