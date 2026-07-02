def diagnose_playlist(analytics):
    """
    Turns playlist analytics into strengths, warnings, and suggestions.
    """

    strengths = []
    warnings = []
    suggestions = []

    total_songs = analytics["total_songs"]

    if total_songs == 0:
        return {
            "summary": "No playlist data available.",
            "strengths": [],
            "warnings": [
                "Start playing a Spotify playlist to analyze it."
            ],
            "suggestions": [
                "Open a playlist in Spotify and refresh the app."
            ],
        }

    health_score = analytics["health_score"]
    duplicate_count = analytics["duplicate_count"]
    diversity_score = analytics["diversity_score"]
    top_artist_percentage = analytics["top_artist_percentage"]
    top_album_percentage = analytics["top_album_percentage"]
    explicit_percentage = analytics["explicit_percentage"]

    # ---------- Health Summary ----------

    if health_score >= 85:
        summary = "This playlist is in excellent shape."
    elif health_score >= 70:
        summary = "This playlist is healthy, with a few areas to improve."
    elif health_score >= 50:
        summary = "This playlist is decent, but it could be improved."
    else:
        summary = "This playlist needs cleanup and better balance."

    # ---------- Strengths ----------

    if duplicate_count == 0:
        strengths.append(
            "No duplicate tracks found."
        )

    if diversity_score >= 45:
        strengths.append(
            "Good artist diversity."
        )

    if top_artist_percentage <= 20:
        strengths.append(
            "No single artist dominates the playlist."
        )

    if top_album_percentage <= 15:
        strengths.append(
            "Good album variety."
        )

    if 10 <= explicit_percentage <= 60:
        strengths.append(
            "Balanced mix of clean and explicit songs."
        )

    if analytics["unique_artists"] >= 20:
        strengths.append(
            "Playlist includes a wide range of artists."
        )

    if not strengths:
        strengths.append(
            "The playlist has enough data for deeper analysis."
        )

    # ---------- Warnings ----------

    if duplicate_count > 0:
        warnings.append(
            f"{duplicate_count} duplicate extra copies found."
        )

    if top_artist_percentage > 25:
        warnings.append(
            f"Top artist represents {top_artist_percentage}% of the playlist."
        )

    if top_album_percentage > 20:
        warnings.append(
            f"Top album represents {top_album_percentage}% of the playlist."
        )

    if diversity_score < 35:
        warnings.append(
            f"Artist diversity is low at {diversity_score}%."
        )

    if total_songs < 30:
        warnings.append(
            "Playlist is quite small, so shuffle variety may feel limited."
        )

    if analytics["release_years"]:

        top_year, top_year_count = analytics["release_years"][0]

        top_year_percentage = round(
            (top_year_count / total_songs) * 100,
            1
        )

        if top_year_percentage > 35:
            warnings.append(
                f"Many songs are concentrated around {top_year}."
            )

    if not warnings:
        warnings.append(
            "No major playlist issues detected."
        )

    # ---------- Suggestions ----------

    if duplicate_count > 0:
        suggestions.append(
            "Use Duplicate Finder to create a cleaned copy."
        )

    if top_artist_percentage > 25:
        suggestions.append(
            "Use Discovery mode or add more artists to reduce artist dominance."
        )

    if top_album_percentage > 20:
        suggestions.append(
            "Add songs from more albums for better variety."
        )

    if diversity_score < 35:
        suggestions.append(
            "Add more unique artists to improve playlist diversity."
        )

    if total_songs < 30:
        suggestions.append(
            "Add more songs before relying heavily on Smart Shuffle."
        )

    if health_score < 70:
        suggestions.append(
            "Review duplicates, artist dominance, and album dominance first."
        )

    if not suggestions:
        suggestions.append(
            "This playlist is ready for Smart Shuffle."
        )

    return {
        "summary": summary,
        "strengths": strengths,
        "warnings": warnings,
        "suggestions": suggestions,
    }