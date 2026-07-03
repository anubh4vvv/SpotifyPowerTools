import json

from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
HISTORY_FILE = DATA_DIR / "listening_history.json"

MAX_HISTORY_ITEMS = 1000

FINISH_COMPLETION_THRESHOLD = 0.85
FINISH_NEAR_END_MS = 15000
SKIP_COMPLETION_THRESHOLD = 0.50
SKIP_PLAYED_MS_THRESHOLD = 30000


def utc_now():

    return datetime.now(
        timezone.utc
    ).isoformat()


def empty_history():

    return {
        "version": 2,
        "events": [],
        "tracks": {},
    }


def load_history():

    if not HISTORY_FILE.exists():
        return empty_history()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return normalize_history(
            data
        )

    except Exception:
        return empty_history()


def normalize_history(data):
    """
    Supports both:
    - old list-based history
    - new dict-based listening memory
    """

    if isinstance(data, dict):

        data.setdefault(
            "version",
            2
        )

        data.setdefault(
            "events",
            []
        )

        data.setdefault(
            "tracks",
            {}
        )

        return data

    if isinstance(data, list):

        history = empty_history()

        for event in data:

            if not isinstance(event, dict):
                continue

            track_key = (
                event.get("track_key")
                or event.get("track_id")
                or event.get("track_uri")
            )

            if not track_key:
                continue

            metadata = {
                "track_key": track_key,
                "track_id": event.get("track_id", ""),
                "track_uri": event.get("track_uri", ""),
                "song_name": event.get("song_name", "Unknown Song"),
                "artist": event.get("artist", "Unknown Artist"),
                "album": event.get("album", "Unknown Album"),
            }

            stats = ensure_track_stats(
                history,
                metadata
            )

            stats["play_count"] += 1
            stats["last_played_at"] = event.get(
                "played_at",
                utc_now()
            )
            stats["last_event"] = "started"

            history["events"].append({
                "type": "started",
                "track_key": track_key,
                "track_id": metadata["track_id"],
                "track_uri": metadata["track_uri"],
                "song_name": metadata["song_name"],
                "artist": metadata["artist"],
                "album": metadata["album"],
                "created_at": stats["last_played_at"],
            })

        history["events"] = history["events"][-MAX_HISTORY_ITEMS:]

        return history

    return empty_history()


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


def get_artist_name(track):

    artists = track.get(
        "artists",
        []
    )

    if not artists:
        return "Unknown Artist"

    return artists[0].get(
        "name",
        "Unknown Artist"
    )


def get_track_metadata(track):

    album = track.get(
        "album",
        {}
    )

    return {
        "track_key": get_track_key(track),
        "track_id": track.get("id", ""),
        "track_uri": track.get("uri", ""),
        "song_name": track.get("name", "Unknown Song"),
        "artist": get_artist_name(track),
        "album": album.get("name", "Unknown Album"),
    }


def ensure_track_stats(history, metadata):

    track_key = metadata["track_key"]

    tracks = history.setdefault(
        "tracks",
        {}
    )

    if track_key not in tracks:

        tracks[track_key] = {
            "track_key": track_key,
            "track_id": metadata.get("track_id", ""),
            "track_uri": metadata.get("track_uri", ""),
            "song_name": metadata.get("song_name", "Unknown Song"),
            "artist": metadata.get("artist", "Unknown Artist"),
            "album": metadata.get("album", "Unknown Album"),
            "play_count": 0,
            "finish_count": 0,
            "skip_count": 0,
            "replay_count": 0,
            "total_played_ms": 0,
            "last_played_at": "",
            "last_finished_at": "",
            "last_skipped_at": "",
            "last_replayed_at": "",
            "last_event": "",
        }

    else:

        tracks[track_key]["track_id"] = metadata.get(
            "track_id",
            tracks[track_key].get("track_id", "")
        )

        tracks[track_key]["track_uri"] = metadata.get(
            "track_uri",
            tracks[track_key].get("track_uri", "")
        )

        tracks[track_key]["song_name"] = metadata.get(
            "song_name",
            tracks[track_key].get("song_name", "Unknown Song")
        )

        tracks[track_key]["artist"] = metadata.get(
            "artist",
            tracks[track_key].get("artist", "Unknown Artist")
        )

        tracks[track_key]["album"] = metadata.get(
            "album",
            tracks[track_key].get("album", "Unknown Album")
        )

    return tracks[track_key]


