from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.stat_tile import StatTile

from services.duplicate_service import analyze_duplicates


class DuplicatesPage(QWidget):

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

        title = QLabel("Duplicate Finder")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "Find duplicate tracks in the playlist you are currently listening to. "
            "This page is read-only and does not modify your Spotify playlist."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        self.total_songs = StatTile("Songs")
        self.duplicate_tracks = StatTile("Duplicate Tracks")
        self.extra_copies = StatTile("Extra Copies")
        self.status = StatTile("Status")

        stats_grid.addWidget(self.total_songs, 0, 0)
        stats_grid.addWidget(self.duplicate_tracks, 0, 1)
        stats_grid.addWidget(self.extra_copies, 0, 2)
        stats_grid.addWidget(self.status, 0, 3)

        layout.addLayout(stats_grid)

        self.duplicates_card = Card("Duplicate Tracks")
        self.duplicates_label = QLabel("No data yet")
        self.duplicates_label.setWordWrap(True)
        self.duplicates_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.duplicates_label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.duplicates_card.layout.addWidget(
            self.duplicates_label
        )

        layout.addWidget(self.duplicates_card)
        layout.addStretch()

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

    def update_duplicates(self, playlist, tracks):

        analysis = analyze_duplicates(
            tracks
        )

        self.total_songs.set_value(
            analysis["total_songs"]
        )

        self.duplicate_tracks.set_value(
            analysis["unique_duplicate_tracks"]
        )

        self.extra_copies.set_value(
            analysis["extra_copies"]
        )

        if playlist is None:
            self.status.set_value("No Playlist")
        elif analysis["extra_copies"] == 0:
            self.status.set_value("Clean")
        else:
            self.status.set_value("Review")

        self.duplicates_label.setText(
            self.format_duplicates(
                analysis["duplicates"]
            )
        )

    def format_duplicates(self, duplicates):

        if not duplicates:
            return (
                "No duplicate tracks found.\n\n"
                "Your playlist looks clean."
            )

        lines = []

        for index, item in enumerate(duplicates, start=1):

            lines.append(
                f"{index}. {item['name']} — {item['artist']}\n"
                f"   Album: {item['album']}\n"
                f"   Year: {item['release_year']}  •  Duration: {item['duration']}\n"
                f"   Total copies: {item['total_copies']}  •  Extra copies: {item['extra_copies']}\n"
            )

        return "\n".join(lines)