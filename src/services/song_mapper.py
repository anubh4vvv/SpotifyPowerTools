from models.song import Song


def playlist_item_to_song(item):

    track = item["item"]

    if track is None:
        return None

    images = track["album"].get("images", [])

    image_url = ""

    if images:
        image_url = images[0]["url"]

    release_year = ""

    if track["album"].get("release_date"):
        release_year = track["album"]["release_date"][:4]

    return Song(

        id=track["id"],

        uri=track["uri"],

        name=track["name"],

        artist=track["artists"][0]["name"],

        album=track["album"]["name"],

        duration_ms=track["duration_ms"],

        image_url=image_url,

        release_year=release_year,

        explicit=track.get("explicit", False),

        popularity=track.get("popularity", 0)

    )