def append_event(history, event):

    history.setdefault(
        "events",
        []
    )

    history["events"].append(
        event
    )

    history["events"] = history["events"][-MAX_HISTORY_ITEMS:]


def was_recently_started(history, track_key, limit=20):

    checked = 0

    for event in reversed(history.get("events", [])):

        if event.get("type") != "started":
            continue

        checked += 1

        if event.get("track_key") == track_key:
            return True

        if checked >= limit:
            break

    return False


def record_track_started(track, previous_track_key=None):
    """
    Records that a track started playing.

    This updates:
    - play_count
    - replay_count
    - last_played_at
    """

    if track is None:
        return None

    metadata = get_track_metadata(
        track
    )

    track_key = metadata["track_key"]

    if not track_key:
        return None

    history = load_history()

    stats = ensure_track_stats(
        history,
        metadata
    )

    now = utc_now()

    recently_started = was_recently_started(
        history,
        track_key,
        limit=20
    )

    stats["play_count"] += 1
    stats["last_played_at"] = now
    stats["last_event"] = "started"

    if recently_started or previous_track_key == track_key:

        stats["replay_count"] += 1
        stats["last_replayed_at"] = now
        stats["last_event"] = "replayed"

        event_type = "replayed"

    else:

        event_type = "started"

    event = {
        "type": event_type,
        "track_key": track_key,
        "track_id": metadata["track_id"],
        "track_uri": metadata["track_uri"],
        "song_name": metadata["song_name"],
        "artist": metadata["artist"],
        "album": metadata["album"],
        "created_at": now,
        "previous_track_key": previous_track_key or "",
    }

    append_event(
        history,
        event
    )

    save_history(
        history
    )

    return event


def finalize_track_play(
    track_key,
    duration_ms=0,
    max_progress_ms=0,
    last_progress_ms=0,
    played_ms=0
):
    """
    Finalizes the previous track when playback moves to another song.

    Decides whether the previous track was:
    - finished
    - skipped
    - partial
    """

    if not track_key:
        return None

    history = load_history()

    tracks = history.setdefault(
        "tracks",
        {}
    )

    if track_key not in tracks:
        return None

    stats = tracks[track_key]

    duration_ms = int(
        duration_ms or 0
    )

    max_progress_ms = int(
        max_progress_ms or 0
    )

    last_progress_ms = int(
        last_progress_ms or 0
    )

    played_ms = int(
        played_ms or 0
    )

    completion_ratio = 0

    if duration_ms > 0:

        completion_ratio = max_progress_ms / duration_ms

    near_end = (
        duration_ms > 0
        and duration_ms - max_progress_ms <= FINISH_NEAR_END_MS
    )

    finished = (
        completion_ratio >= FINISH_COMPLETION_THRESHOLD
        or near_end
    )

    skipped = (
        not finished
        and (
            completion_ratio < SKIP_COMPLETION_THRESHOLD
            or played_ms < SKIP_PLAYED_MS_THRESHOLD
        )
    )

    now = utc_now()

    stats["total_played_ms"] = int(
        stats.get("total_played_ms", 0)
    ) + max(played_ms, 0)

    if finished:

        event_type = "finished"
        stats["finish_count"] += 1
        stats["last_finished_at"] = now
        stats["last_event"] = "finished"

    elif skipped:

        event_type = "skipped"
        stats["skip_count"] += 1
        stats["last_skipped_at"] = now
        stats["last_event"] = "skipped"

    else:

        event_type = "partial"
        stats["last_event"] = "partial"

    event = {
        "type": event_type,
        "track_key": track_key,
        "song_name": stats.get("song_name", "Unknown Song"),
        "artist": stats.get("artist", "Unknown Artist"),
        "album": stats.get("album", "Unknown Album"),
        "duration_ms": duration_ms,
        "max_progress_ms": max_progress_ms,
        "last_progress_ms": last_progress_ms,
        "played_ms": played_ms,
        "completion_ratio": round(
            completion_ratio,
            3
        ),
        "created_at": now,
    }

    append_event(
        history,
        event
    )

    save_history(
        history
    )

    return event


