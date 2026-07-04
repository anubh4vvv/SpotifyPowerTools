from datetime import datetime, timezone
from pathlib import Path

from services.rating_service import (
    load_ratings,
    get_song_rating_from_cache,
)

from services.listening_history_service import (
    get_listening_memory_map,
    calculate_track_rates,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def get_memory_for_song(song, memory_map):

    possible_keys = [
        song.id,
        song.uri,
    ]

    for key in possible_keys:

        if not key:
            continue

        if key in memory_map:
            return memory_map[key]

    return {}


def recommend_shuffle_profile(analytics):

    total_songs = analytics.get(
        "total_songs",
        0
    )

    if total_songs == 0:
        return {
            "profile": "Balanced",
            "confidence": "Low",
            "reason": "No playlist data available yet.",
            "reasons": [
                "Start playing a playlist first."
            ],
        }

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    total_known_songs = listening.get(
        "total_known_songs",
        0
    )

    global_skip_rate = listening.get(
        "global_skip_rate",
        0
    )

    global_completion_rate = listening.get(
        "global_completion_rate",
        0
    )

    rated_percentage = analytics.get(
        "rated_percentage",
        0
    )

    average_rating = analytics.get(
        "average_rating",
        0
    )

    diversity_score = analytics.get(
        "diversity_score",
        0
    )

    artist_entropy_score = analytics.get(
        "artist_entropy_score",
        0
    )

    health_score = analytics.get(
        "health_score",
        0
    )

    reasons = []

    if total_known_songs >= 10 and global_skip_rate >= 25:

        profile = "Adaptive"

        reasons.append(
            f"Skip rate is {global_skip_rate}%, so Adaptive can push frequently skipped songs down."
        )

        reasons.append(
            f"The app has listening memory for {total_known_songs} songs."
        )

    elif rated_percentage >= 40 and average_rating >= 3.8:

        profile = "Weighted"

        reasons.append(
            f"{rated_percentage}% of the playlist is rated."
        )

        reasons.append(
            f"Average rating is strong at {average_rating}/5."
        )

    elif diversity_score < 35 or artist_entropy_score < 55:

        profile = "Discovery"

        reasons.append(
            "Playlist variety is low, so Discovery can reduce repetition."
        )

        reasons.append(
            f"Artist entropy is {artist_entropy_score}%."
        )

    elif total_known_songs >= 10 and global_completion_rate >= 65:

        profile = "Adaptive"

        reasons.append(
            f"Completion rate is {global_completion_rate}%, so listening memory is useful."
        )

        reasons.append(
            "Adaptive can balance favorites with anti-repeat behavior."
        )

    elif health_score >= 80:

        profile = "Balanced"

        reasons.append(
            "Playlist health is strong, so Balanced is a safe default."
        )

    else:

        profile = "Balanced"

        reasons.append(
            "Balanced is recommended until more ratings or listening memory are available."
        )

    if total_known_songs >= 20 or rated_percentage >= 50:
        confidence = "High"
    elif total_known_songs >= 8 or rated_percentage >= 25:
        confidence = "Medium"
    else:
        confidence = "Low"

    return {
        "profile": profile,
        "confidence": confidence,
        "reason": " ".join(reasons),
        "reasons": reasons,
    }


def get_cleanup_suggestions(tracks, limit=8):

    ratings = load_ratings()
    memory_map = get_listening_memory_map()

    suggestions = []

    for song in tracks or []:

        rating = get_song_rating_from_cache(
            song,
            ratings
        )

        memory = get_memory_for_song(
            song,
            memory_map
        )

        play_count = int(
            memory.get("play_count", 0)
        )

        skip_count = int(
            memory.get("skip_count", 0)
        )

        finish_count = int(
            memory.get("finish_count", 0)
        )

        last_event = memory.get(
            "last_event",
            ""
        )

        rates = calculate_track_rates(
            memory
        )

        skip_rate = round(
            rates["skip_rate"] * 100,
            1
        )

        completion_rate = round(
            rates["completion_rate"] * 100,
            1
        )

        score = 0
        reasons = []

        if rating in [1, 2]:
            score += 80
            reasons.append(
                f"Rated {rating}/5"
            )

        if play_count >= 2 and skip_rate >= 60:
            score += 70
            reasons.append(
                f"{skip_rate}% skip rate"
            )

        elif play_count >= 2 and skip_rate >= 35:
            score += 40
            reasons.append(
                f"{skip_rate}% skip rate"
            )

        if skip_count >= 3:
            score += 45
            reasons.append(
                f"Skipped {skip_count} times"
            )

        if play_count >= 2 and completion_rate <= 25:
            score += 25
            reasons.append(
                f"Only {completion_rate}% completion"
            )

        if last_event == "skipped":
            score += 20
            reasons.append(
                "Recently skipped"
            )

        if score <= 0:
            continue

        suggestions.append({
            "name": song.name,
            "artist": song.artist,
            "album": song.album,
            "rating": rating,
            "play_count": play_count,
            "skip_count": skip_count,
            "finish_count": finish_count,
            "skip_rate": skip_rate,
            "completion_rate": completion_rate,
            "score": score,
            "reason": " • ".join(reasons),
        })

    suggestions.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return suggestions[:limit]


def get_hidden_favorites(tracks, limit=8):

    ratings = load_ratings()
    memory_map = get_listening_memory_map()

    favorites = []

    for song in tracks or []:

        rating = get_song_rating_from_cache(
            song,
            ratings
        )

        if rating > 0:
            continue

        memory = get_memory_for_song(
            song,
            memory_map
        )

        play_count = int(
            memory.get("play_count", 0)
        )

        finish_count = int(
            memory.get("finish_count", 0)
        )

        replay_count = int(
            memory.get("replay_count", 0)
        )

        skip_count = int(
            memory.get("skip_count", 0)
        )

        rates = calculate_track_rates(
            memory
        )

        skip_rate = round(
            rates["skip_rate"] * 100,
            1
        )

        completion_rate = round(
            rates["completion_rate"] * 100,
            1
        )

        score = 0
        reasons = []

        if replay_count > 0:
            score += replay_count * 35
            reasons.append(
                f"Replayed {replay_count} times"
            )

        if finish_count >= 2:
            score += finish_count * 18
            reasons.append(
                f"Finished {finish_count} times"
            )

        if play_count >= 2 and completion_rate >= 70:
            score += 35
            reasons.append(
                f"{completion_rate}% completion"
            )

        if play_count >= 2 and skip_rate <= 15:
            score += 20
            reasons.append(
                f"Only {skip_rate}% skip rate"
            )

        if skip_count > 0 and skip_rate >= 35:
            score -= 35

        if score <= 25:
            continue

        favorites.append({
            "name": song.name,
            "artist": song.artist,
            "album": song.album,
            "play_count": play_count,
            "finish_count": finish_count,
            "replay_count": replay_count,
            "skip_count": skip_count,
            "skip_rate": skip_rate,
            "completion_rate": completion_rate,
            "score": score,
            "reason": " • ".join(reasons),
        })

    favorites.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return favorites[:limit]


def calculate_playlist_intelligence(tracks, analytics):

    recommendation = recommend_shuffle_profile(
        analytics
    )

    cleanup_suggestions = get_cleanup_suggestions(
        tracks
    )

    hidden_favorites = get_hidden_favorites(
        tracks
    )

    return {
        "recommended_profile": recommendation["profile"],
        "recommendation_confidence": recommendation["confidence"],
        "recommendation_reason": recommendation["reason"],
        "recommendation_reasons": recommendation["reasons"],
        "cleanup_suggestions": cleanup_suggestions,
        "hidden_favorites": hidden_favorites,
    }


def format_report_items(title, items):

    lines = [
        "",
        title,
        "-" * len(title),
    ]

    if not items:
        lines.append(
            "No items found."
        )
        return lines

    for index, item in enumerate(
        items,
        start=1
    ):

        lines.append(
            f"{index}. {item['name']} — {item['artist']}"
        )

        reason = item.get(
            "reason",
            ""
        )

        if reason:
            lines.append(
                f"   {reason}"
            )

    return lines


def export_playlist_report(playlist, analytics):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    report_file = DATA_DIR / f"playlist_report_{timestamp}.txt"

    intelligence = analytics.get(
        "playlist_intelligence",
        {}
    )

    playlist_name = "Unknown Playlist"

    if playlist is not None:
        playlist_name = playlist.get(
            "name",
            "Unknown Playlist"
        )

    lines = []

    lines.append("Spotify Power Tools Playlist Report")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"Playlist: {playlist_name}")
    lines.append(f"Generated: {timestamp} UTC")

    lines.append("")
    lines.append("Health Summary")
    lines.append("-" * 14)
    lines.append(f"Health Score: {analytics.get('health_score', 0)}%")
    lines.append(f"Status: {analytics.get('health_status', 'N/A')}")
    lines.append(f"Songs: {analytics.get('total_songs', 0)}")
    lines.append(f"Unique Artists: {analytics.get('unique_artists', 0)}")
    lines.append(f"Unique Albums: {analytics.get('unique_albums', 0)}")
    lines.append(f"Diversity: {analytics.get('diversity_score', 0)}%")
    lines.append(f"Duplicates: {analytics.get('duplicate_count', 0)}")

    lines.append("")
    lines.append("Recommended Shuffle Profile")
    lines.append("-" * 29)
    lines.append(
        f"Profile: {intelligence.get('recommended_profile', 'Balanced')}"
    )
    lines.append(
        f"Confidence: {intelligence.get('recommendation_confidence', 'Low')}"
    )
    lines.append(
        f"Reason: {intelligence.get('recommendation_reason', '')}"
    )

    lines.append("")
    lines.append("Rating Summary")
    lines.append("-" * 14)
    lines.append(f"Average Rating: {analytics.get('average_rating', 0)}/5")
    lines.append(f"Rated Songs: {analytics.get('rated_songs', 0)}")
    lines.append(f"Unrated Songs: {analytics.get('unrated_songs', 0)}")
    lines.append(f"5-Star Songs: {analytics.get('five_star_songs', 0)}")
    lines.append(f"Low-Rated Songs: {analytics.get('low_rated_songs', 0)}")

    listening = analytics.get(
        "listening_analytics",
        {}
    )

    lines.append("")
    lines.append("Listening Memory Summary")
    lines.append("-" * 24)
    lines.append(f"Remembered Songs: {listening.get('total_known_songs', 0)}")
    lines.append(f"Total Plays: {listening.get('total_plays', 0)}")
    lines.append(f"Total Replays: {listening.get('total_replays', 0)}")
    lines.append(f"Global Skip Rate: {listening.get('global_skip_rate', 0)}%")
    lines.append(
        f"Global Completion Rate: {listening.get('global_completion_rate', 0)}%"
    )

    lines.extend(
        format_report_items(
            "Skip-aware Cleanup Suggestions",
            intelligence.get("cleanup_suggestions", [])
        )
    )

    lines.extend(
        format_report_items(
            "Hidden Favorites",
            intelligence.get("hidden_favorites", [])
        )
    )

    lines.append("")
    lines.append("Top Artists")
    lines.append("-" * 11)

    for index, item in enumerate(
        analytics.get("top_artists", []),
        start=1
    ):
        name, count = item
        lines.append(
            f"{index}. {name} — {count} songs"
        )

    lines.append("")
    lines.append("Top Albums")
    lines.append("-" * 10)

    for index, item in enumerate(
        analytics.get("top_albums", []),
        start=1
    ):
        name, count = item
        lines.append(
            f"{index}. {name} — {count} songs"
        )

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(
            "\n".join(lines)
        )

    return str(
        report_file
    )