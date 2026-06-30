from engine.rule_engine import RuleEngine

from settings.shuffle_config import (
    RANDOM_MIN,
    RANDOM_MAX,
    RANDOM_WEIGHT,
)

engine = RuleEngine()


def score_song(candidate, context, rng):
    """
    Returns:
        total_score
        reasons
    """

    results = engine.evaluate(
        candidate,
        context,
        rng
    )

    random_points = rng.randint(
        RANDOM_MIN,
        RANDOM_MAX
    )

    total_score = random_points * RANDOM_WEIGHT

    reasons = [
        f"{random_points:+} × {RANDOM_WEIGHT} = {total_score:+.1f} Random factor"
    ]

    for result in results:

        weighted_score = result.score * result.weight

        total_score += weighted_score

        reasons.append(
            f"{result.score:+} × {result.weight} = {weighted_score:+.1f} {result.reason}"
        )

    return total_score, reasons