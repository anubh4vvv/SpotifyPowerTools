import requests


TEMP_PLAYLIST_NAME = "Spotify Power Tools - Smart Shuffle"


def get_access_token(sp):
    token_info = sp.auth_manager.get_cached_token()

    if token_info is None:
        token_info = sp.auth_manager.get_access_token(
            as_dict=True
        )

    return token_info["access_token"]


def create_playlist_for_current_user(sp):
    """
    Creates the Smart Shuffle playlist using Spotify's current /me/playlists endpoint.
    """

    access_token = get_access_token(sp)

    response = requests.post(
        "https://api.spotify.com/v1/me/playlists",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={
            "name": TEMP_PLAYLIST_NAME,
            "public": False,
            "collaborative": False,
            "description": (
                "Smart-shuffled playlist created by Spotify Power Tools. "
                "Your original playlist is not modified."
            ),
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_or_create_temp_playlist(sp):
    """
    Finds the app's temporary Smart Shuffle playlist.
    If it does not exist, creates it.
    """

    user = sp.current_user()
    user_id = user["id"]

    offset = 0

    while True:
        response = sp.current_user_playlists(
            limit=50,
            offset=offset
        )

        playlists = response["items"]

        for playlist in playlists:
            if (
                playlist["name"] == TEMP_PLAYLIST_NAME
                and playlist["owner"]["id"] == user_id
            ):
                return playlist

        if response["next"] is None:
            break

        offset += 50

    return create_playlist_for_current_user(sp)


def replace_playlist_tracks(sp, playlist_id, songs):
    """
    Replaces all tracks in the temporary playlist.
    Spotify only allows 100 tracks per request.
    """

    uris = [
        song.uri
        for song in songs
        if song is not None and song.uri
    ]

    if not uris:
        sp.playlist_replace_items(
            playlist_id,
            []
        )

        return 0

    sp.playlist_replace_items(
        playlist_id,
        uris[:100]
    )

    for start in range(100, len(uris), 100):
        sp.playlist_add_items(
            playlist_id,
            uris[start:start + 100]
        )

    return len(uris)