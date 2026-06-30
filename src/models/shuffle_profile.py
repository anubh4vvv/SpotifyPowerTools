from dataclasses import dataclass


@dataclass
class ShuffleProfile:
    artist_weight: float
    album_weight: float
    random_weight: float

    artist_spacing: int
    album_spacing: int