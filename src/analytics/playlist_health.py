def unique_artists(songs):
    return len({song.artist for song in songs})


def unique_albums(songs):
    return len({song.album for song in songs})


def total_duration(songs):
    return sum(song.duration_ms for song in songs)


def explicit_song_count(songs):
    return sum(song.explicit for song in songs)

def playlist_health_report(songs):
    return {
        "songs": len(songs),
        "artists": unique_artists(songs),
        "albums": unique_albums(songs),
        "duration_ms": total_duration(songs),
    }