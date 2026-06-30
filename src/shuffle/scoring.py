from engine.rule_engine import RuleEngine

from settings.shuffle_config import (
    RANDOM_MIN,
    RANDOM_MAX,
)

from shuffle.profile_config import resolve_shuffle_settings


engine = RuleEngine()


def score_song(candidate, context, rng, settings=None):
    """
    Returns:
        total_score
        reasons
    """

    resolved_settings = resolve_shuffle_settings(
        settings
    )

    results = engine.evaluate(
        candidate,
        context,
        rng,
        resolved_settings
    )

    random_points = rng.randint(
        RANDOM_MIN,
        RANDOM_MAX
    )

    random_weight = resolved_settings["random_weight"]

    total_score = random_points * random_weight

    reasons = [
        f"{random_points:+} × {random_weight} = {total_score:+.1f} Random factor"
    ]

    for result in results:

        weighted_score = result.score * result.weight

        total_score += weighted_score

        reasons.append(
            f"{result.score:+} × {result.weight} = {weighted_score:+.1f} {result.reason}"
        )

    return total_score, reasons