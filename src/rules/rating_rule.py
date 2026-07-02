from models.rule_result import RuleResult


def rating_score(candidate, context, settings=None):
    """
    Scores a song based on the user's saved local rating.

    Stronger behavior:
    5 stars -> very strong boost
    4 stars -> strong boost
    3 stars -> small boost
    2 stars -> penalty
    1 star  -> strong penalty
    unrated -> neutral
    """

    if settings is None:
        settings = {}

    weight = settings.get(
        "rating_weight",
        0
    )

    ratings = settings.get(
        "ratings",
        {}
    )

    song_rating_data = {}

    if candidate.id in ratings:
        song_rating_data = ratings[candidate.id]

    elif candidate.uri in ratings:
        song_rating_data = ratings[candidate.uri]

    rating = int(
        song_rating_data.get("rating", 0)
    )

    if rating == 0:
        return RuleResult(
            score=0,
            reason="Unrated song",
            weight=weight,
        )

    score_map = {
        1: -100,
        2: -45,
        3: 20,
        4: 75,
        5: 140,
    }

    score = score_map.get(
        rating,
        0
    )

    return RuleResult(
        score=score,
        reason=f"{rating}/5 rated song",
        weight=weight,
    )