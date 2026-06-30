from rules.artist_rule import artist_score
from models.song import Song


def make_song(name, artist, album):
    return Song(
        id=name,
        name=name,
        artist=artist,
        album=album,
        duration_ms=180000,
        popularity=50,
        explicit=False,
        release_year=2020,
        uri=f"spotify:track:{name}"
    )


def test_same_artist_penalty():

    previous = make_song(
        "Song A",
        "Artist 1",
        "Album A"
    )

    candidate = make_song(
        "Song B",
        "Artist 1",
        "Album B"
    )

    result = artist_score(candidate, [previous])

    assert result.score < 0