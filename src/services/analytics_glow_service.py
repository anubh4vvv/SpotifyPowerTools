def clamp(value, minimum=0, maximum=100):

    return max(
        minimum,
        min(maximum, value)
    )


def first_item(items, default=None):

    if not items:
        return default

    return items[0]


def make_wrapped_card(title, value, subtitle, emoji):

    return {
        "title": title,
        "value": value,
        "subtitle": subtitle,
        "emoji": emoji,
    }


def calculate_variety_score(analytics):

    diversity_score = analytics.get(
        "diversity_score",
        0
    )

    artist_entropy_score = analytics.get(
        "artist_entropy_score",
        0
    )

    album_entropy_score = analytics.get(
        "album_entropy_score",
        0
    )

    return round(
        (
            diversity_score * 0.45
            + artist_entropy_score * 0.35
            + album_entropy_score * 0.20
        ),
        1
    )


def calculate_replay_energy(listening):

    total_plays = listening.get(
        "total_plays",
        0
    )

    total_replays = listening.get(
        "total_replays",
        0
    )

    most_replayed = listening.get(
        "most_replayed",
        []
    )

    if total_plays <= 0:
        return 0

    replay_rate = (
        total_replays / total_plays
    ) * 100

    bonus = 0

    if most_replayed:
        bonus = min(
            most_replayed[0].get("replay_count", 0) * 12,
            35
        )

    return round(
        clamp(
            replay_rate * 3 + bonus
        ),
        1
    )


def calculate_taste_match(analytics):

    average_rating = analytics.get(
        "average_rating",
        0
    )

    rated_percentage = analytics.get(
        "rated_percentage",
        0
    )

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    completion_rate = listening.get(
        "global_completion_rate",
        0
    )

    skip_rate = listening.get(
        "global_skip_rate",
        0
    )

    if average_rating <= 0:

        score = (
            completion_rate * 0.65
            + max(0, 100 - skip_rate) * 0.35
        )

    else:

        rating_score = (
            average_rating / 5
        ) * 100

        score = (
            rating_score * 0.55
            + completion_rate * 0.25
            + max(0, 100 - skip_rate) * 0.15
            + min(rated_percentage, 100) * 0.05
        )

    return round(
        clamp(score),
        1
    )


def calculate_aura_score(analytics):

    health_score = analytics.get(
        "health_score",
        0
    )

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    skip_rate = listening.get(
        "global_skip_rate",
        0
    )

    variety_score = calculate_variety_score(
        analytics
    )

    taste_match = calculate_taste_match(
        analytics
    )

    score = (
        health_score * 0.35
        + variety_score * 0.25
        + taste_match * 0.25
        + max(0, 100 - skip_rate) * 0.15
    )

    return round(
        clamp(score),
        1
    )


def get_personality(analytics, aura_score, variety_score, replay_energy, taste_match):

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    skip_rate = listening.get(
        "global_skip_rate",
        0
    )

    completion_rate = listening.get(
        "global_completion_rate",
        0
    )

    top_artist_percentage = analytics.get(
        "top_artist_percentage",
        0
    )

    explicit_percentage = analytics.get(
        "explicit_percentage",
        0
    )

    rated_percentage = analytics.get(
        "rated_percentage",
        0
    )

    if skip_rate >= 35:

        return {
            "title": "Chaos Shuffle Energy",
            "emoji": "🌪️",
            "subtitle": "You know exactly what you do not want to hear.",
        }

    if replay_energy >= 60:

        return {
            "title": "Replay Addict",
            "emoji": "🔁",
            "subtitle": "When a song hits, you run it back like a ritual.",
        }

    if variety_score >= 75:

        return {
            "title": "Discovery Explorer",
            "emoji": "🧭",
            "subtitle": "Your playlist jumps across artists, albums, and moods.",
        }

    if top_artist_percentage >= 30:

        return {
            "title": "Artist Loyalist",
            "emoji": "👑",
            "subtitle": "One artist is carrying the emotional weight here.",
        }

    if explicit_percentage >= 60:

        return {
            "title": "After Hours Main Character",
            "emoji": "🌙",
            "subtitle": "This playlist has late-night, headphones-on energy.",
        }

    if aura_score >= 85 and completion_rate >= 70:

        return {
            "title": "Golden Hour Curator",
            "emoji": "🌅",
            "subtitle": "Balanced, replayable, and surprisingly well tuned.",
        }

    if rated_percentage >= 50 and taste_match >= 75:

        return {
            "title": "Taste Architect",
            "emoji": "🏛️",
            "subtitle": "Your ratings and listening behavior are very aligned.",
        }

    return {
        "title": "Main Character Mix",
        "emoji": "✨",
        "subtitle": "Balanced vibes with enough personality to keep it moving.",
    }


