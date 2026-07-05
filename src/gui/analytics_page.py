import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot, Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout

from services.analytics_service import calculate_playlist_analytics
from services.playlist_doctor_service import (
    diagnose_playlist,
    get_rating_recommendations,
)


THEME_EXPORT_MAP = {
    "Golden Hour": "Golden Hour",
    "Late Night": "Late Night",
    "Rosewood": "Rosewood",

    # Backward compatibility if older names are passed from somewhere.
    "Aurora": "Golden Hour",
    "Midnight": "Late Night",
    "Neon Pop": "Rosewood",
}


def safe_get(data, key, default=None):
    if not isinstance(data, dict):
        return default

    value = data.get(key, default)

    if value in (None, "", [], {}):
        return default

    return value


def first_existing(data, keys, default=None):
    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)

        if value not in (None, "", [], {}):
            return value

    return default


def clamp_number(value, minimum=0, maximum=100):
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = 0

    return max(
        minimum,
        min(maximum, number)
    )


def percent_text(value):
    number = clamp_number(value)

    if number.is_integer():
        return f"{int(number)}%"

    return f"{round(number, 1)}%"


def simple_text(value, default="—"):
    if value in (None, "", [], {}):
        return default

    return str(value)


def card_value(card, fallback="—"):
    if not isinstance(card, dict):
        return simple_text(card, fallback)

    return simple_text(
        first_existing(
            card,
            [
                "value",
                "title",
                "name",
                "song_name",
                "track_name",
                "song",
                "headline",
            ],
            fallback
        ),
        fallback
    )


def card_subtitle(card, fallback=""):
    if not isinstance(card, dict):
        return ""

    return simple_text(
        first_existing(
            card,
            [
                "subtitle",
                "description",
                "artist",
                "meta",
                "reason",
            ],
            fallback
        ),
        fallback
    )


def normalize_bar_items(items, name_keys=None, value_keys=None, limit=5):
    name_keys = name_keys or [
        "name",
        "title",
        "song_name",
        "artist",
        "album",
        "label",
    ]

    value_keys = value_keys or [
        "value",
        "count",
        "plays",
        "replay_count",
        "skip_count",
        "rating",
    ]

    if not items:
        return []

    normalized = []

    for item in items[:limit]:
        if isinstance(item, tuple) and len(item) >= 2:
            name = item[0]
            value = item[1]

        elif isinstance(item, dict):
            name = first_existing(
                item,
                name_keys,
                "Unknown"
            )

            value = first_existing(
                item,
                value_keys,
                0
            )

            artist = item.get("artist")

            if artist and "song" in " ".join(name_keys):
                name = f"{name} — {artist}"

        else:
            name = str(item)
            value = 0

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            numeric_value = 0

        normalized.append({
            "name": simple_text(name, "Unknown"),
            "value": numeric_value,
            "displayValue": simple_text(value, "0"),
        })

    return normalized


def normalize_rating_tracks(items, limit=3):
    if not items:
        return []

    rows = []

    for item in items[:limit]:
        if isinstance(item, dict):
            name = item.get("name") or item.get("song_name") or "Unknown Song"
            artist = item.get("artist") or "Unknown Artist"
            rating = item.get("rating", 0)

            rows.append(
                f"{name} — {artist} ({rating}/5)"
            )

    return rows


def normalize_badges(badges, limit=4):
    if not badges:
        return []

    normalized = []

    for badge in badges[:limit]:
        if isinstance(badge, dict):
            normalized.append({
                "emoji": badge.get("emoji", "✨"),
                "title": badge.get("title", "Badge"),
                "description": badge.get("description", ""),
            })
        else:
            normalized.append({
                "emoji": "✨",
                "title": str(badge),
                "description": "",
            })

    return normalized


def normalize_track_rows(items, value_key, value_suffix="", limit=3):
    if not items:
        return []

    rows = []

    for item in items[:limit]:
        if not isinstance(item, dict):
            continue

        song = (
            item.get("song_name")
            or item.get("name")
            or item.get("track_name")
            or "Unknown Song"
        )

        artist = item.get("artist") or "Unknown Artist"
        value = item.get(value_key, 0)

        rows.append({
            "title": f"{song} — {artist}",
            "meta": f"{value}{value_suffix}",
            "value": value,
        })

    return rows


