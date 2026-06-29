def score(candidate, previous_song):
    if previous_song is None:
        return 0

    if candidate.album == previous_song.album:
        return -20

    return 5