from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


BASE_DIR = Path(__file__).resolve().parents[2]
CACHE_PATH = BASE_DIR / ".spotify_power_tools_cache"


SCOPE = (
    "user-read-private "
    "user-read-email "
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-read-private "
    "playlist-read-collaborative "
    "playlist-modify-private "
    "playlist-modify-public"
)


def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=str(CACHE_PATH),
        show_dialog=True
    )

    return spotipy.Spotify(auth_manager=auth_manager)


def add_to_queue(sp, song):
    """
    Adds a Song to Spotify's queue.
    """

    sp.add_to_queue(song.uri)