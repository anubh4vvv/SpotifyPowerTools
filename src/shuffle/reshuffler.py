import random

from models.shuffle_context import ShuffleContext

from shuffle.scoring import score_song

from settings.shuffle_config import (
    ARTIST_SPACING,
    ALBUM_SPACING,
)


def smart_shuffle(tracks, current_index, seed=None):
    """
    Smart-shuffles the playlist while keeping the currently
    playing song as the first song.

    This fixes the "last song" issue because the shuffle now uses
    every other song in the playlist, not only songs after the
    current index.
    """

    if not tracks:
        return []

    if current_index < 0 or current_index >= len(tracks):
        return tracks[:]

    rng = random.Random(seed)

    current = tracks[current_index]

    # Use every song except the current one.
    # This makes the shuffle wrap naturally even if current song is last.
    remaining = (
        tracks[:current_index]
        + tracks[current_index + 1:]
    )

    result = [current]
    previous = current

    while remaining:

        context = ShuffleContext(
            previous_song=previous,
            recent_songs=result[-max(ARTIST_SPACING, ALBUM_SPACING):],
            artist_spacing=ARTIST_SPACING,
            album_spacing=ALBUM_SPACING,
        )

        best_song = None
        best_score = float("-inf")

        for song in remaining:

            score, reasons = score_song(
                song,
                context,
                rng
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