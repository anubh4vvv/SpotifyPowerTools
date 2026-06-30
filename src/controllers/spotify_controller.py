from services.spotify_api import get_spotify_client

from services.playlist import (
    get_current_playlist,
    get_playlist_tracks,
)

from services.song_position import get_current_track_index

from services.temporary_playlist import (
    get_or_create_temp_playlist,
    replace_playlist_tracks,
)

from services.queue_service import (
    queue_songs,
    DEFAULT_QUEUE_LIMIT,
)

from shuffle.reshuffler import smart_shuffle


class SpotifyController:

    def __init__(self):

        self.sp = get_spotify_client()

        self._playlist = None
        self._tracks = None

        # Full list after current song
        self._preview = []

        # Full smart-shuffled playlist order
        self._shuffled = []

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

        if current is None:
            return []

        playlist, tracks = self.current_playlist()

        if playlist is None:
            return []

        index = get_current_track_index(
            current,
            tracks
        )

        if index == -1:
            return []

        shuffled = smart_shuffle(
            tracks,
            index
        )

        self._shuffled = shuffled

        # All songs after the current song
        self._preview = shuffled[index + 1:]

        # Only show first 10 in GUI
        return self._preview[:10]

    def get_preview(self):
        return self._preview

    def get_full_shuffle(self):

        if not self._shuffled:
            self.preview_shuffle()

        return self._shuffled

    def queue_smart_shuffle(self, limit=DEFAULT_QUEUE_LIMIT):
        """
        Adds the next smart-shuffled songs to the Spotify queue.
        This keeps playback in the user's current Spotify session.
        """

        playlist, tracks = self.current_playlist()

        if playlist is None:
            raise RuntimeError(
                "No Spotify playlist is currently playing."
            )

        if not self._preview:
            self.preview_shuffle()

        songs_to_queue = self._preview[:limit]

        if not songs_to_queue:
            raise RuntimeError(
                "No songs available to queue. Try Preview Shuffle first."
            )

        queued_count = queue_songs(
            self.sp,
            songs_to_queue,
            limit
        )

        return {
            "queued_count": queued_count,
            "playlist_name": playlist["name"],
            "queue_limit": limit,
        }

    def apply_shuffle_playlist(self):
        """
        Backup/export feature:
        creates or updates the safe temporary Smart Shuffle playlist.
        This does NOT modify the original playlist.
        """

        playlist, tracks = self.current_playlist()

        if playlist is None:
            raise RuntimeError(
                "No Spotify playlist is currently playing."
            )

        shuffled = self.get_full_shuffle()

        if not shuffled:
            raise RuntimeError(
                "Could not generate Smart Shuffle."
            )

        temp_playlist = get_or_create_temp_playlist(
            self.sp
        )

        track_count = replace_playlist_tracks(
            self.sp,
            temp_playlist["id"],
            shuffled
        )

        return {
            "playlist_name": temp_playlist["name"],
            "playlist_url": temp_playlist["external_urls"]["spotify"],
            "track_count": track_count,
        }

    def refresh_playlist(self):

        self._playlist = None
        self._tracks = None
        self._preview = []
        self._shuffled = []