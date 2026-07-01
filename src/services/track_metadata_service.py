_TRACK_METADATA_CACHE = {}


def get_track_metadata(sp, track):
    """
    Gets full Spotify track metadata and caches it.

    This is used for fields that are not always present in
    current_playback(), such as popularity.
    """

    if track is None:
        return {}

    track_id = track.get("id")

    track_uri = track.get(
        "uri",
        ""
    )

    if not track_id and track_uri.startswith("spotify:track:"):
        track_id = track_uri.split(":")[-1]

    if not track_id:
        return {
            "popularity": "Unavailable",
            "reason": "No Spotify track ID found",
        }

    if track_id in _TRACK_METADATA_CACHE:
        return _TRACK_METADATA_CACHE[track_id]

    full_track = sp.track(
        track_id
    )

    metadata = {
        "id": full_track.get("id", ""),
        "name": full_track.get("name", ""),
        "popularity": full_track.get("popularity"),
        "external_url": full_track.get(
            "external_urls",
            {}
        ).get(
            "spotify",
            ""
        ),
        "reason": "Loaded from Spotify track endpoint",
    }

    _TRACK_METADATA_CACHE[track_id] = metadata

    return metadata