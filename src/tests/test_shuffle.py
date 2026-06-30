from shuffle.reshuffler import smart_shuffle
from models.song import Song


def song(i):

    return Song(
        id=str(i),
        name=f"Song {i}",
        artist=f"Artist {i%5}",
        album=f"Album {i%3}",
        duration_ms=180000,
        popularity=50,
        explicit=False,
        release_year=2020,
        uri=f"spotify:track:{i}"
    )


def test_shuffle_keeps_length():

    tracks = [song(i) for i in range(100)]

    shuffled = smart_shuffle(
        tracks,
        50,
        seed=99
    )

    assert len(shuffled) == len(tracks)

def test_no_duplicates():

    tracks = [song(i) for i in range(100)]

    shuffled = smart_shuffle(
        tracks,
        30,
        seed=42
    )

    ids = [s.id for s in shuffled]

    assert len(ids) == len(set(ids))

def test_current_song_does_not_move():

    tracks = [song(i) for i in range(100)]

    shuffled = smart_shuffle(
        tracks,
        20,
        seed=99
    )

    assert shuffled[20].id == tracks[20].id