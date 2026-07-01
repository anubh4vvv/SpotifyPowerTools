import json

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RATINGS_FILE = DATA_DIR / "song_ratings.json"


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