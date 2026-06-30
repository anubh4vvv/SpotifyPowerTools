from analytics.playlist_health import playlist_health_report
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


def test_health_report():

    tracks = [song(i) for i in range(10)]

    report = playlist_health_report(tracks)

    assert isinstance(report, dict)