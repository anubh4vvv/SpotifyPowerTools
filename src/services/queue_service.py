DEFAULT_QUEUE_LIMIT = 25


def queue_songs(sp, songs, limit=DEFAULT_QUEUE_LIMIT):
    """
    Adds smart-shuffled songs to the user's Spotify queue.

    Spotify does not provide a public API to clear the queue,
    so this safely appends songs to the existing queue.
    """

    queued_count = 0

    for song in songs[:limit]:

        if song is None:
            continue

        if not song.uri:
            continue

        sp.add_to_queue(song.uri)

        queued_count += 1

    return queued_count