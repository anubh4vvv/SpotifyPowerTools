def print_current_song(current):
    if current is None:
        print("Nothing is currently playing.")
        return

    song = current["item"]["name"]
    artist = current["item"]["artists"][0]["name"]
    album = current["item"]["album"]["name"]

    print(f"Song   : {song}")
    print(f"Artist : {artist}")
    print(f"Album  : {album}")

    context = current.get("context")

    if context:
        print(f"Type : {context['type']}")
        print(f"URI  : {context['uri']}")