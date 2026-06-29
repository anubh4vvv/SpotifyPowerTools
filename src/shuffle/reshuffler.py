import random

from shuffle.scoring import score_song


def smart_shuffle(tracks, current_index, seed=None):
    """
    Smart shuffle that avoids consecutive songs
    from the same artist and album.
    """

    rng = random.Random(seed)

    before = tracks[:current_index]

    current = tracks[current_index]

    remaining = tracks[current_index + 1:]

    result = before + [current]

    previous = current

    while remaining:

        best_song = None
        best_score = float("-inf")

        for song in remaining:

            score = score_song(song, previous, rng)

            if score > best_score:
                best_score = score
                best_song = song

        result.append(best_song)

        remaining.remove(best_song)

        previous = best_song

    return result