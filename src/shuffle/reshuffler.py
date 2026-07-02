import random

from models.shuffle_context import ShuffleContext

from shuffle.scoring import score_song

from shuffle.profile_config import resolve_shuffle_settings


def smart_shuffle(tracks, current_index, seed=None, settings=None):
    """
    Smart-shuffles the playlist while keeping the currently
    playing song as the first song.

    Returns only Song objects.
    """

    items = smart_shuffle_with_explanations(
        tracks,
        current_index,
        seed=seed,
        settings=settings
    )

    return [
        item["song"]
        for item in items
    ]


def smart_shuffle_with_explanations(tracks, current_index, seed=None, settings=None):
    """
    Smart-shuffles the playlist and returns explanation data.

    Returns:
    [
        {
            "song": Song,
            "score": float,
            "reasons": [...]
        }
    ]
    """

    if not tracks:
        return []

    if current_index < 0 or current_index >= len(tracks):

        return [
            {
                "song": song,
                "score": 0,
                "reasons": ["Original playlist order"]
            }
            for song in tracks
        ]

    resolved_settings = resolve_shuffle_settings(
        settings
    )

    artist_spacing = resolved_settings["artist_spacing"]
    album_spacing = resolved_settings["album_spacing"]

    rng = random.Random(seed)

    current = tracks[current_index]

    remaining = (
        tracks[:current_index]
        + tracks[current_index + 1:]
    )

    result = [
        {
            "song": current,
            "score": 0,
            "reasons": ["Currently playing"]
        }
    ]

    ordered_songs = [current]

    previous = current

    while remaining:

        context = ShuffleContext(
            previous_song=previous,
            recent_songs=ordered_songs[-max(artist_spacing, album_spacing):],
            artist_spacing=artist_spacing,
            album_spacing=album_spacing,
        )

        best_song = None
        best_score = float("-inf")
        best_reasons = []

        for song in remaining:

            score, reasons = score_song(
                song,
                context,
                rng,
                resolved_settings
            )

            if score > best_score:
                best_score = score
                best_song = song
                best_reasons = reasons

        if best_song is None:
            break

        result.append({
            "song": best_song,
            "score": round(best_score, 1),
            "reasons": best_reasons,
        })

        ordered_songs.append(
            best_song
        )

        remaining.remove(
            best_song
        )

        previous = best_song

    return result