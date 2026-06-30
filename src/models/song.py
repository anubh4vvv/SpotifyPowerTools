from dataclasses import dataclass


@dataclass
class Song:

    id: str

    uri: str

    name: str

    artist: str

    album: str

    duration_ms: int

    image_url: str = ""

    release_year: str = ""

    explicit: bool = False

    popularity: int = 0