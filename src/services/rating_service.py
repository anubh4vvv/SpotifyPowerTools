import json

from services.app_paths import (
    data_file,
    get_data_dir,
    project_root,
)

PROJECT_ROOT = project_root()
DATA_DIR = get_data_dir()
RATINGS_FILE = data_file("song_ratings.json")


def load_ratings():

    if not RATINGS_FILE.exists():
        return {}

    try:
        with open(RATINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return {}


def save_ratings(ratings):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(RATINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            ratings,
            file,
            indent=4
        )


def get_song_rating(track_id):

    if not track_id:
        return 0

    ratings = load_ratings()

    item = ratings.get(
        track_id,
        {}
    )

    return int(
        item.get("rating", 0)
    )


def set_song_rating(track_id, rating, song_name="", artist=""):

    if not track_id:
        raise RuntimeError(
            "No Spotify track ID found for this song."
        )

    rating = int(rating)

    rating = max(
        0,
        min(5, rating)
    )

    ratings = load_ratings()

    if rating == 0:

        if track_id in ratings:
            del ratings[track_id]

    else:

        ratings[track_id] = {
            "rating": rating,
            "song_name": song_name,
            "artist": artist,
        }

    save_ratings(
        ratings
    )

    return {
        "track_id": track_id,
        "rating": rating,
        "song_name": song_name,
        "artist": artist,
    }


def get_song_rating_from_cache(song, ratings):

    possible_keys = [
        song.id,
        song.uri,
    ]

    for key in possible_keys:

        if not key:
            continue

        if key in ratings:

            item = ratings.get(
                key,
                {}
            )

            return int(
                item.get("rating", 0)
            )

    return 0


def calculate_rating_analytics(tracks):
    """
    Calculates local rating analytics for the current playlist.
    """

    ratings = load_ratings()

    total_songs = len(
        tracks
    )

    if total_songs == 0:
        return {
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
        }

    rated_items = []
    unrated_count = 0

    distribution = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
    }

    for song in tracks:

        rating = get_song_rating_from_cache(
            song,
            ratings
        )

        if rating <= 0:
            unrated_count += 1
            continue

        distribution[rating] += 1

        rated_items.append({
            "name": song.name,
            "artist": song.artist,
            "album": song.album,
            "rating": rating,
        })

    rated_count = len(
        rated_items
    )

    if rated_count == 0:
        average_rating = 0
    else:
        average_rating = round(
            sum(item["rating"] for item in rated_items) / rated_count,
            2
        )

    rated_percentage = round(
        (rated_count / total_songs) * 100,
        1
    )

    unrated_percentage = round(
        (unrated_count / total_songs) * 100,
        1
    )

    five_star_songs = distribution[5]

    low_rated_items = [
        item
        for item in rated_items
        if item["rating"] <= 2
    ]

    top_rated_tracks = sorted(
        rated_items,
        key=lambda item: (
            item["rating"],
            item["name"].lower()
        ),
        reverse=True
    )[:5]

    low_rated_tracks = sorted(
        low_rated_items,
        key=lambda item: (
            item["rating"],
            item["name"].lower()
        )
    )[:5]

    rating_distribution = [
        (
            f"{rating} Star",
            count
        )
        for rating, count in distribution.items()
    ]

    return {
        "average_rating": average_rating,
        "rated_songs": rated_count,
        "unrated_songs": unrated_count,
        "rated_percentage": rated_percentage,
        "unrated_percentage": unrated_percentage,
        "five_star_songs": five_star_songs,
        "low_rated_songs": len(low_rated_items),
        "top_rated_tracks": top_rated_tracks,
        "low_rated_tracks": low_rated_tracks,
        "rating_distribution": rating_distribution,
    }