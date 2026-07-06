from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt


class StatStripItem(QFrame):

    def __init__(self, label):
        super().__init__()

        self.setObjectName("StatStripItem")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(1)

        self.value_label = QLabel("--")
        self.value_label.setObjectName("StatStripValue")
        self.value_label.setAlignment(Qt.AlignCenter)

        self.label_label = QLabel(label.upper())
        self.label_label.setObjectName("StatStripLabel")
        self.label_label.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addWidget(self.label_label)
        layout.addStretch()

    def set_value(self, value):
        self.value_label.setText(str(value))


class StatDivider(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("StatDivider")
        self.setFixedWidth(1)


class PlaylistCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("StatsStrip")
        self.setMinimumHeight(106)
        self.setMaximumHeight(116)

        self.last_cache_key = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 10, 26, 10)
        layout.setSpacing(0)

        self.song_tile = StatStripItem("Tracks")
        self.artist_tile = StatStripItem("Artists")
        self.album_tile = StatStripItem("Albums")
        self.duration_tile = StatStripItem("Duration")

        layout.addWidget(self.song_tile)
        layout.addWidget(StatDivider())
        layout.addWidget(self.artist_tile)
        layout.addWidget(StatDivider())
        layout.addWidget(self.album_tile)
        layout.addWidget(StatDivider())
        layout.addWidget(self.duration_tile)

    def make_cache_key(self, playlist, tracks):
        if playlist is None:
            return ("none", 0)

        return (
            playlist.get("id", ""),
            playlist.get("snapshot_id", ""),
            len(tracks or []),
        )

    def update_playlist(self, playlist, tracks):
        tracks = tracks or []

        cache_key = self.make_cache_key(
            playlist,
            tracks
        )

        if cache_key == self.last_cache_key:
            return

        self.last_cache_key = cache_key

        if playlist is None:
            self.song_tile.set_value("--")
            self.artist_tile.set_value("--")
            self.album_tile.set_value("--")
            self.duration_tile.set_value("--")
            return

        artists = len({
            track.artist
            for track in tracks
            if getattr(track, "artist", "")
        })

        albums = len({
            track.album
            for track in tracks
            if getattr(track, "album", "")
        })

        duration = sum(
            getattr(track, "duration_ms", 0)
            for track in tracks
        )

        hours = duration // 1000 // 3600
        minutes = (duration // 1000 % 3600) // 60

        self.song_tile.set_value(len(tracks))
        self.artist_tile.set_value(artists)
        self.album_tile.set_value(albums)
        self.duration_tile.set_value(f"{hours}h {minutes}m")