def record_played_track(track):
    """
    Backward-compatible function.

    Older code can still call this, but new code should use
    record_track_started + finalize_track_play.
    """

    return record_track_started(
        track
    )


def get_recent_track_keys(limit=50):

    history = load_history()

    recent_keys = []

    seen = set()

    for event in reversed(history.get("events", [])):

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


def get_listening_memory_map():

    history = load_history()

    return history.get(
        "tracks",
        {}
    )


def calculate_track_rates(stats):

    play_count = int(
        stats.get("play_count", 0)
    )

    finish_count = int(
        stats.get("finish_count", 0)
    )

    skip_count = int(
        stats.get("skip_count", 0)
    )

    if play_count <= 0:
        return {
            "skip_rate": 0,
            "completion_rate": 0,
        }

    skip_rate = round(
        skip_count / play_count,
        3
    )

    completion_rate = round(
        finish_count / play_count,
        3
    )

    return {
        "skip_rate": skip_rate,
        "completion_rate": completion_rate,
    }
def make_listening_item(stats):

    rates = calculate_track_rates(
        stats
    )

    skip_rate_percent = round(
        rates["skip_rate"] * 100,
        1
    )

    completion_rate_percent = round(
        rates["completion_rate"] * 100,
        1
    )

    return {
        "track_key": stats.get("track_key", ""),
        "song_name": stats.get("song_name", "Unknown Song"),
        "artist": stats.get("artist", "Unknown Artist"),
        "album": stats.get("album", "Unknown Album"),
        "play_count": int(stats.get("play_count", 0)),
        "finish_count": int(stats.get("finish_count", 0)),
        "skip_count": int(stats.get("skip_count", 0)),
        "replay_count": int(stats.get("replay_count", 0)),
        "skip_rate": skip_rate_percent,
        "completion_rate": completion_rate_percent,
        "last_played_at": stats.get("last_played_at", ""),
        "last_finished_at": stats.get("last_finished_at", ""),
        "last_skipped_at": stats.get("last_skipped_at", ""),
        "last_replayed_at": stats.get("last_replayed_at", ""),
        "last_event": stats.get("last_event", ""),
    }


def make_event_item(event):

    return {
        "track_key": event.get("track_key", ""),
        "song_name": event.get("song_name", "Unknown Song"),
        "artist": event.get("artist", "Unknown Artist"),
        "album": event.get("album", "Unknown Album"),
        "type": event.get("type", ""),
        "created_at": event.get("created_at", ""),
    }


def get_recent_events_by_type(events, event_type, limit=5):

    results = []

    for event in reversed(events):

        if event.get("type") != event_type:
            continue

        results.append(
            make_event_item(event)
        )

        if len(results) >= limit:
            break

    return results


