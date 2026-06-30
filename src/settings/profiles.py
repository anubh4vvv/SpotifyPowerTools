from models.shuffle_profile import ShuffleProfile


BALANCED = ShuffleProfile(
    artist_weight=2.0,
    album_weight=1.0,
    random_weight=1.0,
    artist_spacing=5,
    album_spacing=3,
)

DISCOVERY = ShuffleProfile(
    artist_weight=3.0,
    album_weight=1.5,
    random_weight=0.5,
    artist_spacing=8,
    album_spacing=4,
)

ALBUM = ShuffleProfile(
    artist_weight=0.5,
    album_weight=4.0,
    random_weight=0.5,
    artist_spacing=2,
    album_spacing=10,
)

RANDOM = ShuffleProfile(
    artist_weight=1.0,
    album_weight=1.0,
    random_weight=3.0,
    artist_spacing=2,
    album_spacing=2,
)