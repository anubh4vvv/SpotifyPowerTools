import random

from models.shuffle_context import ShuffleContext

from shuffle.scoring import score_song

from shuffle.profile_config import resolve_shuffle_settings


def smart_shuffle(tracks, current_index, seed=None, settings=None):
    """
    Smart-shuffles the playlist while keeping the currently
    playing song as the first song.
    """

    if not tracks:
        return []

    if current_index < 0 or current_index >= len(tracks):
        return tracks[:]

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

    result = [current]
    previous = current

    while remaining:

        context = ShuffleContext(
            previous_song=previous,
            recent_songs=result[-max(artist_spacing, album_spacing):],
            artist_spacing=artist_spacing,
            album_spacing=album_spacing,
        )

        best_song = None
        best_score = float("-inf")

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

        if best_song is None:
            break

        result.append(best_song)

        remaining.remove(best_song)

        previous = best_song

    return result