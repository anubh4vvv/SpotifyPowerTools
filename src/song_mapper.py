from models import Song


def playlist_item_to_song(item):
    track = item["item"]

    return Song(
        id=track["id"],
        name=track["name"],
        artist=track["artists"][0]["name"],
        album=track["album"]["name"]
    )