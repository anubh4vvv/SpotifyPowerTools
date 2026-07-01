from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QProgressBar,
    QPushButton,
    QSlider,
    QComboBox,
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

        self.setMinimumHeight(420)

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

        # ---------- Main Playback Controls ----------

        controls = QHBoxLayout()

        self.previous_button = QPushButton("⏮ Previous")
        self.previous_button.setObjectName("SecondaryButton")

        self.play_pause_button = QPushButton("Pause")

        self.next_button = QPushButton("Next ⏭")
        self.next_button.setObjectName("SecondaryButton")

        controls.addWidget(self.previous_button)
        controls.addWidget(self.play_pause_button)
        controls.addWidget(self.next_button)

        # ---------- Extra Playback Controls ----------

        volume_row = QHBoxLayout()

        volume_title = QLabel("Volume")
        volume_title.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.volume_value = QLabel("50%")
        self.volume_value.setFixedWidth(45)
        self.volume_value.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        self.volume_value.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        volume_row.addWidget(volume_title)
        volume_row.addWidget(self.volume_slider, 1)
        volume_row.addWidget(self.volume_value)

        mode_row = QHBoxLayout()

        self.shuffle_button = QPushButton("Shuffle: Off")
        self.shuffle_button.setObjectName("SecondaryButton")

        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems([
            "Repeat Off",
            "Repeat Track",
            "Repeat Playlist",
        ])

        mode_row.addWidget(self.shuffle_button)
        mode_row.addWidget(self.repeat_combo)

        self.volume_slider.valueChanged.connect(
            self.update_volume_label
        )

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

        info.addLayout(volume_row)

        info.addLayout(mode_row)

        info.addSpacing(10)

        info.addWidget(self.meta)

        info.addStretch()

        body.addLayout(info)

        self.layout.addLayout(body)

    def update_volume_label(self, value):

        self.volume_value.setText(
            f"{value}%"
        )

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

            self.shuffle_button.setText("Shuffle: Off")

            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(0)
            self.volume_slider.blockSignals(False)

            self.volume_value.setText("0%")

            self.repeat_combo.blockSignals(True)
            self.repeat_combo.setCurrentText("Repeat Off")
            self.repeat_combo.blockSignals(False)

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

        device = current.get("device", {})

        volume_percent = device.get(
            "volume_percent",
            0
        )

        if volume_percent is None:
            volume_percent = 0

        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(
            volume_percent
        )
        self.volume_slider.blockSignals(False)

        self.volume_value.setText(
            f"{volume_percent}%"
        )

        if current.get("shuffle_state"):
            self.shuffle_button.setText("Shuffle: On")
        else:
            self.shuffle_button.setText("Shuffle: Off")

        repeat_state = current.get(
            "repeat_state",
            "off"
        )

        repeat_label = {
            "off": "Repeat Off",
            "track": "Repeat Track",
            "context": "Repeat Playlist",
        }.get(
            repeat_state,
            "Repeat Off"
        )

        self.repeat_combo.blockSignals(True)
        self.repeat_combo.setCurrentText(
            repeat_label
        )
        self.repeat_combo.blockSignals(False)

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