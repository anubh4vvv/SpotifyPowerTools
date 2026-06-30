from models.rule_result import RuleResult

from settings.shuffle_config import (
    ARTIST_BONUS,
    ARTIST_PENALTY,
    ARTIST_WEIGHT,
)


def artist_score(candidate, context, settings=None):
    """
    Scores a song based on recent artist history.
    """

    weight = ARTIST_WEIGHT

    if settings is not None:
        weight = settings.get(
            "artist_weight",
            ARTIST_WEIGHT
        )

    recent = context.recent_songs[-context.artist_spacing:]

    for song in recent:
        if song.artist == candidate.artist:
            return RuleResult(
                score=ARTIST_PENALTY,
                reason=f"Artist '{candidate.artist}' appeared recently",
                weight=weight,
            )

    return RuleResult(
        score=ARTIST_BONUS,
        reason="Fresh artist",
        weight=weight,
    )