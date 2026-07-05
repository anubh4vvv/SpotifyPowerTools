from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from gui.card import Card


class PlaylistIdentityCard(Card):

    def __init__(self):
        super().__init__("Playlist Identity")

        self.setMinimumHeight(210)

        body = QHBoxLayout()
        body.setSpacing(28)

        left = QVBoxLayout()
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
        left.addSpacing(12)
        left.addLayout(badge_row)

        self.aura_ring = QFrame()
        self.aura_ring.setObjectName("AuraRing")
        self.aura_ring.setFixedSize(150, 150)

        aura_layout = QVBoxLayout(self.aura_ring)
        aura_layout.setAlignment(Qt.AlignCenter)
        aura_layout.setContentsMargins(0, 0, 0, 0)

        self.aura_number = QLabel("87")
        self.aura_number.setObjectName("AuraRingNumber")
        self.aura_number.setAlignment(Qt.AlignCenter)

        self.aura_label = QLabel("AURA SCORE")
        self.aura_label.setObjectName("AuraRingLabel")
        self.aura_label.setAlignment(Qt.AlignCenter)

        aura_layout.addWidget(self.aura_number)
        aura_layout.addWidget(self.aura_label)

        body.addLayout(left, 1)
        body.addWidget(self.aura_ring)

        self.layout.addLayout(body)