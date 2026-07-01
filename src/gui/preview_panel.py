from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.image_loader import load_pixmap


class PreviewRow(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(62)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.index_label = QLabel("")
        self.index_label.setFixedWidth(28)
        self.index_label.setAlignment(
            Qt.AlignCenter
        )
        self.index_label.setStyleSheet(
            "color:#1DB954; font-size:10pt; font-weight:800;"
        )

        self.cover = QLabel()
        self.cover.setFixedSize(44, 44)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.song_label = QLabel("")
        self.song_label.setStyleSheet(
            "color:#FFFFFF; font-size:11pt; font-weight:700;"
        )

        self.artist_label = QLabel("")
        self.artist_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        text_layout.addWidget(self.song_label)
        text_layout.addWidget(self.artist_label)

        layout.addWidget(self.index_label)
        layout.addWidget(self.cover)
        layout.addLayout(text_layout, 1)

        self.setStyleSheet("""
            PreviewRow {
                background:#151518;
                border:1px solid #2A2A2D;
                border-radius:10px;
            }
        """)

    def update_song(self, index, song):

        self.index_label.setText(
            str(index)
        )

        self.song_label.setText(
            song.name
        )

        self.artist_label.setText(
            song.artist
        )

        if song.image_url:

            pixmap = load_pixmap(
                song.image_url
            )

            if not pixmap.isNull():

                self.cover.setPixmap(
                    pixmap.scaled(
                        44,
                        44,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                )

                return

        self.cover.clear()


class PreviewPanel(Card):

    def __init__(self):

        super().__init__("Upcoming Queue")

        self.setMinimumHeight(500)

        self.layout.setSpacing(12)

        self.helper_label = QLabel(
            "Preview of the smart-shuffled songs that will be added to your Spotify queue."
        )
        self.helper_label.setWordWrap(True)
        self.helper_label.setStyleSheet(
            "color:#8F97A3; font-size:10.5pt;"
        )

        self.empty_label = QLabel(
            "No preview yet. Click Preview Shuffle to generate upcoming songs."
        )
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(10)

        self.rows = []

        self.layout.addWidget(self.helper_label)
        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.rows_layout)
        self.layout.addStretch()

    def clear_rows(self):

        for row in self.rows:
            row.setParent(None)
            row.deleteLater()

        self.rows = []

    def show_tracks(self, tracks):

        self.clear_rows()

        if not tracks:
            self.empty_label.show()
            self.empty_label.setText(
                "No preview available."
            )
            return

        self.empty_label.hide()

        self.helper_label.setText(
            f"Previewing {len(tracks)} songs that will be added to your Spotify queue."
        )

        for index, song in enumerate(
            tracks,
            start=1
        ):

            row = PreviewRow()

            row.update_song(
                index,
                song
            )

            self.rows.append(row)

            self.rows_layout.addWidget(row)