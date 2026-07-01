from services.spotify_api import get_spotify_client

from services.cleaner_service import (
    create_cleaned_playlist as create_cleaned_playlist_service,
)

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
    get_user_queue as get_user_queue_service,
)

from services.settings_service import load_settings

from shuffle.reshuffler import smart_shuffle

from services.player_service import (
    previous_song as previous_song_service,
    next_song as next_song_service,
    toggle_playback as toggle_playback_service,
    set_volume as set_volume_service,
    toggle_shuffle as toggle_shuffle_service,
    set_repeat_mode as set_repeat_mode_service,
)


class SpotifyController:

    def __init__(self):

        self.sp = get_spotify_client()

        self._playlist = None
        self._tracks = None

        self._preview = []
        self._shuffled = []

        # Used to detect stale preview data
        self._current_context_key = None
        self._preview_context_key = None
        self._preview_settings_key = None

    def current_playback(self):
        return self.sp.current_playback()

    def _playlist_id_from_playback(self, current):

        if current is None:
            return None

        context = current.get("context")

        if context is None:
            return None

        if context.get("type") != "playlist":
            return None

        uri = context.get("uri", "")

        return uri.split(":")[-1]

    def _make_context_key(self, current, playlist):

        if current is None or playlist is None:
            return None

        track = current.get("item")

        if track is None:
            return None

        return (
            playlist.get("id"),
            track.get("id"),
        )

    def _resolve_settings(self, settings):

        if settings is None:
            return load_settings()

        return settings

    def _make_settings_key(self, settings):

        settings = self._resolve_settings(
            settings
        )

        return (
            settings.get("shuffle_profile"),
            settings.get("artist_weight"),
            settings.get("album_weight"),
            settings.get("randomness"),
        )

    def _clear_shuffle_cache(self):

        self._preview = []
        self._shuffled = []
        self._preview_context_key = None
        self._preview_settings_key = None

    def _sync_context(self, current, playlist):

        context_key = self._make_context_key(
            current,
            playlist
        )

        if context_key != self._current_context_key:

            self._clear_shuffle_cache()

            self._current_context_key = context_key

    def current_playlist(self, current=None):

        if current is None:
            current = self.current_playback()

        playlist_id = self._playlist_id_from_playback(
            current
        )

        if playlist_id is None:

            self._playlist = None
            self._tracks = None
            self._clear_shuffle_cache()

            return None, []

        if (
            self._playlist is not None
            and self._tracks is not None
            and self._playlist.get("id") == playlist_id
        ):

            self._sync_context(
                current,
                self._playlist
            )

            return self._playlist, self._tracks

        playlist = get_current_playlist(
            self.sp,
            current
        )

        if playlist is None:

            self._playlist = None
            self._tracks = None
            self._clear_shuffle_cache()

            return None, []

        tracks = get_playlist_tracks(
            self.sp,
            playlist
        )

        self._playlist = playlist
        self._tracks = tracks

        self._sync_context(
            current,
            playlist
        )

        return playlist, tracks

    def preview_shuffle(self, settings=None):

        current = self.current_playback()

        if current is None:
            return []

        playlist, tracks = self.current_playlist(
            current
        )

        if playlist is None:
            return []

        index = get_current_track_index(
            current,
            tracks
        )

        if index == -1:
            return []

        shuffle_settings = self._resolve_settings(
            settings
        )
        shuffled = smart_shuffle(
            tracks,
            index,
            settings=shuffle_settings
        )

        self._shuffled = shuffled
        self._preview = shuffled[1:]

        self._preview_context_key = self._make_context_key(
            current,
            playlist
        )
        self._preview_settings_key = self._make_settings_key(
            shuffle_settings
        )

        return self._preview[:10]

    def set_volume(self, volume_percent):
        """
        Sets Spotify playback volume.
        """

        return set_volume_service(
            self.sp,
            volume_percent
        )

    def toggle_shuffle(self):
        """
        Toggles Spotify shuffle mode.
        """

        return toggle_shuffle_service(
            self.sp
        )

    def set_repeat_mode(self, repeat_state):
        """
        Sets Spotify repeat mode.
        """

        return set_repeat_mode_service(
            self.sp,
            repeat_state
        )

    def get_preview(self):
        return self._preview

    def get_full_shuffle(self):

        if not self._shuffled:
            self.preview_shuffle()

        return self._shuffled

    def queue_smart_shuffle(self, limit=DEFAULT_QUEUE_LIMIT, settings=None):
        """
        Adds smart-shuffled songs to the Spotify queue.
        If the song or playlist changed after previewing,
        the preview is regenerated automatically.
        """

        current = self.current_playback()

        if current is None:
            raise RuntimeError(
                "Spotify is not currently playing anything."
            )

        playlist, tracks = self.current_playlist(
            current
        )

        if playlist is None:
            raise RuntimeError(
                "No Spotify playlist is currently playing."
            )

        current_context_key = self._make_context_key(
            current,
            playlist
        )
        shuffle_settings = self._resolve_settings(
            settings
        )

        settings_key = self._make_settings_key(
            shuffle_settings
        )

        if (
                not self._preview
                or self._preview_context_key != current_context_key
                or self._preview_settings_key != settings_key
        ):
            self.preview_shuffle(
                settings=shuffle_settings
            )

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

        current_track = current.get("item", {})

        return {
            "queued_count": queued_count,
            "playlist_name": playlist["name"],
            "queue_limit": limit,
            "current_song_name": current_track.get("name", "Unknown Song"),
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

    def create_cleaned_playlist(self):
        """
        Creates a safe cleaned copy of the current playlist.
        The original playlist is not modified.
        """

        current = self.current_playback()

        playlist, tracks = self.current_playlist(
            current
        )

        if playlist is None:
            raise RuntimeError(
                "No Spotify playlist is currently playing."
            )

        return create_cleaned_playlist_service(
            self.sp,
            playlist,
            tracks
        )

    def previous_song(self):
        """
        Skips to the previous Spotify track.
        """

        previous_song_service(
            self.sp
        )

    def next_song(self):
        """
        Skips to the next Spotify track.
        """

        next_song_service(
            self.sp
        )

    def toggle_playback(self):
        """
        Toggles Spotify playback between play and pause.
        """

        return toggle_playback_service(
            self.sp
        )

    def get_user_queue(self, limit=50):
        """
        Returns the user's current Spotify queue.
        """

        return get_user_queue_service(
            self.sp,
            limit=limit
        )

    def refresh_playlist(self):

        self._playlist = None
        self._tracks = None
        self._clear_shuffle_cache()