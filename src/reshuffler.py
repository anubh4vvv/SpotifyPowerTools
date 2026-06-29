import random


def reshuffle_remaining(tracks, current_index, seed=None):
    """
    Shuffle the playlist while keeping the current song fixed.

    Parameters
    ----------
    tracks : list
        Playlist tracks.
    current_index : int
        Index of the currently playing track.
    seed : int | None
        Optional random seed for reproducible shuffles.
    """

    rng = random.Random(seed)

    before = tracks[:current_index]
    current = tracks[current_index]
    after = tracks[current_index + 1:]

    rng.shuffle(before)
    rng.shuffle(after)

    return before + [current] + after