def normalize_cleanup_rows(items, limit=3):
    if not items:
        return []

    rows = []

    for item in items[:limit]:
        if not isinstance(item, dict):
            continue

        name = item.get("name") or item.get("song_name") or "Unknown Song"
        artist = item.get("artist") or "Unknown Artist"
        reason = item.get("reason") or "Cleanup candidate"

        rows.append({
            "title": f"{name} — {artist}",
            "meta": reason,
        })

    return rows


def normalize_hidden_favorites(items, limit=3):
    if not items:
        return []

    rows = []

    for item in items[:limit]:
        if not isinstance(item, dict):
            continue

        name = item.get("name") or item.get("song_name") or "Unknown Song"
        artist = item.get("artist") or "Unknown Artist"

        completion = item.get("completion_rate")
        skip = item.get("skip_rate")
        replay = item.get("replay_count")

        meta_parts = []

        if completion is not None:
            meta_parts.append(f"{completion}% completion")

        if skip is not None:
            meta_parts.append(f"{skip}% skip")

        if replay:
            meta_parts.append(f"replayed {replay}×")

        rows.append({
            "title": f"{name} — {artist}",
            "meta": " · ".join(meta_parts) or "Hidden favorite",
        })

    return rows


class AnalyticsBridge(QObject):
    applyProfileRequested = Signal(str)
    exportReportRequested = Signal()
    exportShareCardRequested = Signal(str)

    @Slot(str)
    def applyProfile(self, profile_name):
        self.applyProfileRequested.emit(
            str(profile_name or "Balanced")
        )

    @Slot()
    def exportReport(self):
        self.exportReportRequested.emit()

    @Slot(str)
    def exportShareCard(self, theme_name):
        display_theme = str(theme_name or "Golden Hour")

        export_theme = THEME_EXPORT_MAP.get(
            display_theme,
            display_theme
        )

        self.exportShareCardRequested.emit(
            export_theme
        )


