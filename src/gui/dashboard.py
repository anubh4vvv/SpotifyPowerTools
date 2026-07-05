from datetime import datetime
from html import escape

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)

from PySide6.QtCore import Qt

from gui.current_song_card import CurrentSongCard
from gui.player_controls_card import PlayerControlsCard
from gui.playlist_card import PlaylistCard
from gui.shuffle_panel import ShufflePanel


def format_duration(total_ms):
    total_ms = int(total_ms or 0)

    total_seconds = total_ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def get_time_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "good morning"

    if 12 <= hour < 17:
        return "good afternoon"

    if 17 <= hour < 22:
        return "good evening"

    return "late night"


class PlaylistIdentityCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("IdentityCard")
        self.setMinimumHeight(190)
        self.setMaximumHeight(205)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 20, 26, 20)
        layout.setSpacing(28)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(7)

        self.eyebrow = QLabel("PLAYLIST IDENTITY")
        self.eyebrow.setObjectName("IdentityEyebrow")

        self.identity_name = QLabel("Replay Addict")
        self.identity_name.setObjectName("IdentityName")

        self.identity_subtitle = QLabel(
            "High replay energy, low skip rate, moderate artist dominance.\n"
            "This playlist knows exactly what it likes."
        )
        self.identity_subtitle.setObjectName("IdentitySubtitle")
        self.identity_subtitle.setWordWrap(True)

        badge_row = QHBoxLayout()
        badge_row.setContentsMargins(0, 0, 0, 0)
        badge_row.setSpacing(12)

        self.hidden_favorite = QLabel("hidden favorite: breathe")
        self.hidden_favorite.setObjectName("BadgeStickerSage")

        self.playlist_villain = QLabel("playlist villain: track 19")
        self.playlist_villain.setObjectName("BadgeStickerRose")

        self.discovery_badge = QLabel("discovery explorer")
        self.discovery_badge.setObjectName("BadgeStickerAmber")

        badge_row.addWidget(self.hidden_favorite)
        badge_row.addWidget(self.playlist_villain)
        badge_row.addWidget(self.discovery_badge)
        badge_row.addStretch()

        left.addWidget(self.eyebrow)
        left.addWidget(self.identity_name)
        left.addWidget(self.identity_subtitle)
        left.addSpacing(5)
        left.addLayout(badge_row)
        left.addStretch()

        self.aura_ring = QFrame()
        self.aura_ring.setObjectName("AuraRing")
        self.aura_ring.setFixedSize(148, 148)

        aura_layout = QVBoxLayout(self.aura_ring)
        aura_layout.setContentsMargins(0, 0, 0, 0)
        aura_layout.setSpacing(0)
        aura_layout.setAlignment(Qt.AlignCenter)

        self.aura_number = QLabel("87")
        self.aura_number.setObjectName("AuraRingNumber")
        self.aura_number.setAlignment(Qt.AlignCenter)

        self.aura_label = QLabel("AURA SCORE")
        self.aura_label.setObjectName("AuraRingLabel")
        self.aura_label.setAlignment(Qt.AlignCenter)

        aura_layout.addStretch()
        aura_layout.addWidget(self.aura_number)
        aura_layout.addWidget(self.aura_label)
        aura_layout.addStretch()

        layout.addLayout(left, 1)
        layout.addWidget(self.aura_ring, alignment=Qt.AlignCenter)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("Dashboard")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        content = QWidget()
        content.setObjectName("DashboardContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(16)

        self.dashboard_header = self.build_dashboard_header()

        self.current_song_card = CurrentSongCard()
        self.current_song_card.setMinimumHeight(400)
        self.current_song_card.setMaximumHeight(410)

        self.shuffle_panel = ShufflePanel()
        self.shuffle_panel.setMinimumHeight(400)
        self.shuffle_panel.setMaximumHeight(410)

        self.playlist_card = PlaylistCard()
        self.playlist_card.setMinimumHeight(112)
        self.playlist_card.setMaximumHeight(122)

        self.playlist_identity_card = PlaylistIdentityCard()

        # Keep this alive because MainWindow still connects to it.
        # It is intentionally hidden from the cinematic dashboard.
        self.player_controls_card = PlayerControlsCard()
        self.player_controls_card.setVisible(False)

        # MainWindow.preview_finished() calls:
        # self.dashboard.preview_panel.show_tracks(preview)
        # Preview now lives inside the Smart Shuffle card.
        self.preview_panel = self.shuffle_panel

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(22)

        top_row.addWidget(self.current_song_card, 13)
        top_row.addWidget(self.shuffle_panel, 10)

        layout.addWidget(self.dashboard_header)
        layout.addLayout(top_row)
        layout.addWidget(self.playlist_card)
        layout.addWidget(self.playlist_identity_card)

        root_layout.addWidget(content)

    def build_dashboard_header(self):
        header = QFrame()
        header.setObjectName("DashboardHeader")
        header.setMinimumHeight(62)
        header.setMaximumHeight(70)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 2)
        layout.setSpacing(16)

        text_block = QVBoxLayout()
        text_block.setContentsMargins(0, 0, 0, 0)
        text_block.setSpacing(3)

        self.greeting_label = QLabel()
        self.greeting_label.setObjectName("DashboardGreeting")
        self.greeting_label.setTextFormat(Qt.RichText)

        self.playlist_meta_label = QLabel()
        self.playlist_meta_label.setObjectName("DashboardMeta")

        text_block.addWidget(self.greeting_label)
        text_block.addWidget(self.playlist_meta_label)

        self.profile_pill = QLabel("anubhav")
        self.profile_pill.setObjectName("ProfilePill")
        self.profile_pill.setAlignment(Qt.AlignCenter)
        self.profile_pill.setFixedHeight(40)
        self.profile_pill.setMinimumWidth(120)

        layout.addLayout(text_block, 1)
        layout.addWidget(self.profile_pill)

        self.update_playlist_summary(None, [])

        return header

    def update_playlist_summary(self, playlist, tracks):
        tracks = tracks or []

        if playlist is None:
            playlist_name = "late night mix"
        else:
            playlist_name = playlist.get("name", "late night mix")

        safe_playlist_name = escape(str(playlist_name))
        greeting = get_time_greeting()

        self.greeting_label.setText(
            f'{greeting} — '
            f'<span style="color:#e3a857; font-style:italic;">'
            f'{safe_playlist_name}'
            f'</span>'
        )

        duration_ms = sum(
            getattr(track, "duration_ms", 0)
            for track in tracks
        )

        self.playlist_meta_label.setText(
            f"{len(tracks)} tracks · {format_duration(duration_ms)} · last synced just now"
        )