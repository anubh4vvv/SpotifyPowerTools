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


class PlaylistIdentityCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("IdentityCard")
        self.setMinimumHeight(185)
        self.setMaximumHeight(210)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(28)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(8)

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
        left.addSpacing(6)
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

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        content = QWidget()
        content.setObjectName("DashboardContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 22, 28, 22)
        layout.setSpacing(18)

        self.dashboard_header = self.build_dashboard_header()

        self.current_song_card = CurrentSongCard()
        self.current_song_card.setMinimumHeight(390)
        self.current_song_card.setMaximumHeight(420)

        self.shuffle_panel = ShufflePanel()
        self.shuffle_panel.setMinimumHeight(390)
        self.shuffle_panel.setMaximumHeight(420)

        self.playlist_card = PlaylistCard()
        self.playlist_card.setMinimumHeight(125)
        self.playlist_card.setMaximumHeight(145)

        self.playlist_identity_card = PlaylistIdentityCard()

        # Keep this object alive because MainWindow still connects to it.
        # It is hidden from the visible dashboard.
        self.player_controls_card = PlayerControlsCard()
        self.player_controls_card.setVisible(False)

        # Important:
        # MainWindow.preview_finished() calls self.dashboard.preview_panel.show_tracks(preview).
        # In the new mockup layout, preview rows live inside Smart Shuffle.
        self.preview_panel = self.shuffle_panel

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(22)

        top_row.addWidget(
            self.current_song_card,
            3
        )

        top_row.addWidget(
            self.shuffle_panel,
            2
        )

        layout.addWidget(
            self.dashboard_header
        )

        layout.addLayout(
            top_row,
            1
        )

        layout.addWidget(
            self.playlist_card
        )

        layout.addWidget(
            self.playlist_identity_card
        )

        root_layout.addWidget(content)

    def build_dashboard_header(self):

        header = QFrame()
        header.setObjectName("DashboardHeader")
        header.setMinimumHeight(58)
        header.setMaximumHeight(70)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 2)
        layout.setSpacing(16)

        text_block = QVBoxLayout()
        text_block.setContentsMargins(0, 0, 0, 0)
        text_block.setSpacing(3)

        self.greeting_label = QLabel(
            'good evening — '
            '<span style="color:#e3a857; font-style:italic;">late night mix</span>'
        )
        self.greeting_label.setObjectName("DashboardGreeting")
        self.greeting_label.setTextFormat(Qt.RichText)

        self.playlist_meta_label = QLabel(
            "317 tracks · 20h 30m · last synced just now"
        )
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

        return header