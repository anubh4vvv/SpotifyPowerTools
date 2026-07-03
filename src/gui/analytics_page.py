from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.stat_tile import StatTile
from gui.bar_chart_card import BarChartCard
from gui.health_score_card import HealthScoreCard
from gui.playlist_doctor_card import PlaylistDoctorCard
from gui.rating_recommendations_card import RatingRecommendationsCard
from gui.visual_balance_card import VisualBalanceCard
from gui.dominance_breakdown_card import DominanceBreakdownCard

from services.playlist_doctor_service import (
    diagnose_playlist,
    get_rating_recommendations,
)

from services.analytics_service import calculate_playlist_analytics


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("Playlist Analytics")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "Understand the health, balance, structure, and rating intelligence of the playlist you are currently listening to."
        )
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ---------- Main Stats ----------

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        self.total_songs = StatTile("Songs")
        self.unique_artists = StatTile("Artists")
        self.unique_albums = StatTile("Albums")
        self.duration = StatTile("Duration")

        self.health_score = StatTile("Health")
        self.health_status = StatTile("Status")
        self.duplicates = StatTile("Duplicates")
        self.diversity = StatTile("Diversity")

        self.average_popularity = StatTile("Avg Popularity")
        self.average_song_length = StatTile("Avg Length")
        self.explicit_songs = StatTile("Explicit")
        self.clean_songs = StatTile("Clean")

        self.artist_entropy = StatTile("Artist Entropy")
        self.album_entropy = StatTile("Album Entropy")
        self.average_rating = StatTile("Avg Rating")
        self.rated_songs = StatTile("Rated")

        self.unrated_songs = StatTile("Unrated")
        self.five_star_songs = StatTile("5-Star")

        stats_grid.addWidget(self.total_songs, 0, 0)
        stats_grid.addWidget(self.unique_artists, 0, 1)
        stats_grid.addWidget(self.unique_albums, 0, 2)
        stats_grid.addWidget(self.duration, 0, 3)

        stats_grid.addWidget(self.health_score, 1, 0)
        stats_grid.addWidget(self.health_status, 1, 1)
        stats_grid.addWidget(self.duplicates, 1, 2)
        stats_grid.addWidget(self.diversity, 1, 3)

        stats_grid.addWidget(self.average_popularity, 2, 0)
        stats_grid.addWidget(self.average_song_length, 2, 1)
        stats_grid.addWidget(self.explicit_songs, 2, 2)
        stats_grid.addWidget(self.clean_songs, 2, 3)

        stats_grid.addWidget(self.artist_entropy, 3, 0)
        stats_grid.addWidget(self.album_entropy, 3, 1)
        stats_grid.addWidget(self.average_rating, 3, 2)
        stats_grid.addWidget(self.rated_songs, 3, 3)

        stats_grid.addWidget(self.unrated_songs, 4, 0)
        stats_grid.addWidget(self.five_star_songs, 4, 1)

        layout.addLayout(stats_grid)

        # ---------- Visual Summary Cards ----------

        visual_grid = QGridLayout()
        visual_grid.setSpacing(20)

        self.health_visual_card = HealthScoreCard()
        self.visual_balance_card = VisualBalanceCard()
        self.dominance_breakdown_card = DominanceBreakdownCard()

        visual_grid.addWidget(self.health_visual_card, 0, 0)
        visual_grid.addWidget(self.visual_balance_card, 0, 1)
        visual_grid.addWidget(self.dominance_breakdown_card, 1, 0, 1, 2)

        layout.addLayout(visual_grid)

        # ---------- Smart Recommendation Cards ----------

        self.playlist_doctor_card = PlaylistDoctorCard()

        layout.addWidget(
            self.playlist_doctor_card
        )

        self.rating_recommendations_card = RatingRecommendationsCard()

        layout.addWidget(
            self.rating_recommendations_card
        )

        # ---------- Chart Cards ----------

        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        self.top_artists_chart = BarChartCard("Top Artists")
        self.top_albums_chart = BarChartCard("Top Albums")
        self.release_years_chart = BarChartCard("Release Years")
        self.clean_explicit_chart = BarChartCard("Clean vs Explicit")
        self.rating_distribution_chart = BarChartCard("Rating Distribution")

        charts_grid.addWidget(self.top_artists_chart, 0, 0)
        charts_grid.addWidget(self.top_albums_chart, 0, 1)

        charts_grid.addWidget(self.release_years_chart, 1, 0)
        charts_grid.addWidget(self.clean_explicit_chart, 1, 1)

        charts_grid.addWidget(self.rating_distribution_chart, 2, 0, 1, 2)

        layout.addLayout(charts_grid)

        # ---------- Insight Cards ----------

        insight_grid = QGridLayout()
        insight_grid.setSpacing(20)

        self.duplicates_card = Card("Duplicate Tracks")
        self.age_card = Card("Oldest / Newest")
        self.rating_card = Card("Rating Insights")

        self.duplicates_label = self.make_text_label()
        self.age_label = self.make_text_label()
        self.rating_label = self.make_text_label()

        self.duplicates_card.layout.addWidget(
            self.duplicates_label
        )

        self.age_card.layout.addWidget(
            self.age_label
        )

        self.rating_card.layout.addWidget(
            self.rating_label
        )

        insight_grid.addWidget(self.duplicates_card, 0, 0)
        insight_grid.addWidget(self.age_card, 0, 1)
        insight_grid.addWidget(self.rating_card, 1, 0, 1, 2)

        layout.addLayout(insight_grid)
        layout.addStretch()

        scroll.setWidget(content)

        root_layout.addWidget(scroll)

    def make_text_label(self):

        label = QLabel("No data yet")
        label.setWordWrap(True)
        label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        return label

    def update_analytics(self, playlist, tracks):

        analytics = calculate_playlist_analytics(
            tracks
        )

        self.total_songs.set_value(
            analytics["total_songs"]
        )

        self.unique_artists.set_value(
            analytics["unique_artists"]
        )

        self.unique_albums.set_value(
            analytics["unique_albums"]
        )

        self.duration.set_value(
            analytics["total_duration"]
        )

        self.health_score.set_value(
            f"{analytics['health_score']}%"
        )

        self.health_status.set_value(
            analytics["health_status"]
        )

        self.duplicates.set_value(
            analytics["duplicate_count"]
        )

        self.diversity.set_value(
            f"{analytics['diversity_score']}%"
        )

        self.average_popularity.set_value(
            analytics["average_popularity"]
        )

        self.average_song_length.set_value(
            analytics["average_song_length"]
        )

        self.explicit_songs.set_value(
            f"{analytics['explicit_songs']} ({analytics['explicit_percentage']}%)"
        )

        self.clean_songs.set_value(
            analytics["clean_songs"]
        )

        self.artist_entropy.set_value(
            f"{analytics['artist_entropy_score']}%"
        )

        self.album_entropy.set_value(
            f"{analytics['album_entropy_score']}%"
        )

        self.average_rating.set_value(
            f"{analytics['average_rating']}/5"
        )

        self.rated_songs.set_value(
            f"{analytics['rated_songs']} ({analytics['rated_percentage']}%)"
        )

        self.unrated_songs.set_value(
            f"{analytics['unrated_songs']} ({analytics['unrated_percentage']}%)"
        )

        self.five_star_songs.set_value(
            analytics["five_star_songs"]
        )

        self.health_visual_card.update_health(
            analytics["health_score"],
            analytics["health_status"],
            analytics["duplicate_count"],
            analytics["diversity_score"]
        )

        self.visual_balance_card.update_balance(
            analytics
        )

        self.dominance_breakdown_card.update_dominance(
            analytics
        )

        diagnosis = diagnose_playlist(
            analytics
        )

        self.playlist_doctor_card.update_diagnosis(
            diagnosis
        )

        rating_recommendations = get_rating_recommendations(
            analytics
        )

        self.rating_recommendations_card.update_recommendations(
            rating_recommendations
        )

        self.top_artists_chart.set_data(
            analytics["top_artists"]
        )

        self.top_albums_chart.set_data(
            analytics["top_albums"]
        )

        self.release_years_chart.set_data(
            analytics["release_years"]
        )

        self.clean_explicit_chart.set_data([
            (
                "Clean",
                analytics["clean_songs"]
            ),
            (
                "Explicit",
                analytics["explicit_songs"]
            ),
        ])

        self.rating_distribution_chart.set_data(
            analytics["rating_distribution"]
        )

        self.duplicates_label.setText(
            self.format_duplicate_list(
                analytics["duplicate_tracks"]
            )
        )

        self.age_label.setText(
            self.format_age_info(
                analytics
            )
        )

        self.rating_label.setText(
            self.format_rating_info(
                analytics
            )
        )

    def format_duplicate_list(self, duplicates):

        if not duplicates:
            return "No duplicate tracks found."

        lines = []

        for index, item in enumerate(duplicates, start=1):
            name, duplicate_count = item

            lines.append(
                f"{index}. {name}  —  {duplicate_count} extra"
            )

        return "\n".join(lines)

    def format_age_info(self, analytics):

        return (
            f"Oldest:\n"
            f"{analytics['oldest_song']}\n"
            f"Year: {analytics['oldest_year']}\n\n"
            f"Newest:\n"
            f"{analytics['newest_song']}\n"
            f"Year: {analytics['newest_year']}"
        )

    def format_rating_info(self, analytics):

        lines = []

        lines.append(
            f"Average Rating: {analytics['average_rating']}/5"
        )

        lines.append(
            f"Rated Songs: {analytics['rated_songs']} "
            f"({analytics['rated_percentage']}%)"
        )

        lines.append(
            f"Unrated Songs: {analytics['unrated_songs']} "
            f"({analytics['unrated_percentage']}%)"
        )

        lines.append(
            f"5-Star Songs: {analytics['five_star_songs']}"
        )

        lines.append(
            f"Low-Rated Songs: {analytics['low_rated_songs']}"
        )

        lines.append("")
        lines.append("Top Rated:")

        top_tracks = analytics["top_rated_tracks"]

        if not top_tracks:
            lines.append(
                "No rated songs yet."
            )
        else:
            for index, item in enumerate(
                    top_tracks,
                    start=1
            ):
                lines.append(
                    f"{index}. {item['name']} - {item['artist']} "
                    f"({item['rating']}/5)"
                )

        lines.append("")
        lines.append("Low Rated:")

        low_tracks = analytics["low_rated_tracks"]

        if not low_tracks:
            lines.append(
                "No low-rated songs found."
            )
        else:
            for index, item in enumerate(
                    low_tracks,
                    start=1
            ):
                lines.append(
                    f"{index}. {item['name']} - {item['artist']} "
                    f"({item['rating']}/5)"
                )

        return "\n".join(
            lines
        )