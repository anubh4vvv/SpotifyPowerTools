from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider,
)

from PySide6.QtCore import Qt, Signal

from gui.card import Card
from gui.image_loader import load_scaled_pixmap


def format_time(ms):

    seconds = ms // 1000
    minutes = seconds // 60
    seconds %= 60

    return f"{minutes}:{seconds:02d}"


def set_label_text(label, text):

    if label.text() != text:
        label.setText(
            text
        )


class CurrentSongCard(Card):

    rating_changed = Signal(str, int, str, str)

    def __init__(self):

        super().__init__("Currently Playing")

        self.setMinimumHeight(400)

        self.current_image_url = ""
        self.duration_ms = 0
        self.current_track_id = ""
        self.current_rating = 0
        self.last_is_playing = None

        body = QHBoxLayout()
        body.setSpacing(30)

        self.cover = QLabel()
        self.cover.setFixedSize(240, 240)

        body.addWidget(
            self.cover,
            alignment=Qt.AlignCenter
        )

        info = QVBoxLayout()
        info.setSpacing(12)

        self.song = QLabel()
        self.song.setWordWrap(True)
        self.song.setStyleSheet("""
            font-size:30px;
            font-weight:800;
        """)

        self.artist = QLabel()
        self.artist.setStyleSheet("""
            font-size:18px;
        """)

        self.album = QLabel()
        self.album.setWordWrap(True)
        self.album.setStyleSheet("""
            color:#AAAAAA;
            font-size:14px;
        """)

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 0)
        self.progress_slider.setFixedHeight(18)

        self.time = QLabel("0:00 / 0:00")
        self.time.setStyleSheet("""
            color:#AAAAAA;
            font-size:11pt;
        """)

        self.progress_slider.valueChanged.connect(
            self.update_seek_time_label
        )

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.previous_button = QPushButton("Previous")
        self.previous_button.setObjectName("SecondaryButton")

        self.play_pause_button = QPushButton("Pause")

        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("SecondaryButton")

        controls.addWidget(self.previous_button)
        controls.addWidget(self.play_pause_button)
        controls.addWidget(self.next_button)

        rating_row = QHBoxLayout()
        rating_row.setSpacing(8)

        rating_title = QLabel("Rating")
        rating_title.setFixedWidth(55)
        rating_title.setStyleSheet("""
            color:#A0A0A0;
            font-size:10.5pt;
            font-weight:700;
        """)

        self.rating_buttons = []

        for rating in range(1, 6):

            button = QPushButton(str(rating))
            button.setFixedWidth(38)
            button.setObjectName("RatingButton")

            button.clicked.connect(
                lambda checked=False, value=rating: self.emit_rating_changed(value)
            )

            self.rating_buttons.append(
                button
            )

            rating_row.addWidget(
                button
            )

        self.clear_rating_button = QPushButton("Clear")
        self.clear_rating_button.setObjectName("SecondaryButton")
        self.clear_rating_button.setFixedWidth(70)

        self.clear_rating_button.clicked.connect(
            lambda: self.emit_rating_changed(0)
        )

        rating_row.insertWidget(
            0,
            rating_title
        )

        rating_row.addWidget(
            self.clear_rating_button
        )

        rating_row.addStretch()

        self.meta = QLabel()
        self.meta.setStyleSheet("""
            color:#8F97A3;
            font-size:12px;
        """)

        info.addStretch()
        info.addWidget(self.song)
        info.addWidget(self.artist)
        info.addWidget(self.album)
        info.addSpacing(20)
        info.addWidget(self.progress_slider)
        info.addWidget(self.time)
        info.addLayout(controls)
        info.addLayout(rating_row)
        info.addSpacing(12)
        info.addWidget(self.meta)
        info.addStretch()

        body.addLayout(info, 1)

        self.layout.addLayout(body)

        self.update_rating(0)

    def update_seek_time_label(self, value):

        self.time.setText(
            f"{format_time(value)} / {format_time(self.duration_ms)}"
        )

    def emit_rating_changed(self, rating):

        if not self.current_track_id:
            return

        self.update_rating(
            rating
        )

        self.rating_changed.emit(
            self.current_track_id,
            rating,
            self.song.text(),
            self.artist.text()
        )

    def update_rating(self, rating):

        rating = int(
            rating or 0
        )

        if rating == self.current_rating:
            return

        self.current_rating = rating

        for index, button in enumerate(
            self.rating_buttons,
            start=1
        ):

            if index <= self.current_rating:

                button.setStyleSheet("""
                    QPushButton#RatingButton {
                        background:#1DB954;
                        color:#000000;
                        border:none;
                        border-radius:10px;
                        font-weight:900;
                        padding:8px;
                    }
                """)

            else:

                button.setStyleSheet("""
                    QPushButton#RatingButton {
                        background:#19191D;
                        color:#F5F5F5;
                        border:1px solid #333338;
                        border-radius:10px;
                        font-weight:700;
                        padding:8px;
                    }

                    QPushButton#RatingButton:hover {
                        border:1px solid #1DB954;
                    }
                """)

    def clear_display(self):

        if self.current_track_id == "":
            return

        set_label_text(
            self.song,
            "Nothing Playing"
        )

        self.artist.clear()
        self.album.clear()
        self.cover.clear()

        self.current_image_url = ""
        self.current_track_id = ""
        self.duration_ms = 0
        self.last_is_playing = None

        self.progress_slider.blockSignals(True)
        self.progress_slider.setRange(0, 0)
        self.progress_slider.setValue(0)
        self.progress_slider.blockSignals(False)

        set_label_text(
            self.time,
            "0:00 / 0:00"
        )

        self.meta.clear()

        self.play_pause_button.setText(
            "Play"
        )

        self.current_rating = -1
        self.update_rating(0)

    def update_progress(self, current, duration):

        progress = current.get(
            "progress_ms",
            0
        )

        if progress is None:
            progress = 0

        self.duration_ms = duration

        if self.progress_slider.isSliderDown():
            return

        if self.progress_slider.maximum() != duration:
            self.progress_slider.blockSignals(True)
            self.progress_slider.setRange(
                0,
                duration
            )
            self.progress_slider.blockSignals(False)

        if self.progress_slider.value() != progress:
            self.progress_slider.blockSignals(True)
            self.progress_slider.setValue(
                progress
            )
            self.progress_slider.blockSignals(False)

        new_time = f"{format_time(progress)} / {format_time(duration)}"

        set_label_text(
            self.time,
            new_time
        )

    def update_play_button(self, current):

        is_playing = bool(
            current.get("is_playing")
        )

        if is_playing == self.last_is_playing:
            return

        self.last_is_playing = is_playing

        if is_playing:
            self.play_pause_button.setText("Pause")
        else:
            self.play_pause_button.setText("Play")

    def update_cover_art(self, album):

        images = album.get(
            "images",
            []
        )

        if not images:
            self.cover.clear()
            self.current_image_url = ""

            return

        image_url = images[0].get(
            "url",
            ""
        )

        if not image_url:
            return

        should_reload = (
                image_url != self.current_image_url
                or self.cover.pixmap() is None
                or self.cover.pixmap().isNull()
        )

        if not should_reload:
            return

        pixmap = load_scaled_pixmap(
            image_url,
            240,
            240,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        if not pixmap.isNull():
            self.cover.setPixmap(
                pixmap
            )

            self.current_image_url = image_url

    def update_static_track_info(self, track, track_metadata, rating):

        track_id = (
            track.get("id")
            or track.get("uri")
            or ""
        )

        self.current_track_id = track_id

        set_label_text(
            self.song,
            track.get("name", "Unknown Song")
        )

        artists = track.get(
            "artists",
            []
        )

        artist_name = "Unknown Artist"

        if artists:
            artist_name = artists[0].get(
                "name",
                "Unknown Artist"
            )

        set_label_text(
            self.artist,
            artist_name
        )

        album = track.get(
            "album",
            {}
        )

        set_label_text(
            self.album,
            album.get("name", "Unknown Album")
        )

        self.update_cover_art(
            album
        )

        explicit = (
            "Explicit"
            if track.get("explicit", False)
            else "Clean"
        )

        release = album.get(
            "release_date",
            ""
        )

        year = release[:4] if release else "Unknown"

        popularity = track_metadata.get(
            "popularity"
        )

        if popularity is None:
            popularity = track.get(
                "popularity"
            )

        if popularity is None:
            popularity = "Unavailable"

        meta_parts = [
            explicit,
            year,
        ]

        if popularity != "Unavailable":
            meta_parts.append(
                f"Popularity {popularity}"
            )

        set_label_text(
            self.meta,
            "   •   ".join(meta_parts)
        )

        self.current_rating = -1
        self.update_rating(
            rating
        )

    def update_song(self, current, track_metadata=None, rating=0):

        if track_metadata is None:
            track_metadata = {}

        if current is None or current.get("item") is None:
            self.clear_display()
            return

        track = current.get(
            "item",
            {}
        )

        track_id = (
            track.get("id")
            or track.get("uri")
            or ""
        )

        track_changed = (
            track_id != self.current_track_id
        )

        if track_changed:

            self.update_static_track_info(
                track,
                track_metadata,
                rating
            )

        else:

            album = track.get(
                "album",
                {}
            )

            self.update_cover_art(
                album
            )

            if int(rating or 0) != self.current_rating:
                self.update_rating(
                    rating
                )

        duration = track.get(
            "duration_ms",
            0
        )

        if duration is None:
            duration = 0

        self.update_progress(
            current,
            duration
        )

        self.update_play_button(
            current
        )