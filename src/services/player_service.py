def previous_song(sp):
    """
    Skips to the previous song in Spotify.
    """

    sp.previous_track()


def next_song(sp):
    """
    Skips to the next song in Spotify.
    """

    sp.next_track()


def toggle_playback(sp):
    """
    Toggles play/pause based on current playback state.
    """

    current = sp.current_playback()

    if current is None:
        raise RuntimeError(
            "No active Spotify playback found."
        )

    if current.get("is_playing"):
        sp.pause_playback()

        return {
            "is_playing": False,
            "message": "Playback paused",
        }

    sp.start_playback()

    return {
        "is_playing": True,
        "message": "Playback resumed",
    }