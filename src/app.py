from spotify_api import get_spotify_client
from playback import print_current_song
from playlist import get_current_playlist, get_playlist_tracks
from song_position import get_current_track_index
from reshuffler import reshuffle_remaining

def main():
    sp = get_spotify_client()

    current = sp.current_playback()

    print_current_song(current)

    playlist = get_current_playlist(sp, current)
    if playlist is None:
        print("No playlist is currently playing.")
        return

    tracks = get_playlist_tracks(sp, playlist)
    index = get_current_track_index(current, tracks)

    print(f"\nCurrent position: {index + 1}/{len(tracks)}")

    print(f"\nPlaylist: {playlist['name']}")
    print(f"Tracks: {len(tracks)}")

    if playlist is None:
        print("No playlist is currently playing.")
        return

    print("\n=== Playlist ===")
    print(playlist["name"])

    new_tracks = reshuffle_remaining(
        tracks,
        index,
        seed=99
    )

    print("\nNext five songs after reshuffle:")

    for item in new_tracks[index + 1:index + 6]:
        print("-", item.name)


if __name__ == "__main__":
    main()