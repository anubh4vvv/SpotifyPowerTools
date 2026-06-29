from song_mapper import playlist_item_to_song
def get_current_playlist(sp, current):
    """
    Returns the playlist dictionary for the playlist
    that is currently playing.
    """

    if current is None:
        return None

    context = current.get("context")

    if context is None:
        return None

    if context["type"] != "playlist":
        return None

    playlist_uri = context["uri"]

    return sp.playlist(playlist_uri)

def get_playlist_tracks(sp, playlist):
    """
    Returns every track in the playlist,
    even if the playlist has more than 100 songs.
    """

    playlist_id = playlist["id"]

    tracks = []

    offset = 0

    while True:

        response = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=100
        )

        tracks.extend(response["items"])

        if len(response["items"]) < 100:
            break

        offset += 100

    songs = []

    for item in tracks:
        if item["item"] is not None:
            songs.append(playlist_item_to_song(item))

    return songs