from collections import defaultdict


def format_duration(ms):

    total_seconds = ms // 1000

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:02d}"


def get_track_key(song):
    """
    Prefer Spotify track ID for duplicate detection.
    If ID is missing, fall back to song name + artist.
    """

    if song.id:
        return song.id

    return f"{song.name.lower()}::{song.artist.lower()}"


def analyze_duplicates(tracks):
    """
    Returns duplicate analysis for the current playlist.

    This is read-only. It does not modify Spotify.
    """

    groups = defaultdict(list)

    for song in tracks:
        key = get_track_key(song)
        groups[key].append(song)

    duplicate_groups = []

    for songs in groups.values():

        if len(songs) <= 1:
            continue

        first = songs[0]

        duplicate_groups.append({
            "name": first.name,
            "artist": first.artist,
            "album": first.album,
            "release_year": first.release_year or "Unknown",
            "duration": format_duration(first.duration_ms),
            "total_copies": len(songs),
            "extra_copies": len(songs) - 1,
        })

    duplicate_groups.sort(
        key=lambda item: item["extra_copies"],
        reverse=True
    )

    extra_copies = sum(
        item["extra_copies"]
        for item in duplicate_groups
    )

    return {
        "total_songs": len(tracks),
        "unique_duplicate_tracks": len(duplicate_groups),
        "extra_copies": extra_copies,
        "duplicates": duplicate_groups,
    }