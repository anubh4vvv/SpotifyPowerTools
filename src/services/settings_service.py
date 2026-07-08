import json

from services.app_paths import (
    data_file,
    get_data_dir,
    project_root,
)

DEFAULT_HOTKEYS = {
    "hotkey_play_pause": "ctrl+alt+space",
    "hotkey_next": "ctrl+alt+right",
    "hotkey_previous": "ctrl+alt+left",
    "hotkey_preview_shuffle": "ctrl+alt+p",
    "hotkey_queue_shuffle": "ctrl+alt+q",
    "hotkey_show_dashboard": "ctrl+alt+d",
    "hotkey_show_app": "ctrl+alt+s",
}


HOTKEY_LABELS = {
    "hotkey_play_pause": "Play / Pause",
    "hotkey_next": "Next Track",
    "hotkey_previous": "Previous Track",
    "hotkey_preview_shuffle": "Preview Smart Shuffle",
    "hotkey_queue_shuffle": "Queue Smart Shuffle",
    "hotkey_show_dashboard": "Show Dashboard",
    "hotkey_show_app": "Show / Restore App",
}


DEFAULT_SETTINGS = {
    "queue_size": 25,
    "shuffle_profile": "Balanced",
    "artist_weight": 50,
    "album_weight": 50,
    "randomness": 50,
    "hotkeys_enabled": True,
    "gaming_mode_enabled": False,
    **DEFAULT_HOTKEYS,
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


VALID_HOTKEY_KEYS = list(
    DEFAULT_HOTKEYS.keys()
)


PROJECT_ROOT = project_root()
DATA_DIR = get_data_dir()
SETTINGS_FILE = data_file("settings.json")


def clamp(value, minimum, maximum):
    return max(
        minimum,
        min(maximum, value)
    )


def bool_from_value(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "1",
            "yes",
            "on",
            "enabled",
        }

    return bool(value)


def normalize_hotkey(value, fallback):
    text = str(value or "").strip().lower()

    if not text:
        return fallback

    text = text.replace(" ", "")
    text = text.replace("control", "ctrl")
    text = text.replace("cmd", "windows")
    text = text.replace("win", "windows")
    text = text.replace("arrowleft", "left")
    text = text.replace("arrowright", "right")
    text = text.replace("arrowup", "up")
    text = text.replace("arrowdown", "down")
    text = text.replace("escape", "esc")

    parts = [
        part
        for part in text.split("+")
        if part
    ]

    if not parts:
        return fallback

    order = {
        "ctrl": 1,
        "alt": 2,
        "shift": 3,
        "windows": 4,
    }

    modifiers = []
    keys = []

    for part in parts:

        if part in order:
            if part not in modifiers:
                modifiers.append(part)

        else:
            keys.append(part)

    if not keys:
        return fallback

    modifiers.sort(
        key=lambda item: order.get(item, 99)
    )

    primary_key = keys[-1]

    return "+".join(
        modifiers + [primary_key]
    )


def sanitize_hotkeys(clean):
    clean["hotkeys_enabled"] = bool_from_value(
        clean.get(
            "hotkeys_enabled",
            True
        )
    )

    for key, default_value in DEFAULT_HOTKEYS.items():

        clean[key] = normalize_hotkey(
            clean.get(
                key,
                default_value
            ),
            default_value
        )

    return clean


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

    clean["gaming_mode_enabled"] = bool_from_value(
        clean.get(
            "gaming_mode_enabled",
            False
        )
    )

    clean = sanitize_hotkeys(
        clean
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


def reset_hotkeys(settings=None):
    clean = load_settings()

    if isinstance(settings, dict):
        clean.update(settings)

    clean["hotkeys_enabled"] = True

    for key, value in DEFAULT_HOTKEYS.items():
        clean[key] = value

    return save_settings(
        clean
    )


def hotkey_items_from_settings(settings):
    clean = sanitize_settings(
        settings
    )

    return [
        {
            "key": key,
            "label": HOTKEY_LABELS.get(
                key,
                key
            ),
            "value": clean.get(
                key,
                DEFAULT_HOTKEYS[key]
            ),
            "default": DEFAULT_HOTKEYS[key],
        }
        for key in VALID_HOTKEY_KEYS
    ]