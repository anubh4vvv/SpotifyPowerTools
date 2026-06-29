from rules.artist_rule import score as artist_score
from rules.album_rule import score as album_score
from rules.random_rule import score as random_score


def score_song(candidate, previous_song, rng):
    score = 0

    score += random_score(rng)
    score += artist_score(candidate, previous_song)
    score += album_score(candidate, previous_song)

    return score