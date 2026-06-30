import requests


def get_track_key(song):
    if song.id:
        return song.id

    return f"{song.name.lower()}::{song.artist.lower()}"


def get_unique_tracks(tracks):
    """
    Keeps the first copy of each song and removes later duplicates.
    Preserves original playlist order.
    """

    seen = set()
    unique_tracks = []

    for song in tracks:

        if song is None:
            continue

        key = get_track_key(song)

        if key in seen:
            continue

        seen.add(key)
        unique_tracks.append(song)

    return unique_tracks


def get_access_token(sp):
    token_info = sp.auth_manager.get_cached_token()

    if token_info is None:
        token_info = sp.auth_manager.get_access_token(
            as_dict=True
        )

    return token_info["access_token"]


def create_playlist_for_current_user(sp, name, description):
    """
    Creates a private playlist for the current Spotify user.
    """

    access_token = get_access_token(sp)

    response = requests.post(
        "https://api.spotify.com/v1/me/playlists",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={
            "name": name,
            "public": False,
            "collaborative": False,
            "description": description,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def upload_tracks_to_playlist(sp, playlist_id, songs):
    """
    Uploads tracks to a playlist in batches of 100.
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


def create_cleaned_playlist(sp, playlist, tracks):
    """
    Creates a safe cleaned copy of the current playlist.
    The original playlist is never modified.
    """

    if playlist is None:
        raise RuntimeError(
            "No playlist is currently playing."
        )

    if not tracks:
        raise RuntimeError(
            "No tracks found in the current playlist."
        )

    unique_tracks = get_unique_tracks(
        tracks
    )

    removed_count = len(tracks) - len(unique_tracks)

    cleaned_name = (
        f"{playlist['name']} - Cleaned by Spotify Power Tools"
    )

    description = (
        "Cleaned copy created by Spotify Power Tools. "
        "Duplicate extra copies were removed. "
        "The original playlist was not modified."
    )

    cleaned_playlist = create_playlist_for_current_user(
        sp,
        cleaned_name,
        description
    )

    uploaded_count = upload_tracks_to_playlist(
        sp,
        cleaned_playlist["id"],
        unique_tracks
    )

    return {
        "playlist_name": cleaned_playlist["name"],
        "playlist_url": cleaned_playlist["external_urls"]["spotify"],
        "original_count": len(tracks),
        "cleaned_count": uploaded_count,
        "removed_count": removed_count,
    }