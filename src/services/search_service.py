from services.queue_service import spotify_track_to_song


def search_tracks(sp, query, limit=10):
    """
    Searches Spotify tracks.
    """

    query = query.strip()

    if not query:
        return []

    response = sp.search(
        q=query,
        type="track",
        limit=limit
    )

    tracks = response.get(
        "tracks",
        {}
    ).get(
        "items",
        []
    )

    songs = []

    for track in tracks:

        song = spotify_track_to_song(
            track
        )

        if song is not None:
            songs.append(song)

    return songs


def add_song_to_queue(sp, song):
    """
    Adds one searched song to Spotify queue.
    """

    if song is None:
        raise RuntimeError(
            "No song selected."
        )

    if not song.uri:
        raise RuntimeError(
            "Selected song does not have a Spotify URI."
        )

    sp.add_to_queue(
        song.uri
    )

    return {
        "song_name": song.name,
        "artist": song.artist,
        "message": f"Added to queue: {song.name} — {song.artist}",
    }