from PySide6.QtWidgets import (
    QGridLayout,
)

from gui.card import Card
from gui.stat_tile import StatTile


class PlaylistCard(Card):

    def __init__(self):

        super().__init__("Playlist Statistics")

        self.setMinimumHeight(300)

        grid = QGridLayout()

        grid.setSpacing(15)

        self.song_tile = StatTile("Songs")

        self.artist_tile = StatTile("Artists")

        self.album_tile = StatTile("Albums")

        self.duration_tile = StatTile("Duration")

        grid.addWidget(
            self.song_tile,
            0,
            0
        )

        grid.addWidget(
            self.artist_tile,
            0,
            1
        )

        grid.addWidget(
            self.album_tile,
            1,
            0
        )

        grid.addWidget(
            self.duration_tile,
            1,
            1
        )

        self.layout.addLayout(grid)

    def update_playlist(self, playlist, tracks):

        if playlist is None:

            self.song_tile.set_value("--")

            self.artist_tile.set_value("--")

            self.album_tile.set_value("--")

            self.duration_tile.set_value("--")

            return

        artists = len({
            t.artist
            for t in tracks
        })

        albums = len({
            t.album
            for t in tracks
        })

        duration = sum(
            t.duration_ms
            for t in tracks
        )

        hours = duration // 1000 // 3600

        minutes = (
            duration // 1000 % 3600
        ) // 60

        self.song_tile.set_value(
            len(tracks)
        )

        self.artist_tile.set_value(
            artists
        )

        self.album_tile.set_value(
            albums
        )

        self.duration_tile.set_value(
            f"{hours}h {minutes}m"
        )