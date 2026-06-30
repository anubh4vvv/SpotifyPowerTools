from models.rule_result import RuleResult

from settings.shuffle_config import (
    ARTIST_BONUS,
    ARTIST_PENALTY,
    ARTIST_WEIGHT,
)


def artist_score(candidate, context):
    """
    Scores a song based on recent artist history.
    """

    recent = context.recent_songs[-context.artist_spacing:]

    for song in recent:
        if song.artist == candidate.artist:
            return RuleResult(
                score=ARTIST_PENALTY,
                reason=f"Artist '{candidate.artist}' appeared recently",
                weight=ARTIST_WEIGHT,
            )

    return RuleResult(
        score=ARTIST_BONUS,
        reason="Fresh artist",
        weight=ARTIST_WEIGHT,
    )