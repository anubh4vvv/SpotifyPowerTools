from dataclasses import dataclass


@dataclass
class Song:
    id: str
    name: str
    artist: str
    album: str
    duration_ms: int
    uri: str