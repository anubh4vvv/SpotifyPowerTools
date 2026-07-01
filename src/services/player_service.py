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


def set_volume(sp, volume_percent):
    """
    Sets Spotify playback volume.
    """

    volume_percent = int(volume_percent)

    volume_percent = max(
        0,
        min(100, volume_percent)
    )

    sp.volume(
        volume_percent
    )

    return {
        "volume_percent": volume_percent,
        "message": f"Volume set to {volume_percent}%",
    }


def toggle_shuffle(sp):
    """
    Toggles Spotify shuffle mode.
    """

    current = sp.current_playback()

    if current is None:
        raise RuntimeError(
            "No active Spotify playback found."
        )

    new_state = not current.get(
        "shuffle_state",
        False
    )

    sp.shuffle(
        new_state
    )

    return {
        "shuffle_state": new_state,
        "message": "Shuffle enabled" if new_state else "Shuffle disabled",
    }


def set_repeat_mode(sp, repeat_state):
    """
    Sets Spotify repeat mode.

    Valid states:
    - off
    - track
    - context
    """

    valid_states = [
        "off",
        "track",
        "context",
    ]

    if repeat_state not in valid_states:
        raise ValueError(
            "Invalid repeat mode."
        )

    sp.repeat(
        repeat_state
    )

    labels = {
        "off": "Repeat off",
        "track": "Repeat track",
        "context": "Repeat playlist/context",
    }

    return {
        "repeat_state": repeat_state,
        "message": labels[repeat_state],
    }