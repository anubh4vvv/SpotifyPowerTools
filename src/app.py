from src.services.spotify_api import get_spotify_client, add_to_queue
from src.services.playback import print_current_song
from src.services.playlist import get_current_playlist, get_playlist_tracks
from song_position import get_current_track_index
from src.shuffle.reshuffler import smart_shuffle


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


if __name__ == "__main__":
    main()