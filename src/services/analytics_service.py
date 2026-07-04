from collections import Counter
from math import log2

from services.rating_service import calculate_rating_analytics
from services.listening_history_service import get_listening_analytics
from services.playlist_intelligence_service import calculate_playlist_intelligence

def format_duration(total_ms):
    total_seconds = total_ms // 1000

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def format_song_length(total_ms):
    total_seconds = total_ms // 1000

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}m {seconds}s"


def safe_percentage(part, total):
    if total == 0:
        return 0

    return round(
        (part / total) * 100,
        1
    )


def calculate_entropy_score(values):
    """
    Calculates normalized Shannon entropy from 0 to 100.

    0 means very repetitive.
    100 means evenly spread across categories.
    """

    if not values:
        return 0, 0

    counter = Counter(values)

    total = len(values)

    unique_count = len(counter)

    if unique_count <= 1:
        return 0, 0

    entropy = 0

    for count in counter.values():

        probability = count / total

        entropy -= probability * log2(
            probability
        )

    max_entropy = log2(
        unique_count
    )

    entropy_score = round(
        (entropy / max_entropy) * 100,
        1
    )

    entropy_bits = round(
        entropy,
        2
    )

    return entropy_score, entropy_bits


def get_track_key(song):
    """
    Prefer Spotify track ID for duplicate detection.
    If ID is missing, fall back to song name + artist.
    """

    if song.id:
        return song.id

    return f"{song.name.lower()}::{song.artist.lower()}"


def get_duplicate_tracks(tracks):
    """
    Returns duplicate tracks as:
    [
        ("Song Name - Artist", duplicate_count),
        ...
    ]

    duplicate_count means extra copies, not total copies.
    Example:
    If a song appears 3 times, duplicate_count = 2.
    """

    key_counter = Counter()
    display_names = {}

    for song in tracks:

        key = get_track_key(
            song
        )

        key_counter[key] += 1

        display_names[key] = f"{song.name} - {song.artist}"

    duplicates = []

    for key, count in key_counter.items():

        if count > 1:

            duplicates.append(
                (
                    display_names[key],
                    count - 1
                )
            )

    duplicates.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return duplicates


def get_oldest_and_newest_tracks(tracks):

    valid_tracks = []

    for song in tracks:

        if not song.release_year:
            continue

        try:
            year = int(
                song.release_year
            )

        except ValueError:
            continue

        valid_tracks.append(
            (
                year,
                song
            )
        )

    if not valid_tracks:
        return None, None

    oldest = min(
        valid_tracks,
        key=lambda item: item[0]
    )

    newest = max(
        valid_tracks,
        key=lambda item: item[0]
    )

    return oldest, newest


def calculate_health_score(
    diversity_score,
    duplicate_count,
    top_artist_percentage,
    top_album_percentage
):
    """
    Simple playlist health score from 0 to 100.

    Higher is better.

    Penalizes:
    - Too many duplicate songs
    - One artist dominating too much
    - One album dominating too much
    - Very low artist diversity
    """

    score = 100

    duplicate_penalty = min(
        duplicate_count * 3,
        30
    )

    artist_penalty = 0

    if top_artist_percentage > 25:

        artist_penalty = min(
            (top_artist_percentage - 25) * 0.8,
            20
        )

    album_penalty = 0

    if top_album_percentage > 20:

        album_penalty = min(
            (top_album_percentage - 20) * 0.7,
            15
        )

    diversity_penalty = 0

    if diversity_score < 35:

        diversity_penalty = min(
            (35 - diversity_score) * 0.6,
            20
        )

    score -= duplicate_penalty
    score -= artist_penalty
    score -= album_penalty
    score -= diversity_penalty

    score = max(
        0,
        min(100, round(score, 1))
    )

    return score


def get_health_status(score):

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Okay"

    return "Needs Work"


def get_empty_analytics():
    """
    Returns a full empty analytics object.

    Keeping this separate prevents missing-key errors in the GUI.
    """

    analytics = {
        "total_songs": 0,
        "unique_artists": 0,
        "unique_albums": 0,
        "explicit_songs": 0,
        "clean_songs": 0,
        "explicit_percentage": 0,
        "average_popularity": 0,
        "total_duration": "0h 0m",
        "average_song_length": "0m 0s",
        "diversity_score": 0,
        "artist_entropy_score": 0,
        "artist_entropy_bits": 0,
        "album_entropy_score": 0,
        "album_entropy_bits": 0,
        "average_rating": 0,
        "rated_songs": 0,
        "unrated_songs": 0,
        "rated_percentage": 0,
        "unrated_percentage": 0,
        "five_star_songs": 0,
        "low_rated_songs": 0,
        "top_rated_tracks": [],
        "low_rated_tracks": [],
        "rating_distribution": [],
        "listening_analytics": get_listening_analytics(),
        "health_score": 0,
        "health_status": "No Data",
        "duplicate_count": 0,
        "unique_duplicate_tracks": 0,
        "duplicate_tracks": [],
        "top_artist_name": "N/A",
        "top_artist_count": 0,
        "top_artist_percentage": 0,
        "top_album_name": "N/A",
        "top_album_count": 0,
        "top_album_percentage": 0,
        "oldest_song": "N/A",
        "oldest_year": "N/A",
        "newest_song": "N/A",
        "newest_year": "N/A",
        "top_artists": [],
        "top_albums": [],
        "release_years": [],
    }

    analytics["playlist_intelligence"] = calculate_playlist_intelligence(
        [],
        analytics
    )

    return analytics


