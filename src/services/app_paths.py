import os
import shutil
import sys
from pathlib import Path


APP_NAME = "SpotifyPowerTools"


def is_frozen_app():
    return bool(
        getattr(sys, "frozen", False)
    )


def project_root():
    """
    Source project root during development.

    In a packaged app this may point inside the bundled app,
    so runtime data should not be stored here.
    """

    return Path(__file__).resolve().parents[2]


def executable_dir():
    if is_frozen_app():
        return Path(sys.executable).resolve().parent

    return project_root()


def get_app_data_dir():
    """
    User-writable app data folder.

    Windows:
        C:/Users/<user>/AppData/Roaming/SpotifyPowerTools

    Other systems:
        ~/.local/share/SpotifyPowerTools
    """

    if sys.platform == "win32":
        base = os.getenv("APPDATA")

        if base:
            path = Path(base) / APP_NAME
        else:
            path = Path.home() / "AppData" / "Roaming" / APP_NAME

    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / APP_NAME

    else:
        path = Path.home() / ".local" / "share" / APP_NAME

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def get_data_dir():
    path = get_app_data_dir() / "data"

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def copy_legacy_file_if_needed(target, legacy_paths):
    if target.exists():
        return target

    for legacy_path in legacy_paths:
        legacy_path = Path(legacy_path)

        if not legacy_path.exists():
            continue

        try:
            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                legacy_path,
                target
            )

            return target

        except Exception:
            return target

    return target


def data_file(filename):
    target = get_data_dir() / filename

    legacy_paths = [
        project_root() / "data" / filename,
    ]

    return copy_legacy_file_if_needed(
        target,
        legacy_paths
    )


def spotify_cache_file():
    target = get_app_data_dir() / ".spotify_power_tools_cache"

    legacy_paths = [
        project_root() / ".spotify_power_tools_cache",
    ]

    return copy_legacy_file_if_needed(
        target,
        legacy_paths
    )


def env_file_candidates():
    """
    Locations where the app may read Spotify credentials from.

    Development:
        project_root/.env

    Packaged app:
        folder beside SpotifyPowerTools.exe
        AppData/Roaming/SpotifyPowerTools/.env
    """

    candidates = [
        project_root() / ".env",
        Path.cwd() / ".env",
        executable_dir() / ".env",
        get_app_data_dir() / ".env",
    ]

    unique = []

    for path in candidates:
        if path not in unique:
            unique.append(path)

    return unique