from models.rule_result import RuleResult


def get_candidate_memory(candidate, listening_memory):

    possible_keys = [
        candidate.id,
        candidate.uri,
    ]

    for key in possible_keys:

        if not key:
            continue

        if key in listening_memory:
            return listening_memory[key]

    return {}


def get_recent_index(candidate, recent_track_keys):

    candidate_keys = [
        candidate.id,
        candidate.uri,
    ]

    candidate_keys = [
        key
        for key in candidate_keys
        if key
    ]

    for key in candidate_keys:

        if key in recent_track_keys:

            return recent_track_keys.index(
                key
            )

    return None


def safe_rate(part, total):

    if total <= 0:
        return 0

    return part / total


def history_score(candidate, context, settings=None):
    """
    Smart Anti-Repeat v3.

    Uses:
    - recent play position
    - skip rate
    - completion rate
    - replay count
    - last event
    - Adaptive profile mode
    """

    if settings is None:
        settings = {}

    weight = settings.get(
        "history_weight",
        0
    )

    adaptive_mode = bool(
        settings.get("adaptive_mode", False)
    )

    recent_track_keys = settings.get(
        "recent_track_keys",
        []
    )

    listening_memory = settings.get(
        "listening_memory",
        {}
    )

    memory = get_candidate_memory(
        candidate,
        listening_memory
    )

    recent_index = get_recent_index(
        candidate,
        recent_track_keys
    )

    score = 0
    reasons = []

    # ---------- Recent play penalty ----------

    if recent_index is None:

        if adaptive_mode:
            score += 22
        else:
            score += 12

        reasons.append(
            "Not recently played"
        )

    elif recent_index < 5:

        if adaptive_mode:
            score -= 190
        else:
            score -= 150

        reasons.append(
            "Played very recently"
        )

    elif recent_index < 15:

        if adaptive_mode:
            score -= 120
        else:
            score -= 90

        reasons.append(
            "Played recently"
        )

    else:

        if adaptive_mode:
            score -= 55
        else:
            score -= 40

        reasons.append(
            "Played in recent history"
        )

    # ---------- Memory-based behavior ----------

    play_count = int(
        memory.get("play_count", 0)
    )

    finish_count = int(
        memory.get("finish_count", 0)
    )

    skip_count = int(
        memory.get("skip_count", 0)
    )

    replay_count = int(
        memory.get("replay_count", 0)
    )

    last_event = memory.get(
        "last_event",
        ""
    )

    skip_rate = safe_rate(
        skip_count,
        play_count
    )

    completion_rate = safe_rate(
        finish_count,
        play_count
    )

    if play_count == 0:

        if adaptive_mode:
            score += 35
            reasons.append("Discovery boost")
        else:
            score += 15
            reasons.append("No listening memory")

    if last_event == "skipped":

        if adaptive_mode:
            score -= 120
        else:
            score -= 80

        reasons.append(
            "Recently skipped"
        )

    elif last_event == "finished":

        if adaptive_mode:
            score -= 35
        else:
            score -= 25

        reasons.append(
            "Recently finished"
        )

    elif last_event == "replayed":

        if adaptive_mode:
            score += 35
        else:
            score += 20

        reasons.append(
            "Recently replayed"
        )

    if play_count >= 3 and skip_rate >= 0.60:

        if adaptive_mode:
            score -= 150
        else:
            score -= 100

        reasons.append(
            "High skip percentage"
        )

    elif play_count >= 3 and skip_rate >= 0.35:

        if adaptive_mode:
            score -= 70
        else:
            score -= 45

        reasons.append(
            "Moderate skip percentage"
        )

    if play_count >= 3 and completion_rate >= 0.70 and skip_rate <= 0.20:

        if adaptive_mode:
            score += 40
        else:
            score += 20

        reasons.append(
            "Strong completion rate"
        )

    if replay_count >= 2 and skip_rate <= 0.25:

        if adaptive_mode:
            score += 50
        else:
            score += 25

        reasons.append(
            "Often replayed"
        )

    if (
        adaptive_mode
        and play_count >= 5
        and completion_rate >= 0.60
        and skip_rate <= 0.10
    ):

        score += 20

        reasons.append(
            "Reliable favorite"
        )

    if not reasons:

        reasons.append(
            "Neutral listening history"
        )

    reason_text = " • ".join(
        reasons[:4]
    )

    return RuleResult(
        score=score,
        reason=reason_text,
        weight=weight,
    )