def calculate_playlist_analytics(tracks):
    """
    Calculates useful analytics from a list of Song objects.
    """

    tracks = tracks or []

    if not tracks:
        return get_empty_analytics()

    total_songs = len(tracks)

    artists = [
        song.artist
        for song in tracks
    ]

    albums = [
        song.album
        for song in tracks
    ]

    artist_counter = Counter(
        artists
    )

    album_counter = Counter(
        albums
    )

    top_artist_name, top_artist_count = artist_counter.most_common(1)[0]
    top_album_name, top_album_count = album_counter.most_common(1)[0]

    top_artist_percentage = safe_percentage(
        top_artist_count,
        total_songs
    )

    top_album_percentage = safe_percentage(
        top_album_count,
        total_songs
    )

    explicit_count = sum(
        1
        for song in tracks
        if song.explicit
    )

    clean_count = total_songs - explicit_count

    explicit_percentage = safe_percentage(
        explicit_count,
        total_songs
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

    average_duration_ms = total_duration_ms // total_songs

    unique_artists = len(
        set(artists)
    )

    unique_albums = len(
        set(albums)
    )

    diversity_score = round(
        (unique_artists / total_songs) * 100,
        1
    )

    artist_entropy_score, artist_entropy_bits = calculate_entropy_score(
        artists
    )

    album_entropy_score, album_entropy_bits = calculate_entropy_score(
        albums
    )

    rating_analytics = calculate_rating_analytics(
        tracks
    )

    listening_analytics = get_listening_analytics()

    years = [
        song.release_year
        for song in tracks
        if song.release_year
    ]

    duplicate_tracks = get_duplicate_tracks(
        tracks
    )

    duplicate_count = sum(
        count
        for _, count in duplicate_tracks
    )

    oldest, newest = get_oldest_and_newest_tracks(
        tracks
    )

    if oldest is None:

        oldest_song = "N/A"
        oldest_year = "N/A"

    else:

        oldest_year, oldest_track = oldest
        oldest_song = f"{oldest_track.name} - {oldest_track.artist}"

    if newest is None:

        newest_song = "N/A"
        newest_year = "N/A"

    else:

        newest_year, newest_track = newest
        newest_song = f"{newest_track.name} - {newest_track.artist}"

    health_score = calculate_health_score(
        diversity_score=diversity_score,
        duplicate_count=duplicate_count,
        top_artist_percentage=top_artist_percentage,
        top_album_percentage=top_album_percentage,
    )

    health_status = get_health_status(
        health_score
    )

    analytics = {
        "total_songs": total_songs,
        "unique_artists": unique_artists,
        "unique_albums": unique_albums,
        "explicit_songs": explicit_count,
        "clean_songs": clean_count,
        "explicit_percentage": explicit_percentage,
        "average_popularity": average_popularity,
        "total_duration": format_duration(total_duration_ms),
        "average_song_length": format_song_length(average_duration_ms),
        "diversity_score": diversity_score,
        "artist_entropy_score": artist_entropy_score,
        "artist_entropy_bits": artist_entropy_bits,
        "album_entropy_score": album_entropy_score,
        "album_entropy_bits": album_entropy_bits,
        "average_rating": rating_analytics["average_rating"],
        "rated_songs": rating_analytics["rated_songs"],
        "unrated_songs": rating_analytics["unrated_songs"],
        "rated_percentage": rating_analytics["rated_percentage"],
        "unrated_percentage": rating_analytics["unrated_percentage"],
        "five_star_songs": rating_analytics["five_star_songs"],
        "low_rated_songs": rating_analytics["low_rated_songs"],
        "top_rated_tracks": rating_analytics["top_rated_tracks"],
        "low_rated_tracks": rating_analytics["low_rated_tracks"],
        "rating_distribution": rating_analytics["rating_distribution"],
        "listening_analytics": listening_analytics,
        "health_score": health_score,
        "health_status": health_status,
        "duplicate_count": duplicate_count,
        "unique_duplicate_tracks": len(duplicate_tracks),
        "duplicate_tracks": duplicate_tracks[:5],
        "top_artist_name": top_artist_name,
        "top_artist_count": top_artist_count,
        "top_artist_percentage": top_artist_percentage,
        "top_album_name": top_album_name,
        "top_album_count": top_album_count,
        "top_album_percentage": top_album_percentage,
        "oldest_song": oldest_song,
        "oldest_year": oldest_year,
        "newest_song": newest_song,
        "newest_year": newest_year,
        "top_artists": artist_counter.most_common(5),
        "top_albums": album_counter.most_common(5),
        "release_years": Counter(years).most_common(5),
    }

    analytics["playlist_intelligence"] = calculate_playlist_intelligence(
        tracks,
        analytics
    )

    return analytics