import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


SCOPE = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-read-private "
    "playlist-read-collaborative"
)


def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    return spotipy.Spotify(auth_manager=auth_manager)

def add_to_queue(sp, song):
    """
    Adds a Song to Spotify's queue.
    """

    sp.add_to_queue(song.id)