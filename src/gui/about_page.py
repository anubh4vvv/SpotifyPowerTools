from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
)

from PySide6.QtCore import Qt

from gui.card import Card


class AboutPage(QWidget):

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("About Spotify Power Tools")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "A smart Spotify desktop companion for better shuffle, playlist insights, "
            "duplicate detection, and safe playlist cleaning."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        overview = Card("What This App Does")

        overview_text = QLabel(
            "Spotify Power Tools helps you improve how you listen to playlists.\n\n"
            "It can generate smarter shuffle previews, add smart-shuffled songs "
            "directly to your Spotify queue, analyze playlist health, find duplicate "
            "tracks, and create cleaned playlist copies without modifying the original playlist."
        )
        overview_text.setWordWrap(True)
        overview_text.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        overview.layout.addWidget(overview_text)

        features = Card("Current Features")

        features_text = QLabel(
            "✓ Smart Shuffle Preview\n"
            "✓ Queue Smart Shuffle\n"
            "✓ Queue size control\n"
            "✓ Persistent settings\n"
            "✓ Playlist analytics\n"
            "✓ Visual analytics charts\n"
            "✓ Playlist health score\n"
            "✓ Duplicate finder\n"
            "✓ Safe playlist cleaner\n"
            "✓ Open created playlists in Spotify"
        )
        features_text.setWordWrap(True)
        features_text.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        features.layout.addWidget(features_text)

        safety = Card("Safety Design")

        safety_text = QLabel(
            "Spotify Power Tools is designed to be safe by default.\n\n"
            "The app does not overwrite your original playlists. Cleaner features create "
            "new playlist copies instead of deleting or modifying your existing playlists."
        )
        safety_text.setWordWrap(True)
        safety_text.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        safety.layout.addWidget(safety_text)

        tech = Card("Tech Stack")

        tech_text = QLabel(
            "Python\n"
            "PySide6\n"
            "Spotipy\n"
            "Spotify Web API\n"
            "Git + GitHub"
        )
        tech_text.setWordWrap(True)
        tech_text.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        tech.layout.addWidget(tech_text)

        layout.addWidget(overview)
        layout.addWidget(features)
        layout.addWidget(safety)
        layout.addWidget(tech)
        layout.addStretch()

        scroll.setWidget(content)

        root_layout.addWidget(scroll)