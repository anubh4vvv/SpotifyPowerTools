def get_current_track_index(current, tracks):
    """
    Returns the index of the currently playing song
    inside the playlist.
    """

    current_track_id = current["item"]["id"]

    for index, playlist_item in enumerate(tracks):

        for index, song in enumerate(tracks):

            if song.id == current_track_id:
                return index
    return -1