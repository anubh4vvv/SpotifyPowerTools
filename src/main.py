from services.spotify_api import get_spotify_client, add_to_queue
from services.playback import print_current_song
from services.playlist import get_current_playlist, get_playlist_tracks
from shuffle.reshuffler import smart_shuffle
from analytics.playlist_health import playlist_health_report
from services.song_position import get_current_track_index
import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

def main():
    # Connect to Spotify
    sp = get_spotify_client()

    # Get current playback
    current = sp.current_playback()

    if current is None:
        print("Nothing is currently playing.")
        return

    # Print current song
    print_current_song(current)

    # Get current playlist
    playlist = get_current_playlist(sp, current)

    if playlist is None:
        print("Current playback is not from a playlist.")
        return

    # Load every song in the playlist
    tracks = get_playlist_tracks(sp, playlist)

    # Find current song index
    index = get_current_track_index(current, tracks)

    if index == -1:
        print("Couldn't find the current song in the playlist.")
        return

    print("\n==============================")
    print(f"Playlist : {playlist['name']}")
    print(f"Songs    : {len(tracks)}")
    print(f"Current  : {index + 1}/{len(tracks)}")
    print("==============================")

    # Perform Smart Shuffle
    shuffled_tracks = smart_shuffle(
        tracks,
        index,
        seed=99
    )
    next_song = shuffled_tracks[index + 1]

    print(f"\nQueueing: {next_song.name}")

    add_to_queue(sp, next_song)

    print("\nNext 5 songs after Smart Shuffle:\n")

    for song in shuffled_tracks[index + 1:index + 6]:
        print(f"• {song.name} — {song.artist}")

    report = playlist_health_report(tracks)

    hours = report["duration_ms"] // 1000 // 3600
    minutes = (report["duration_ms"] // 1000 % 3600) // 60

    print("\n========== Playlist Health ==========")
    print(f"Songs           : {report['songs']}")
    print(f"Unique Artists  : {report['artists']}")
    print(f"Unique Albums   : {report['albums']}")
    print(f"Duration        : {hours}h {minutes}m")
    print("=====================================")


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())