class AnalyticsPage(QWidget):
    profile_apply_requested = Signal(str)
    report_export_requested = Signal()
    share_card_export_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("AnalyticsPage")

        self.web_ready = False
        self.latest_payload = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebAnalyticsView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True
        )

        self.bridge = AnalyticsBridge()

        self.bridge.applyProfileRequested.connect(
            self.profile_apply_requested.emit
        )

        self.bridge.exportReportRequested.connect(
            self.report_export_requested.emit
        )

        self.bridge.exportShareCardRequested.connect(
            self.share_card_export_requested.emit
        )

        self.channel = QWebChannel(self.web_view.page())
        self.channel.registerObject("analyticsBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self.web_view.loadFinished.connect(
            self.on_web_loaded
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "analytics.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(
            self.web_view
        )

    def on_web_loaded(self, ok):
        self.web_ready = bool(ok)

        if self.web_ready and self.latest_payload is not None:
            self.push_payload(
                self.latest_payload
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

    def push_payload(self, payload):
        self.run_js_function(
            "window.analytics.update",
            payload
        )

    def update_analytics(self, playlist, tracks):
        analytics = calculate_playlist_analytics(
            tracks
        )

        self.update_from_analytics(
            playlist,
            analytics
        )

    def update_from_analytics(self, playlist, analytics):
        analytics = analytics or {}
        playlist = playlist or {}

        payload = self.build_payload(
            playlist,
            analytics
        )

        self.latest_payload = payload

        self.push_payload(
            payload
        )

    def build_payload(self, playlist, analytics):
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

        wrapped = glow.get(
            "wrapped_cards",
            {}
        )

        personality = glow.get(
            "personality",
            {}
        )

        recommendation = intelligence.get(
            "recommendation",
            {}
        )

        recommended_profile = (
            intelligence.get("recommended_profile")
            or recommendation.get("profile")
            or intelligence.get("profile")
            or "Balanced"
        )

        recommendation_confidence = (
            intelligence.get("recommendation_confidence")
            or recommendation.get("confidence")
            or "Low"
        )

        recommendation_reason = (
            intelligence.get("recommendation_reason")
            or recommendation.get("reason")
            or intelligence.get("reason")
            or "Balanced is a safe default until more data is available."
        )

        doctor = diagnose_playlist(
            analytics
        )

        rating_recommendations = get_rating_recommendations(
            analytics
        )

        top_artist_card = wrapped.get("top_artist", {})
        most_replayed_card = wrapped.get("most_replayed", {})
        most_skipped_card = wrapped.get("most_skipped", {})
        hidden_favorite_card = wrapped.get("hidden_favorite", {})
        playlist_villain_card = wrapped.get("playlist_villain", {})
        playlist_mvp_card = wrapped.get("playlist_mvp", {})

        top_artists = normalize_bar_items(
            analytics.get("top_artists", []),
            name_keys=["name", "artist", "label"],
            value_keys=["count", "value"],
            limit=5
        )

        top_albums = normalize_bar_items(
            analytics.get("top_albums", []),
            name_keys=["name", "album", "label"],
            value_keys=["count", "value"],
            limit=5
        )

        rating_distribution = normalize_bar_items(
            analytics.get("rating_distribution", []),
            name_keys=["name", "label"],
            value_keys=["count", "value"],
            limit=5
        )

        cleanup_suggestions = normalize_cleanup_rows(
            intelligence.get("cleanup_suggestions", []),
            limit=3
        )

        hidden_favorites = normalize_hidden_favorites(
            intelligence.get("hidden_favorites", []),
            limit=3
        )

        most_replayed = normalize_track_rows(
            listening.get("most_replayed", []),
            "replay_count",
            " replays",
            limit=3
        )

        most_skipped = normalize_track_rows(
            listening.get("most_skipped", []),
            "skip_count",
            " skips",
            limit=3
        )

        top_rated = normalize_rating_tracks(
            analytics.get("top_rated_tracks", []),
            limit=3
        )

        low_rated = normalize_rating_tracks(
            analytics.get("low_rated_tracks", []),
            limit=3
        )

        streaks = listening.get(
            "streaks",
            {}
        )

        strengths = doctor.get(
            "strengths",
            []
        )

        warnings = doctor.get(
            "warnings",
            []
        )

        rating_tips = rating_recommendations.get(
            "recommendations",
            []
        )

        if not rating_tips:
            rating_tips = rating_recommendations.get(
                "tips",
                []
            )

        if not rating_tips:
            rating_tips = [
                f"{analytics.get('unrated_songs', 0)} songs are still unrated — rate more to sharpen personalization."
            ]

        return {
            "page": {
                "title": "Playlist Analytics",
                "subtitle": "Understand the health, balance, and listening memory of the playlist you're currently listening to.",
                "playlistName": playlist.get("name", ""),
            },

            "hero": {
                "title": safe_get(personality, "title", "Main Character Mix"),
                "emoji": safe_get(personality, "emoji", "✨"),
                "subtitle": safe_get(
                    personality,
                    "subtitle",
                    "Balanced vibes with enough personality to keep it moving."
                ),
                "recommendedProfile": recommended_profile,
                "confidence": recommendation_confidence,
                "auraScore": round(
                    clamp_number(
                        glow.get("aura_score", 0)
                    )
                ),
                "auraStatus": self.get_aura_status(
                    glow.get("aura_score", 0)
                ),
            },

            "tasteSignals": [
                {
                    "label": "Taste Match",
                    "value": percent_text(
                        glow.get("taste_match", 0)
                    ),
                    "percent": clamp_number(
                        glow.get("taste_match", 0)
                    ),
                },
                {
                    "label": "Variety",
                    "value": percent_text(
                        glow.get("variety_score", 0)
                    ),
                    "percent": clamp_number(
                        glow.get("variety_score", 0)
                    ),
                },
                {
                    "label": "Replay Energy",
                    "value": percent_text(
                        glow.get("replay_energy", 0)
                    ),
                    "percent": clamp_number(
                        glow.get("replay_energy", 0)
                    ),
                },
            ],

            "identityCards": [
                {
                    "icon": "🎤",
                    "label": "Top Artist",
                    "value": card_value(top_artist_card),
                    "sub": card_subtitle(top_artist_card),
                },
                {
                    "icon": "🔁",
                    "label": "Most Replayed",
                    "value": card_value(most_replayed_card),
                    "sub": card_subtitle(most_replayed_card),
                },
                {
                    "icon": "⏭",
                    "label": "Most Skipped",
                    "value": card_value(most_skipped_card),
                    "sub": card_subtitle(most_skipped_card),
                },
                {
                    "icon": "💎",
                    "label": "Hidden Favorite",
                    "value": card_value(hidden_favorite_card),
                    "sub": card_subtitle(hidden_favorite_card),
                },
                {
                    "icon": "👹",
                    "label": "Playlist Villain",
                    "value": card_value(playlist_villain_card),
                    "sub": card_subtitle(playlist_villain_card),
                },
                {
                    "icon": "🏆",
                    "label": "Playlist MVP",
                    "value": card_value(playlist_mvp_card),
                    "sub": card_subtitle(playlist_mvp_card),
                },
            ],

            "badges": normalize_badges(
                glow.get("badges", []),
                limit=4
            ),

            "overview": [
                {
                    "label": "Songs",
                    "value": analytics.get("total_songs", 0),
                    "tone": "",
                },
                {
                    "label": "Artists",
                    "value": analytics.get("unique_artists", 0),
                    "tone": "",
                },
                {
                    "label": "Albums",
                    "value": analytics.get("unique_albums", 0),
                    "tone": "",
                },
                {
                    "label": "Duration",
                    "value": analytics.get("total_duration", "0h 0m"),
                    "tone": "",
                },
                {
                    "label": "Avg Length",
                    "value": analytics.get("average_song_length", "0m 0s"),
                    "tone": "",
                },
                {
                    "label": "Clean",
                    "value": analytics.get("clean_songs", 0),
                    "tone": "sage",
                },
                {
                    "label": "Explicit",
                    "value": analytics.get("explicit_songs", 0),
                    "tone": "rose",
                },
                {
                    "label": "Duplicates",
                    "value": analytics.get("duplicate_count", 0),
                    "tone": "sage" if analytics.get("duplicate_count", 0) == 0 else "rose",
                },
            ],

            "health": {
                "score": analytics.get("health_score", 0),
                "status": analytics.get("health_status", "No Data"),
                "bars": [
                    {
                        "label": "Diversity",
                        "value": analytics.get("diversity_score", 0),
                    },
                    {
                        "label": "Artist Entropy",
                        "value": analytics.get("artist_entropy_score", 0),
                    },
                    {
                        "label": "Album Entropy",
                        "value": analytics.get("album_entropy_score", 0),
                    },
                    {
                        "label": "Rating Coverage",
                        "value": analytics.get("rated_percentage", 0),
                    },
                ],
                "note": (
                    f"{analytics.get('top_artist_name', 'N/A')} makes up "
                    f"{analytics.get('top_artist_percentage', 0)}% of the playlist. "
                    f"Duplicate pressure: {analytics.get('duplicate_count', 0)} extra copies."
                ),
            },

            "doctor": {
                "headline": doctor.get(
                    "headline",
                    f"This playlist is in {str(analytics.get('health_status', 'good')).lower()} shape."
                ),
                "strengths": strengths[:3],
                "warnings": warnings[:3],
                "ratingTips": rating_tips[:3],
            },

            "listening": {
                "totalKnownSongs": listening.get("total_known_songs", 0),
                "totalPlays": listening.get("total_plays", 0),
                "totalReplays": listening.get("total_replays", 0),
                "completionRate": listening.get("global_completion_rate", 0),
                "skipRate": listening.get("global_skip_rate", 0),
                "streaks": {
                    "finished": f"{streaks.get('finished_streak', 0)} songs",
                    "skip": f"{streaks.get('skip_streak', 0)} songs",
                    "artist": (
                        f"{streaks.get('artist_streak_name', 'N/A')} ×"
                        f"{streaks.get('artist_streak_count', 0)}"
                    ),
                    "album": (
                        f"{streaks.get('album_streak_name', 'N/A')} ×"
                        f"{streaks.get('album_streak_count', 0)}"
                    ),
                },
            },

            "mostReplayed": most_replayed,
            "mostSkipped": most_skipped,

            "shuffleRecommendation": {
                "profile": recommended_profile,
                "confidence": recommendation_confidence,
                "reason": recommendation_reason,
                "cleanup": cleanup_suggestions,
                "hiddenFavorites": hidden_favorites,
            },

            "library": {
                "topArtists": top_artists,
                "topAlbums": top_albums,
            },

            "ratings": {
                "distribution": rating_distribution,
                "topRated": top_rated,
                "lowRated": low_rated,
            },
        }

    def get_aura_status(self, score):
        score = clamp_number(score)

        if score >= 90:
            return "Legendary"

        if score >= 80:
            return "Excellent"

        if score >= 65:
            return "Strong"

        if score >= 45:
            return "Developing"

        return "Needs Vibes"