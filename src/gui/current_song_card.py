from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.image_loader import load_pixmap


class CurrentSongCard(Card):

    def __init__(self):

        super().__init__("Current Song")

        body = QHBoxLayout()

        self.cover = QLabel()

        self.cover.setFixedSize(220,220)

        body.addWidget(
            self.cover,
            alignment=Qt.AlignCenter
        )

        info = QVBoxLayout()

        self.song = QLabel()

        self.song.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.artist = QLabel()

        self.artist.setStyleSheet("""
            font-size:18px;
        """)

        self.album = QLabel()

        self.album.setStyleSheet("""
            color:#AAAAAA;
        """)

        info.addStretch()

        info.addWidget(self.song)

        info.addWidget(self.artist)

        info.addWidget(self.album)

        info.addStretch()

        body.addLayout(info)

        self.layout.addLayout(body)

    def update_song(self,current):

        if current is None:

            self.song.setText("Nothing Playing")

            self.artist.clear()

            self.album.clear()

            self.cover.clear()

            return

        track=current["item"]

        self.song.setText(track["name"])

        self.artist.setText(
            track["artists"][0]["name"]
        )

        self.album.setText(
            track["album"]["name"]
        )

        pixmap=load_pixmap(
            track["album"]["images"][0]["url"]
        )

        self.cover.setPixmap(
            pixmap.scaled(
                220,
                220,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )