from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QPushButton,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.stat_tile import StatTile

from services.duplicate_service import analyze_duplicates


class DuplicatesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.is_busy = False

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
            "Find duplicate tracks and create a safe cleaned playlist copy. "
            "Your original Spotify playlist is never modified."
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

        self.clean_button = QPushButton(
            "Create Cleaned Copy"
        )
        self.clean_button.setEnabled(False)

        self.helper_label = QLabel(
            "A cleaned copy keeps the first copy of every song and removes extra duplicates."
        )
        self.helper_label.setWordWrap(True)
        self.helper_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        self.duplicates_card.layout.addWidget(
            self.duplicates_label
        )

        self.duplicates_card.layout.addSpacing(12)

        self.duplicates_card.layout.addWidget(
            self.helper_label
        )

        self.duplicates_card.layout.addWidget(
            self.clean_button
        )

        layout.addWidget(self.duplicates_card)
        layout.addStretch()

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

    def set_busy(self, busy):

        self.is_busy = busy

        if busy:
            self.clean_button.setEnabled(False)
            self.clean_button.setText("Creating...")
        else:
            self.clean_button.setText("Create Cleaned Copy")

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

        has_duplicates = analysis["extra_copies"] > 0

        if playlist is None:
            self.status.set_value("No Playlist")
        elif not has_duplicates:
            self.status.set_value("Clean")
        else:
            self.status.set_value("Review")

        if not self.is_busy:
            self.clean_button.setEnabled(
                playlist is not None and has_duplicates
            )

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