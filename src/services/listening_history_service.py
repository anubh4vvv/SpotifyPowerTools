import json

from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
HISTORY_FILE = DATA_DIR / "listening_history.json"

MAX_HISTORY_ITEMS = 500


def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_history(history):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4
        )


def get_track_key(track):

    if track is None:
        return ""

    return (
        track.get("id")
        or track.get("uri")
        or ""
    )


def record_played_track(track):

    track_key = get_track_key(
        track
    )

    if not track_key:
        return None

    artists = track.get(
        "artists",
        []
    )

    artist_name = "Unknown Artist"

    if artists:
        artist_name = artists[0].get(
            "name",
            "Unknown Artist"
        )

    album = track.get(
        "album",
        {}
    )

    event = {
        "track_id": track.get("id", ""),
        "track_uri": track.get("uri", ""),
        "track_key": track_key,
        "song_name": track.get("name", "Unknown Song"),
        "artist": artist_name,
        "album": album.get("name", "Unknown Album"),
        "played_at": datetime.now(timezone.utc).isoformat(),
    }

    history = load_history()

    if history:

        last_event = history[-1]

        if last_event.get("track_key") == track_key:
            return last_event

    history.append(
        event
    )

    history = history[-MAX_HISTORY_ITEMS:]

    save_history(
        history
    )

    return event


def get_recent_track_keys(limit=50):

    history = load_history()

    recent_keys = []

    seen = set()

    for event in reversed(history):

        track_key = (
            event.get("track_key")
            or event.get("track_id")
            or event.get("track_uri")
        )

        if not track_key:
            continue

        if track_key in seen:
            continue

        seen.add(
            track_key
        )

        recent_keys.append(
            track_key
        )

        if len(recent_keys) >= limit:
            break

    return recent_keys