from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QProgressBar,
    QPushButton,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.image_loader import load_pixmap


def format_time(ms):
    seconds = ms // 1000

    minutes = seconds // 60

    seconds %= 60

    return f"{minutes}:{seconds:02d}"


class CurrentSongCard(Card):

    def __init__(self):

        super().__init__("Currently Playing")

        self.setMinimumHeight(340)

        self.current_image_url = ""

        body = QHBoxLayout()

        body.setSpacing(25)

        self.cover = QLabel()

        self.cover.setFixedSize(220, 220)

        body.addWidget(
            self.cover,
            alignment=Qt.AlignCenter
        )

        info = QVBoxLayout()

        info.setSpacing(10)

        self.song = QLabel()

        self.song.setStyleSheet("""
            font-size:28px;
            font-weight:700;
        """)

        self.artist = QLabel()

        self.artist.setStyleSheet("""
            font-size:18px;
        """)

        self.album = QLabel()

        self.album.setStyleSheet("""
            color:#AAAAAA;
            font-size:14px;
        """)

        self.progress = QProgressBar()

        self.progress.setTextVisible(False)

        self.progress.setFixedHeight(8)

        self.time = QLabel("0:00 / 0:00")

        self.time.setStyleSheet("""
            color:#AAAAAA;
        """)

        controls = QHBoxLayout()

        self.previous_button = QPushButton("⏮ Previous")
        self.previous_button.setObjectName("SecondaryButton")

        self.play_pause_button = QPushButton("Pause")

        self.next_button = QPushButton("Next ⏭")
        self.next_button.setObjectName("SecondaryButton")

        controls.addWidget(self.previous_button)
        controls.addWidget(self.play_pause_button)
        controls.addWidget(self.next_button)

        self.meta = QLabel()

        self.meta.setStyleSheet("""
            color:#8F97A3;
            font-size:12px;
        """)

        info.addStretch()

        info.addWidget(self.song)

        info.addWidget(self.artist)

        info.addWidget(self.album)

        info.addSpacing(15)

        info.addWidget(self.progress)

        info.addWidget(self.time)

        info.addLayout(controls)

        info.addSpacing(10)

        info.addWidget(self.meta)

        info.addStretch()

        body.addLayout(info)

        self.layout.addLayout(body)

    def update_song(self, current):

        if current is None:
            self.song.setText("Nothing Playing")

            self.artist.clear()

            self.album.clear()

            self.cover.clear()

            self.current_image_url = ""

            self.progress.setValue(0)

            self.time.setText("0:00 / 0:00")

            self.meta.clear()

            self.play_pause_button.setText("Play")

            return

        track = current["item"]

        self.song.setText(track["name"])

        self.artist.setText(
            track["artists"][0]["name"]
        )

        self.album.setText(
            track["album"]["name"]
        )

        images = track["album"].get("images", [])

        if images:
            image_url = images[0]["url"]

            if image_url != self.current_image_url:

                pixmap = load_pixmap(
                    image_url
                )

                if not pixmap.isNull():

                    self.cover.setPixmap(
                        pixmap.scaled(
                            220,
                            220,
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation
                        )
                    )

                    self.current_image_url = image_url

        duration = track["duration_ms"]

        progress = current["progress_ms"]

        self.progress.setMaximum(duration)

        self.progress.setValue(progress)

        self.time.setText(
            f"{format_time(progress)} / {format_time(duration)}"
        )

        if current.get("is_playing"):
            self.play_pause_button.setText("Pause")
        else:
            self.play_pause_button.setText("Play")

        explicit = (
            "🅴 Explicit"
            if track.get("explicit", False)
            else "Clean"
        )

        release = track["album"].get("release_date", "")

        year = release[:4] if release else "Unknown"

        popularity = track.get("popularity", "N/A")

        self.meta.setText(
            f"{explicit}   •   {year}   •   Popularity {popularity}"
        )