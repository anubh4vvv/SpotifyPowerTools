from spotify_api import get_spotify_client
from playback import print_current_song
from playlist import get_current_playlist


def main():
    sp = get_spotify_client()

    current = sp.current_playback()

    print_current_song(current)

    playlist = get_current_playlist(sp, current)

    if playlist is None:
        print("No playlist is currently playing.")
        return

    print("\n=== Playlist ===")
    print(playlist["name"])


if __name__ == "__main__":
    main()