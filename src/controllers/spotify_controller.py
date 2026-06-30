from services.spotify_api import get_spotify_client
from services.playlist import (
    get_current_playlist,
    get_playlist_tracks,
)
from services.song_position import get_current_track_index

from shuffle.reshuffler import smart_shuffle


class SpotifyController:

    def __init__(self):

        self.sp = get_spotify_client()

        self._playlist = None
        self._tracks = None

        # Stores the last generated shuffle
        self._preview = []

    def current_playback(self):
        return self.sp.current_playback()

    def current_playlist(self):

        if self._playlist is not None:
            return self._playlist, self._tracks

        current = self.current_playback()

        playlist = get_current_playlist(
            self.sp,
            current
        )

        if playlist is None:
            return None, []

        tracks = get_playlist_tracks(
            self.sp,
            playlist
        )

        self._playlist = playlist
        self._tracks = tracks

        return playlist, tracks

    def preview_shuffle(self):

        current = self.current_playback()

        playlist, tracks = self.current_playlist()

        if playlist is None:
            return []

        index = get_current_track_index(
            current,
            tracks
        )

        shuffled = smart_shuffle(
            tracks,
            index
        )

        # Save every remaining song
        self._preview = shuffled[index + 1:]

        # Only display the first 10
        return self._preview[:10]

    def get_preview(self):
        return self._preview

    def apply_shuffle_playlist(self):
        """
        Placeholder.
        We will implement this after
        building temporary_playlist.py
        """
        pass

    def refresh_playlist(self):

        self._playlist = None
        self._tracks = None