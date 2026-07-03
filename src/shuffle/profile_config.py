BALANCED_PROFILE = {
    "artist_weight": 2.0,
    "album_weight": 1.0,
    "random_weight": 1.0,
    "rating_weight": 0.0,
    "history_weight": 1.0,
    "adaptive_mode": False,
    "artist_spacing": 5,
    "album_spacing": 3,
}

DISCOVERY_PROFILE = {
    "artist_weight": 3.5,
    "album_weight": 2.0,
    "random_weight": 0.8,
    "rating_weight": 0.3,
    "history_weight": 1.8,
    "adaptive_mode": False,
    "artist_spacing": 8,
    "album_spacing": 5,
}

ADAPTIVE_PROFILE = {
    "artist_weight": 2.4,
    "album_weight": 1.2,
    "random_weight": 0.7,
    "rating_weight": 2.0,
    "history_weight": 2.5,
    "adaptive_mode": True,
    "artist_spacing": 6,
    "album_spacing": 3,
}

ALBUM_PROFILE = {
    "artist_weight": 1.0,
    "album_weight": 0.3,
    "random_weight": 0.9,
    "rating_weight": 0.2,
    "history_weight": 0.5,
    "adaptive_mode": False,
    "artist_spacing": 3,
    "album_spacing": 1,
}

RANDOM_PROFILE = {
    "artist_weight": 0.4,
    "album_weight": 0.2,
    "random_weight": 3.0,
    "rating_weight": 0.0,
    "history_weight": 0.0,
    "adaptive_mode": False,
    "artist_spacing": 1,
    "album_spacing": 1,
}

WEIGHTED_PROFILE = {
    "artist_weight": 1.0,
    "album_weight": 0.4,
    "random_weight": 0.3,
    "rating_weight": 5.0,
    "history_weight": 1.6,
    "adaptive_mode": False,
    "artist_spacing": 3,
    "album_spacing": 2,
}


PROFILES = {
    "Balanced": BALANCED_PROFILE,
    "Discovery": DISCOVERY_PROFILE,
    "Adaptive": ADAPTIVE_PROFILE,
    "Album": ALBUM_PROFILE,
    "Random": RANDOM_PROFILE,
    "Weighted": WEIGHTED_PROFILE,
}


def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(maximum, value)
    )


def preserve_extra_settings(resolved_settings, original_settings):
    """
    Keeps extra data passed into the shuffle engine.
    """

    extra_keys = [
        "ratings",
        "recent_track_keys",
        "listening_memory",
        "queue_size",
        "adaptive_mode",
    ]

    for key in extra_keys:

        if key in original_settings:
            resolved_settings[key] = original_settings[key]

    return resolved_settings


def resolve_shuffle_settings(settings=None):
    """
    Converts saved/UI settings into actual shuffle-engine values.
    """

    if settings is None:
        settings = {}

    if (
        "random_weight" in settings
        and "artist_spacing" in settings
        and "album_spacing" in settings
    ):

        resolved_settings = settings.copy()

        return preserve_extra_settings(
            resolved_settings,
            settings
        )

    profile = settings.get(
        "shuffle_profile",
        "Balanced"
    )

    if profile in PROFILES and profile != "Custom":

        resolved_settings = PROFILES[profile].copy()

        return preserve_extra_settings(
            resolved_settings,
            settings
        )

    artist_value = int(
        settings.get("artist_weight", 50)
    )

    album_value = int(
        settings.get("album_weight", 50)
    )

    randomness_value = int(
        settings.get("randomness", 50)
    )

    artist_value = clamp(
        artist_value,
        0,
        100
    )

    album_value = clamp(
        album_value,
        0,
        100
    )

    randomness_value = clamp(
        randomness_value,
        0,
        100
    )

    resolved_settings = {
        "artist_weight": round(artist_value / 25, 2),
        "album_weight": round(album_value / 50, 2),
        "random_weight": round(max(0.1, randomness_value / 50), 2),
        "rating_weight": 1.5,
        "history_weight": 1.0,
        "adaptive_mode": False,
        "artist_spacing": 2 + artist_value // 20,
        "album_spacing": 1 + album_value // 25,
    }

    return preserve_extra_settings(
        resolved_settings,
        settings
    )