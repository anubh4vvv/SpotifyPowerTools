from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
)

from gui.card import Card
from gui.stat_tile import StatTile

from services.analytics_service import calculate_playlist_analytics


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("Playlist Analytics")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "Understand the playlist you are currently listening to."
        )
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        self.total_songs = StatTile("Songs")
        self.unique_artists = StatTile("Artists")
        self.unique_albums = StatTile("Albums")
        self.explicit_songs = StatTile("Explicit")
        self.average_popularity = StatTile("Avg Popularity")
        self.duration = StatTile("Duration")
        self.diversity = StatTile("Diversity")
        self.status = StatTile("Status")

        stats_grid.addWidget(self.total_songs, 0, 0)
        stats_grid.addWidget(self.unique_artists, 0, 1)
        stats_grid.addWidget(self.unique_albums, 0, 2)
        stats_grid.addWidget(self.explicit_songs, 0, 3)

        stats_grid.addWidget(self.average_popularity, 1, 0)
        stats_grid.addWidget(self.duration, 1, 1)
        stats_grid.addWidget(self.diversity, 1, 2)
        stats_grid.addWidget(self.status, 1, 3)

        layout.addLayout(stats_grid)

        lists_grid = QGridLayout()
        lists_grid.setSpacing(20)

        self.top_artists_card = Card("Top Artists")
        self.top_albums_card = Card("Top Albums")
        self.release_years_card = Card("Release Years")

        self.top_artists_label = QLabel("No data yet")
        self.top_albums_label = QLabel("No data yet")
        self.release_years_label = QLabel("No data yet")

        for label in [
            self.top_artists_label,
            self.top_albums_label,
            self.release_years_label,
        ]:
            label.setStyleSheet(
                "color:#DADADA; font-size:12pt;"
            )

        self.top_artists_card.layout.addWidget(
            self.top_artists_label
        )

        self.top_albums_card.layout.addWidget(
            self.top_albums_label
        )

        self.release_years_card.layout.addWidget(
            self.release_years_label
        )

        lists_grid.addWidget(self.top_artists_card, 0, 0)
        lists_grid.addWidget(self.top_albums_card, 0, 1)
        lists_grid.addWidget(self.release_years_card, 0, 2)

        layout.addLayout(lists_grid)
        layout.addStretch()

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

        self.explicit_songs.set_value(
            analytics["explicit_songs"]
        )

        self.average_popularity.set_value(
            analytics["average_popularity"]
        )

        self.duration.set_value(
            analytics["total_duration"]
        )

        self.diversity.set_value(
            f"{analytics['diversity_score']}%"
        )

        if playlist is None:
            self.status.set_value("No Playlist")
        else:
            self.status.set_value("Live")

        self.top_artists_label.setText(
            self.format_ranked_list(
                analytics["top_artists"]
            )
        )

        self.top_albums_label.setText(
            self.format_ranked_list(
                analytics["top_albums"]
            )
        )

        self.release_years_label.setText(
            self.format_ranked_list(
                analytics["release_years"]
            )
        )

    def format_ranked_list(self, items):

        if not items:
            return "No data yet"

        lines = []

        for index, item in enumerate(items, start=1):
            name, count = item

            lines.append(
                f"{index}. {name}  —  {count}"
            )

        return "\n".join(lines)