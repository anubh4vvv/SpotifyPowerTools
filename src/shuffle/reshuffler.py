import random

from models.shuffle_context import ShuffleContext
from shuffle.scoring import score_song
from settings.shuffle_config import (
    ARTIST_SPACING,
    ALBUM_SPACING,
)


def smart_shuffle(tracks, current_index, seed=None):
    """
    Smart Shuffle V2

    Preserves songs before the current song and
    intelligently shuffles everything after it.
    """

    rng = random.Random(seed)

    before = tracks[:current_index]

    current = tracks[current_index]

    remaining = tracks[current_index + 1:]

    result = before + [current]

    previous = current

    while remaining:

        context = ShuffleContext(
            previous_song=previous,

            recent_songs=result[-
                                max(
                                    ARTIST_SPACING,
                                    ALBUM_SPACING
                                ):
            ],

            artist_spacing=ARTIST_SPACING,

            album_spacing=ALBUM_SPACING,
        )

        best_song = None
        best_score = float("-inf")
        best_reasons = []

        for song in remaining:

            score, reasons = score_song(
                song,
                context,
                rng
            )

            if score > best_score:
                best_score = score
                best_song = song
                best_reasons = reasons

        print(f"\nChosen: {best_song.name}")

        for reason in best_reasons:
            print(reason)

        print(f"Final Score: {best_score}")

        result.append(best_song)

        remaining.remove(best_song)

        previous = best_song

    return result