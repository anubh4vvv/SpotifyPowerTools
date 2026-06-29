from spotify_api import get_spotify_client
from playback import print_current_song


def main():
    sp = get_spotify_client()

    current = sp.current_playback()

    print_current_song(current)


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()