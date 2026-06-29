def artist_score(candidate, previous_song):
    """
    Reward songs from different artists.
    """

    if previous_song is None:
        return 0

    if candidate.artist == previous_song.artist:
        return -50

    return 20