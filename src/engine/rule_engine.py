from rules.artist_rule import artist_score
from rules.album_rule import album_score


class RuleEngine:

    def evaluate(self, candidate, context, rng):

        results = []

        results.append(
            artist_score(candidate, context)
        )

        results.append(
            album_score(candidate, context)
        )

        return results