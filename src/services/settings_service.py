import json

from pathlib import Path


DEFAULT_SETTINGS = {
    "queue_size": 25,
    "shuffle_profile": "Balanced",
    "artist_weight": 50,
    "album_weight": 50,
    "randomness": 50,
}


VALID_QUEUE_SIZES = [10, 25, 50, 100]

VALID_PROFILES = [
    "Balanced",
    "Discovery",
    "Adaptive",
    "Album",
    "Random",
    "Weighted",
    "Custom",
]


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"


def clamp(value, minimum, maximum):
    return max(
        minimum,
        min(maximum, value)
    )


def sanitize_settings(settings):
    clean = DEFAULT_SETTINGS.copy()

    if isinstance(settings, dict):
        clean.update(settings)

    if clean["queue_size"] not in VALID_QUEUE_SIZES:
        clean["queue_size"] = DEFAULT_SETTINGS["queue_size"]

    if clean["shuffle_profile"] not in VALID_PROFILES:
        clean["shuffle_profile"] = DEFAULT_SETTINGS["shuffle_profile"]

    clean["artist_weight"] = clamp(
        int(clean["artist_weight"]),
        0,
        100
    )

    clean["album_weight"] = clamp(
        int(clean["album_weight"]),
        0,
        100
    )

    clean["randomness"] = clamp(
        int(clean["randomness"]),
        0,
        100
    )

    return clean


def load_settings():
    if not SETTINGS_FILE.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return sanitize_settings(data)

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    clean = sanitize_settings(settings)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            clean,
            file,
            indent=4
        )

    return clean


def reset_settings():
    return save_settings(
        DEFAULT_SETTINGS.copy()
    )