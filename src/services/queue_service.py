import requests

from models.song import Song


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


def get_access_token(sp):

    token_info = sp.auth_manager.get_cached_token()

    if token_info is None:
        token_info = sp.auth_manager.get_access_token(
            as_dict=True
        )

    return token_info["access_token"]


def spotify_track_to_song(track):

    if track is None:
        return None

    if track.get("type") != "track":
        return None

    album = track.get("album", {})

    images = album.get("images", [])

    image_url = ""

    if images:
        image_url = images[0]["url"]

    release_date = album.get("release_date", "")

    release_year = release_date[:4] if release_date else ""

    artists = track.get("artists", [])

    artist_name = "Unknown Artist"

    if artists:
        artist_name = artists[0].get("name", "Unknown Artist")

    return Song(
        id=track.get("id", ""),
        uri=track.get("uri", ""),
        name=track.get("name", "Unknown Track"),
        artist=artist_name,
        album=album.get("name", "Unknown Album"),
        duration_ms=track.get("duration_ms", 0),
        image_url=image_url,
        release_year=release_year,
        explicit=track.get("explicit", False),
        popularity=track.get("popularity", 0),
    )


def get_user_queue(sp, limit=50):
    """
    Gets the user's current Spotify queue.
    """

    access_token = get_access_token(sp)

    response = requests.get(
        "https://api.spotify.com/v1/me/player/queue",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    currently_playing = spotify_track_to_song(
        data.get("currently_playing")
    )

    queue_items = []

    for item in data.get("queue", []):

        song = spotify_track_to_song(item)

        if song is not None:
            queue_items.append(song)

        if len(queue_items) >= limit:
            break

    return {
        "currently_playing": currently_playing,
        "queue": queue_items,
    }