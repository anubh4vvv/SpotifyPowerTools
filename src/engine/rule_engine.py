from rules.artist_rule import artist_score
from rules.album_rule import album_score
from rules.rating_rule import rating_score
from rules.history_rule import history_score


class RuleEngine:

    def evaluate(self, candidate, context, rng, settings=None):

        results = []

        results.append(
            artist_score(
                candidate,
                context,
                settings
            )
        )

        results.append(
            album_score(
                candidate,
                context,
                settings
            )
        )

        results.append(
            rating_score(
                candidate,
                context,
                settings
            )
        )

        results.append(
            history_score(
                candidate,
                context,
                settings
            )
        )

        return results