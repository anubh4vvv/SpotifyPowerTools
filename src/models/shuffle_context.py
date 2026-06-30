from dataclasses import dataclass

from models.song import Song


@dataclass
class ShuffleContext:
    previous_song: Song | None

    recent_songs: list[Song]

    artist_spacing: int

    album_spacing: int