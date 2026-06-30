from collections import Counter


def format_duration(total_ms):
    total_seconds = total_ms // 1000

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def calculate_playlist_analytics(tracks):
    """
    Calculates useful analytics from a list of Song objects.
    """

    if not tracks:
        return {
            "total_songs": 0,
            "unique_artists": 0,
            "unique_albums": 0,
            "explicit_songs": 0,
            "average_popularity": 0,
            "total_duration": "0h 0m",
            "diversity_score": 0,
            "top_artists": [],
            "top_albums": [],
            "release_years": [],
        }

    artists = [
        song.artist
        for song in tracks
    ]

    albums = [
        song.album
        for song in tracks
    ]

    explicit_count = sum(
        1 for song in tracks if song.explicit
    )

    popularity_values = [
        song.popularity
        for song in tracks
        if song.popularity is not None
    ]

    if popularity_values:
        average_popularity = round(
            sum(popularity_values) / len(popularity_values),
            1
        )
    else:
        average_popularity = 0

    total_duration_ms = sum(
        song.duration_ms
        for song in tracks
    )

    unique_artists = len(
        set(artists)
    )

    diversity_score = round(
        (unique_artists / len(tracks)) * 100,
        1
    )

    years = [
        song.release_year
        for song in tracks
        if song.release_year
    ]

    return {
        "total_songs": len(tracks),
        "unique_artists": unique_artists,
        "unique_albums": len(set(albums)),
        "explicit_songs": explicit_count,
        "average_popularity": average_popularity,
        "total_duration": format_duration(total_duration_ms),
        "diversity_score": diversity_score,
        "top_artists": Counter(artists).most_common(5),
        "top_albums": Counter(albums).most_common(5),
        "release_years": Counter(years).most_common(5),
    }