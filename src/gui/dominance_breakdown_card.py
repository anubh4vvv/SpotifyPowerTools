from PySide6.QtWidgets import QLabel

from gui.card import Card
from gui.metric_bar import MetricBar


class DominanceBreakdownCard(Card):

    def __init__(self):
        super().__init__("Dominance Breakdown")

        self.setMinimumHeight(230)

        self.top_artist_bar = MetricBar("Top Artist Dominance")
        self.top_album_bar = MetricBar("Top Album Dominance")

        self.duplicate_label = QLabel("Duplicate Pressure: 0 extra copies")
        self.duplicate_label.setWordWrap(True)
        self.duplicate_label.setStyleSheet(
            "color:#DADADA; font-size:11pt; font-weight:700;"
        )

        self.context_label = QLabel("")
        self.context_label.setWordWrap(True)
        self.context_label.setStyleSheet(
            "color:#8F97A3; font-size:10.5pt;"
        )

        self.layout.addWidget(self.top_artist_bar)
        self.layout.addWidget(self.top_album_bar)
        self.layout.addSpacing(8)
        self.layout.addWidget(self.duplicate_label)
        self.layout.addWidget(self.context_label)

    def update_dominance(self, analytics):

        top_artist_name = analytics["top_artist_name"]
        top_artist_percentage = analytics["top_artist_percentage"]

        top_album_name = analytics["top_album_name"]
        top_album_percentage = analytics["top_album_percentage"]

        duplicate_count = analytics["duplicate_count"]

        self.top_artist_bar.name_label.setText(
            f"Top Artist: {top_artist_name}"
        )

        self.top_artist_bar.update_value(
            top_artist_percentage
        )

        self.top_album_bar.name_label.setText(
            f"Top Album: {top_album_name}"
        )

        self.top_album_bar.update_value(
            top_album_percentage
        )

        self.duplicate_label.setText(
            f"Duplicate Pressure: {duplicate_count} extra copies"
        )

        if duplicate_count == 0:
            duplicate_text = "No duplicate pressure detected."
        elif duplicate_count <= 3:
            duplicate_text = "Duplicate pressure is low."
        elif duplicate_count <= 10:
            duplicate_text = "Duplicate pressure is moderate."
        else:
            duplicate_text = "Duplicate pressure is high."

        self.context_label.setText(
            (
                f"{top_artist_name} makes up {top_artist_percentage}% of the playlist. "
                f"{top_album_name} makes up {top_album_percentage}% of the playlist. "
                f"{duplicate_text}"
            )
        )