def album_score(candidate, previous_song):
    """
    Reward songs from different albums.
    """

    if previous_song is None:
        return 0

    if candidate.album == previous_song.album:
        return -20

    return 10