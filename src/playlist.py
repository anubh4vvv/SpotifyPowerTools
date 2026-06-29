def get_current_playlist(sp, current):
    """
    Returns the playlist dictionary for the playlist
    that is currently playing.
    """

    context = current.get("context")

    if context is None:
        return None

    if context["type"] != "playlist":
        return None

    playlist_uri = context["uri"]

    playlist = sp.playlist(playlist_uri)

    return playlist