def calculate_listening_streaks(events):

    final_events = [
        event
        for event in reversed(events)
        if event.get("type") in ["finished", "skipped", "partial"]
    ]

    finished_streak = 0

    for event in final_events:

        if event.get("type") == "finished":
            finished_streak += 1
        else:
            break

    skip_streak = 0

    for event in final_events:

        if event.get("type") == "skipped":
            skip_streak += 1
        else:
            break

    start_events = [
        event
        for event in reversed(events)
        if event.get("type") in ["started", "replayed"]
    ]

    artist_streak_name = "N/A"
    artist_streak_count = 0

    album_streak_name = "N/A"
    album_streak_count = 0

    if start_events:

        artist_streak_name = start_events[0].get(
            "artist",
            "Unknown Artist"
        )

        album_streak_name = start_events[0].get(
            "album",
            "Unknown Album"
        )

        for event in start_events:

            if event.get("artist") == artist_streak_name:
                artist_streak_count += 1
            else:
                break

        for event in start_events:

            if event.get("album") == album_streak_name:
                album_streak_count += 1
            else:
                break

    return {
        "finished_streak": finished_streak,
        "skip_streak": skip_streak,
        "artist_streak_name": artist_streak_name,
        "artist_streak_count": artist_streak_count,
        "album_streak_name": album_streak_name,
        "album_streak_count": album_streak_count,
    }


def get_listening_analytics(limit=5):

    history = load_history()

    memory = history.get(
        "tracks",
        {}
    )

    events = history.get(
        "events",
        []
    )

    items = [
        make_listening_item(stats)
        for stats in memory.values()
    ]

    total_known_songs = len(
        items
    )

    total_plays = sum(
        item["play_count"]
        for item in items
    )

    total_finishes = sum(
        item["finish_count"]
        for item in items
    )

    total_skips = sum(
        item["skip_count"]
        for item in items
    )

    total_replays = sum(
        item["replay_count"]
        for item in items
    )

    if total_plays > 0:
        global_skip_rate = round(
            (total_skips / total_plays) * 100,
            1
        )
        global_completion_rate = round(
            (total_finishes / total_plays) * 100,
            1
        )
    else:
        global_skip_rate = 0
        global_completion_rate = 0

    most_replayed = sorted(
        [
            item
            for item in items
            if item["replay_count"] > 0
        ],
        key=lambda item: item["replay_count"],
        reverse=True
    )[:limit]

    most_skipped = sorted(
        [
            item
            for item in items
            if item["skip_count"] > 0
        ],
        key=lambda item: item["skip_count"],
        reverse=True
    )[:limit]

    best_completion = sorted(
        [
            item
            for item in items
            if item["play_count"] >= 2
        ],
        key=lambda item: (
            item["completion_rate"],
            item["finish_count"]
        ),
        reverse=True
    )[:limit]

    worst_skip_rate = sorted(
        [
            item
            for item in items
            if item["play_count"] >= 2
        ],
        key=lambda item: (
            item["skip_rate"],
            item["skip_count"]
        ),
        reverse=True
    )[:limit]

    recently_finished = get_recent_events_by_type(
        events,
        "finished",
        limit=limit
    )

    recently_played = []

    for event in reversed(events):

        if event.get("type") not in ["started", "replayed"]:
            continue

        recently_played.append(
            make_event_item(event)
        )

        if len(recently_played) >= limit:
            break

    recently_skipped = get_recent_events_by_type(
        events,
        "skipped",
        limit=limit
    )

    recently_replayed = get_recent_events_by_type(
        events,
        "replayed",
        limit=limit
    )

    streaks = calculate_listening_streaks(
        events
    )

    return {
        "total_known_songs": total_known_songs,
        "total_plays": total_plays,
        "total_finishes": total_finishes,
        "total_skips": total_skips,
        "total_replays": total_replays,
        "global_skip_rate": global_skip_rate,
        "global_completion_rate": global_completion_rate,
        "most_replayed": most_replayed,
        "most_skipped": most_skipped,
        "best_completion": best_completion,
        "worst_skip_rate": worst_skip_rate,
        "recently_finished": recently_finished,
        "recently_played": recently_played,
        "recently_skipped": recently_skipped,
        "recently_replayed": recently_replayed,
        "streaks": streaks,
    }


def export_listening_memory():

    history = load_history()

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    export_file = DATA_DIR / f"listening_memory_export_{timestamp}.json"

    with open(export_file, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4
        )

    return str(
        export_file
    )


def clear_listening_memory():

    save_history(
        empty_history()
    )

    return str(
        HISTORY_FILE
    )
    