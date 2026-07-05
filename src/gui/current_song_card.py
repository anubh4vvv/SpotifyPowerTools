from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QFrame,
)

from PySide6.QtCore import Qt, Signal

from PySide6.QtGui import QFontMetrics

from gui.card import Card
from gui.image_loader import load_scaled_pixmap


def format_time(ms):
    seconds = int(ms or 0) // 1000
    minutes = seconds // 60
    seconds %= 60

    return f"{minutes}:{seconds:02d}"


def set_label_text(label, text):
    if label.text() != text:
        label.setText(text)


class ElidedLabel(QLabel):

    def __init__(self, text=""):
        super().__init__()

        self.full_text = ""
        self.setText(text)

    def setText(self, text):
        self.full_text = str(text or "")
        self.apply_elide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_elide()

    def apply_elide(self):
        if self.width() <= 0:
            super().setText(self.full_text)
            return

        metrics = QFontMetrics(self.font())

        elided = metrics.elidedText(
            self.full_text,
            Qt.ElideRight,
            max(40, self.width())
        )

        super().setText(elided)

    def raw_text(self):
        return self.full_text


class CurrentSongCard(Card):

    rating_changed = Signal(str, int, str, str)

    def __init__(self):
        super().__init__("NOW PLAYING")

        self.setObjectName("NowPlayingCard")
        self.setMinimumHeight(400)
        self.setMaximumHeight(410)

        self.current_image_url = ""
        self.duration_ms = 0
        self.current_track_id = ""
        self.current_rating = -1
        self.last_is_playing = None

        body = QHBoxLayout()
        body.setContentsMargins(0, 6, 0, 0)
        body.setSpacing(26)

        self.polaroid = QFrame()
        self.polaroid.setObjectName("PolaroidFrame")
        self.polaroid.setFixedSize(260, 300)

        polaroid_layout = QVBoxLayout(self.polaroid)
        polaroid_layout.setContentsMargins(9, 9, 9, 10)
        polaroid_layout.setSpacing(8)

        self.cover = QLabel()
        self.cover.setObjectName("AlbumCover")
        self.cover.setFixedSize(242, 242)
        self.cover.setAlignment(Qt.AlignCenter)

        self.side_caption = QLabel("side A · track 07")
        self.side_caption.setObjectName("PolaroidCaption")
        self.side_caption.setAlignment(Qt.AlignCenter)

        polaroid_layout.addWidget(self.cover)
        polaroid_layout.addWidget(self.side_caption)

        body.addWidget(
            self.polaroid,
            alignment=Qt.AlignVCenter
        )

        info = QVBoxLayout()
        info.setContentsMargins(0, 4, 0, 4)
        info.setSpacing(8)

        self.song = ElidedLabel("Nothing Playing")
        self.song.setObjectName("NowPlayingTitle")
        self.song.setMinimumWidth(220)
        self.song.setMaximumHeight(58)

        self.artist = ElidedLabel("")
        self.artist.setObjectName("NowPlayingArtist")
        self.artist.setMinimumWidth(220)
        self.artist.setMaximumHeight(28)

        self.album = ElidedLabel("")
        self.album.setObjectName("NowPlayingAlbum")
        self.album.setMinimumWidth(220)
        self.album.setMaximumHeight(24)

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setObjectName("NowPlayingProgress")
        self.progress_slider.setRange(0, 0)
        self.progress_slider.setFixedHeight(18)

        self.time = QLabel("0:00 / 0:00")
        self.time.setObjectName("NowPlayingTime")

        self.progress_slider.valueChanged.connect(
            self.update_seek_time_label
        )

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.previous_button = QPushButton("‹")
        self.previous_button.setObjectName("TransportSecondary")

        self.play_pause_button = QPushButton("▶")
        self.play_pause_button.setObjectName("TransportPlay")

        self.next_button = QPushButton("›")
        self.next_button.setObjectName("TransportSecondary")

        controls.addWidget(self.previous_button)
        controls.addWidget(self.play_pause_button)
        controls.addWidget(self.next_button)

        rating_row = QHBoxLayout()
        rating_row.setSpacing(7)

        rating_title = QLabel("Rating")
        rating_title.setObjectName("RatingTitle")
        rating_title.setFixedWidth(58)

        self.rating_buttons = []

        for rating in range(1, 6):
            button = QPushButton("★")
            button.setFixedSize(36, 36)
            button.setObjectName("RatingButton")

            button.clicked.connect(
                lambda checked=False, value=rating: self.emit_rating_changed(value)
            )

            self.rating_buttons.append(button)
            rating_row.addWidget(button)

        self.clear_rating_button = QPushButton("clear")
        self.clear_rating_button.setObjectName("RatingClearButton")
        self.clear_rating_button.setFixedWidth(70)

        self.clear_rating_button.clicked.connect(
            lambda: self.emit_rating_changed(0)
        )

        rating_row.insertWidget(0, rating_title)
        rating_row.addWidget(self.clear_rating_button)
        rating_row.addStretch()

        self.meta = QLabel("")
        self.meta.setObjectName("NowPlayingMeta")

        info.addStretch()
        info.addWidget(self.song)
        info.addWidget(self.artist)
        info.addWidget(self.album)
        info.addSpacing(14)
        info.addWidget(self.progress_slider)
        info.addWidget(self.time)
        info.addSpacing(4)
        info.addLayout(controls)
        info.addLayout(rating_row)
        info.addSpacing(4)
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

        self.update_rating(rating)

        song_name = (
            self.song.raw_text()
            if hasattr(self.song, "raw_text")
            else self.song.text()
        )

        artist_name = (
            self.artist.raw_text()
            if hasattr(self.artist, "raw_text")
            else self.artist.text()
        )

        self.rating_changed.emit(
            self.current_track_id,
            rating,
            song_name,
            artist_name
        )

    def update_rating(self, rating):
        rating = int(rating or 0)

        self.current_rating = rating

        for index, button in enumerate(self.rating_buttons, start=1):
            if index <= self.current_rating:
                button.setStyleSheet("""
                    QPushButton#RatingButton {
                        background:#e3a857;
                        color:#14110e;
                        border:none;
                        border-radius:10px;
                        font-weight:900;
                        padding:6px;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton#RatingButton {
                        background:#1a1611;
                        color:#c9bfae;
                        border:1px solid rgba(243,236,223,0.12);
                        border-radius:10px;
                        font-weight:700;
                        padding:6px;
                    }

                    QPushButton#RatingButton:hover {
                        border:1px solid #e3a857;
                        color:#f3ecdf;
                    }
                """)

    def clear_display(self):
        if self.current_track_id == "":
            return

        set_label_text(self.song, "Nothing Playing")

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

        set_label_text(self.time, "0:00 / 0:00")

        self.meta.clear()

        self.play_pause_button.setText("▶")

        self.current_rating = -1
        self.update_rating(0)

    def update_progress(self, current, duration):
        progress = current.get("progress_ms", 0)

        if progress is None:
            progress = 0

        self.duration_ms = duration

        if self.progress_slider.isSliderDown():
            return

        if self.progress_slider.maximum() != duration:
            self.progress_slider.blockSignals(True)
            self.progress_slider.setRange(0, duration)
            self.progress_slider.blockSignals(False)

        if self.progress_slider.value() != progress:
            self.progress_slider.blockSignals(True)
            self.progress_slider.setValue(progress)
            self.progress_slider.blockSignals(False)

        new_time = f"{format_time(progress)} / {format_time(duration)}"

        set_label_text(self.time, new_time)

    def update_play_button(self, current):
        is_playing = bool(
            current.get("is_playing")
        )

        if is_playing == self.last_is_playing:
            return

        self.last_is_playing = is_playing

        if is_playing:
            self.play_pause_button.setText("Ⅱ")
        else:
            self.play_pause_button.setText("▶")

    def update_cover_art(self, album):
        images = album.get("images", [])

        if not images:
            self.cover.clear()
            self.current_image_url = ""
            return

        image_url = images[0].get("url", "")

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
            242,
            242,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        if not pixmap.isNull():
            self.cover.setPixmap(pixmap)
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

        artists = track.get("artists", [])

        artist_name = "Unknown Artist"

        if artists:
            artist_name = artists[0].get(
                "name",
                "Unknown Artist"
            )

        set_label_text(self.artist, artist_name)

        album = track.get("album", {})

        set_label_text(
            self.album,
            album.get("name", "Unknown Album")
        )

        self.update_cover_art(album)

        explicit = (
            "Explicit"
            if track.get("explicit", False)
            else "Clean"
        )

        release = album.get("release_date", "")
        year = release[:4] if release else "Unknown"

        popularity = track_metadata.get("popularity")

        if popularity is None:
            popularity = track.get("popularity")

        if popularity is None:
            popularity = "Unavailable"

        meta_parts = [
            explicit,
            year,
        ]

        if popularity != "Unavailable":
            meta_parts.append(f"Popularity {popularity}")

        set_label_text(
            self.meta,
            "   •   ".join(meta_parts)
        )

        self.current_rating = -1
        self.update_rating(rating)

    def update_song(self, current, track_metadata=None, rating=0):
        if track_metadata is None:
            track_metadata = {}

        if current is None or current.get("item") is None:
            self.clear_display()
            return

        track = current.get("item", {})

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
            album = track.get("album", {})

            self.update_cover_art(album)

            if int(rating or 0) != self.current_rating:
                self.update_rating(rating)

        duration = track.get("duration_ms", 0)

        if duration is None:
            duration = 0

        self.update_progress(current, duration)
        self.update_play_button(current)