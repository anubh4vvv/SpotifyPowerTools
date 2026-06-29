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

    return sp.playlist(playlist_uri)


def get_playlist_tracks(playlist):
    """
    Returns every track in the playlist.
    """

    return playlist["items"]["items"]