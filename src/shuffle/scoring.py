import random

from rules.artist_rule import artist_score
from rules.album_rule import album_score


def score_song(candidate, previous_song, rng):
    score = 0

    score += artist_score(candidate, previous_song)
    score += album_score(candidate, previous_song)

    score += rng.randint(0, 100)

    return score