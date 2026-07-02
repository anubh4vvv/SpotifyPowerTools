from models.rule_result import RuleResult


def history_score(candidate, context, settings=None):
    """
    Penalizes songs that were played recently.

    Most recent songs receive the strongest penalty.
    Older history receives a smaller penalty.
    """

    if settings is None:
        settings = {}

    weight = settings.get(
        "history_weight",
        0
    )

    recent_track_keys = settings.get(
        "recent_track_keys",
        []
    )

    candidate_keys = [
        candidate.id,
        candidate.uri,
    ]

    candidate_keys = [
        key
        for key in candidate_keys
        if key
    ]

    recent_index = None

    for key in candidate_keys:

        if key in recent_track_keys:

            recent_index = recent_track_keys.index(
                key
            )

            break

    if recent_index is None:

        return RuleResult(
            score=10,
            reason="Not recently played",
            weight=weight,
        )

    if recent_index < 5:
        score = -140
        reason = "Played very recently"
    elif recent_index < 15:
        score = -80
        reason = "Played recently"
    else:
        score = -35
        reason = "Played in recent history"

    return RuleResult(
        score=score,
        reason=reason,
        weight=weight,
    )