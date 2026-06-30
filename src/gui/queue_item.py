from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from gui.image_loader import load_pixmap


class QueueItem(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("QueueItem")
        self.setFixedHeight(76)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(14)

        self.cover = QLabel()
        self.cover.setFixedSize(48, 48)

        layout.addWidget(self.cover)

        text = QVBoxLayout()
        text.setContentsMargins(0, 0, 0, 0)
        text.setSpacing(2)

        self.song = QLabel()
        self.song.setObjectName("QueueSong")
        self.song.setWordWrap(False)

        self.artist = QLabel()
        self.artist.setObjectName("QueueArtist")
        self.artist.setWordWrap(False)

        text.addWidget(self.song)
        text.addWidget(self.artist)

        layout.addLayout(text, 1)

        self.duration = QLabel()
        self.duration.setObjectName("QueueDuration")

        layout.addWidget(
            self.duration,
            alignment=Qt.AlignRight | Qt.AlignVCenter
        )

    def update_song(self, song):

        self.song.setText(song.name)
        self.song.setToolTip(song.name)

        self.artist.setText(song.artist)
        self.artist.setToolTip(song.artist)

        if song.image_url:

            pixmap = load_pixmap(song.image_url)

            if not pixmap.isNull():

                self.cover.setPixmap(
                    pixmap.scaled(
                        48,
                        48,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )

            else:

                self.show_placeholder()

        else:

            self.show_placeholder()

        total_seconds = song.duration_ms // 1000

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        self.duration.setText(
            f"{minutes}:{seconds:02d}"
        )

    def show_placeholder(self):

        self.cover.clear()
        self.cover.setAlignment(Qt.AlignCenter)
        self.cover.setText("🎵")