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
            "Understand the health, balance, and structure of the playlist you are currently listening to."
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

        layout.addLayout(stats_grid)

        # ---------- Chart Cards ----------

        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)

        self.top_artists_chart = BarChartCard("Top Artists")
        self.top_albums_chart = BarChartCard("Top Albums")
        self.release_years_chart = BarChartCard("Release Years")
        self.clean_explicit_chart = BarChartCard("Clean vs Explicit")

        charts_grid.addWidget(self.top_artists_chart, 0, 0)
        charts_grid.addWidget(self.top_albums_chart, 0, 1)

        charts_grid.addWidget(self.release_years_chart, 1, 0)
        charts_grid.addWidget(self.clean_explicit_chart, 1, 1)

        layout.addLayout(charts_grid)

        # ---------- Insight Cards ----------

        insight_grid = QGridLayout()
        insight_grid.setSpacing(20)

        self.duplicates_card = Card("Duplicate Tracks")
        self.dominance_card = Card("Dominance")
        self.age_card = Card("Oldest / Newest")

        self.duplicates_label = self.make_text_label()
        self.dominance_label = self.make_text_label()
        self.age_label = self.make_text_label()

        self.duplicates_card.layout.addWidget(
            self.duplicates_label
        )

        self.dominance_card.layout.addWidget(
            self.dominance_label
        )

        self.age_card.layout.addWidget(
            self.age_label
        )

        insight_grid.addWidget(self.duplicates_card, 0, 0)
        insight_grid.addWidget(self.dominance_card, 0, 1)
        insight_grid.addWidget(self.age_card, 0, 2)

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

        self.duplicates_label.setText(
            self.format_duplicate_list(
                analytics["duplicate_tracks"]
            )
        )

        self.dominance_label.setText(
            self.format_dominance(
                analytics
            )
        )

        self.age_label.setText(
            self.format_age_info(
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

    def format_dominance(self, analytics):

        return (
            f"Top Artist:\n"
            f"{analytics['top_artist_name']}\n"
            f"{analytics['top_artist_count']} songs "
            f"({analytics['top_artist_percentage']}%)\n\n"
            f"Top Album:\n"
            f"{analytics['top_album_name']}\n"
            f"{analytics['top_album_count']} songs "
            f"({analytics['top_album_percentage']}%)"
        )

    def format_age_info(self, analytics):

        return (
            f"Oldest:\n"
            f"{analytics['oldest_song']}\n"
            f"Year: {analytics['oldest_year']}\n\n"
            f"Newest:\n"
            f"{analytics['newest_song']}\n"
            f"Year: {analytics['newest_year']}"
        )