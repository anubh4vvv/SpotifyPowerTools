def score(candidate, previous_song):
    if previous_song is None:
        return 0

    if candidate.artist == previous_song.artist:
        return -50

    return 15