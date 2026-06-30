from models.rule_result import RuleResult

from settings.shuffle_config import (
    ALBUM_BONUS,
    ALBUM_PENALTY,
    ALBUM_WEIGHT,
)


def album_score(candidate, context):
    """
    Scores a song based on recent album history.
    """

    recent = context.recent_songs[-context.album_spacing:]

    for song in recent:
        if song.album == candidate.album:
            return RuleResult(
                score=ALBUM_PENALTY,
                reason=f"Album '{candidate.album}' appeared recently",
                weight=ALBUM_WEIGHT,
            )

    return RuleResult(
        score=ALBUM_BONUS,
        reason="Fresh album",
        weight=ALBUM_WEIGHT,
    )