def get_badges(analytics, aura_score, variety_score, replay_energy, taste_match):

    badges = []

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    intelligence = analytics.get(
        "playlist_intelligence",
        {}
    )

    skip_rate = listening.get(
        "global_skip_rate",
        0
    )

    completion_rate = listening.get(
        "global_completion_rate",
        0
    )

    explicit_percentage = analytics.get(
        "explicit_percentage",
        0
    )

    top_artist_percentage = analytics.get(
        "top_artist_percentage",
        0
    )

    rated_percentage = analytics.get(
        "rated_percentage",
        0
    )

    cleanup_suggestions = intelligence.get(
        "cleanup_suggestions",
        []
    )

    hidden_favorites = intelligence.get(
        "hidden_favorites",
        []
    )

    if aura_score >= 85:
        badges.append({
            "emoji": "🌟",
            "title": "Golden Aura",
            "description": "Elite playlist health",
        })

    if variety_score >= 70:
        badges.append({
            "emoji": "🌈",
            "title": "Diversity King",
            "description": "Strong variety",
        })

    if replay_energy >= 50:
        badges.append({
            "emoji": "🔁",
            "title": "Replay Heavy",
            "description": "Songs worth repeating",
        })

    if skip_rate >= 35:
        badges.append({
            "emoji": "⚡",
            "title": "Skip Storm",
            "description": "Strong opinions detected",
        })

    if completion_rate >= 70:
        badges.append({
            "emoji": "🎧",
            "title": "No-Skip Zone",
            "description": "High completion rate",
        })

    if hidden_favorites:
        badges.append({
            "emoji": "💎",
            "title": "Hidden Gems",
            "description": "Unrated favorites found",
        })

    if cleanup_suggestions:
        badges.append({
            "emoji": "🧹",
            "title": "Needs Cleanup",
            "description": "Some songs drag it down",
        })

    if top_artist_percentage >= 25:
        badges.append({
            "emoji": "👑",
            "title": "Artist Loyalist",
            "description": "Top artist dominance",
        })

    if explicit_percentage >= 50:
        badges.append({
            "emoji": "🔥",
            "title": "After Hours",
            "description": "Explicit-heavy energy",
        })

    if rated_percentage >= 50:
        badges.append({
            "emoji": "🧠",
            "title": "Taste Trained",
            "description": "Ratings are strong",
        })

    if taste_match >= 80:
        badges.append({
            "emoji": "💚",
            "title": "Taste Match",
            "description": "This playlist gets you",
        })

    if not badges:
        badges.append({
            "emoji": "✨",
            "title": "Fresh Start",
            "description": "More listening will unlock badges",
        })

    return badges[:8]


def get_wrapped_cards(analytics):

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    intelligence = analytics.get(
        "playlist_intelligence",
        {}
    )

    top_artist = first_item(
        analytics.get("top_artists", []),
        ("N/A", 0)
    )

    top_artist_name, top_artist_count = top_artist

    most_replayed = first_item(
        listening.get("most_replayed", []),
        {}
    )

    most_skipped = first_item(
        listening.get("most_skipped", []),
        {}
    )

    hidden_favorite = first_item(
        intelligence.get("hidden_favorites", []),
        {}
    )

    villain = first_item(
        intelligence.get("cleanup_suggestions", []),
        {}
    )

    playlist_mvp = first_item(
        analytics.get("top_rated_tracks", []),
        {}
    )

    if not playlist_mvp:
        playlist_mvp = hidden_favorite

    return {
        "top_artist": make_wrapped_card(
            "Top Artist",
            str(top_artist_name),
            f"{top_artist_count} songs in this playlist",
            "🎤"
        ),
        "most_replayed": make_wrapped_card(
            "Most Replayed",
            most_replayed.get("song_name", "Not enough memory yet"),
            most_replayed.get("artist", "Keep listening to unlock this"),
            "🔁"
        ),
        "most_skipped": make_wrapped_card(
            "Most Skipped",
            most_skipped.get("song_name", "No major skips yet"),
            most_skipped.get("artist", "Your playlist is behaving"),
            "⏭️"
        ),
        "hidden_favorite": make_wrapped_card(
            "Hidden Favorite",
            hidden_favorite.get("name", "No hidden favorite yet"),
            hidden_favorite.get("reason", "Unrated gems will appear here"),
            "💎"
        ),
        "playlist_villain": make_wrapped_card(
            "Playlist Villain",
            villain.get("name", "No villain detected"),
            villain.get("reason", "Nothing is obviously dragging this playlist down"),
            "😈"
        ),
        "playlist_mvp": make_wrapped_card(
            "Playlist MVP",
            playlist_mvp.get("name", "No MVP yet"),
            playlist_mvp.get("artist", "Rate songs to unlock this"),
            "🏆"
        ),
    }


def calculate_analytics_glow(analytics):

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    variety_score = calculate_variety_score(
        analytics
    )

    replay_energy = calculate_replay_energy(
        listening
    )

    taste_match = calculate_taste_match(
        analytics
    )

    aura_score = calculate_aura_score(
        analytics
    )

    personality = get_personality(
        analytics,
        aura_score,
        variety_score,
        replay_energy,
        taste_match
    )

    badges = get_badges(
        analytics,
        aura_score,
        variety_score,
        replay_energy,
        taste_match
    )

    wrapped_cards = get_wrapped_cards(
        analytics
    )

    return {
        "aura_score": aura_score,
        "taste_match": taste_match,
        "variety_score": variety_score,
        "replay_energy": replay_energy,
        "personality": personality,
        "badges": badges,
        "wrapped_cards": wrapped_cards,
    }