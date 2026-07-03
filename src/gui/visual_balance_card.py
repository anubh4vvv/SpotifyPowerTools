from gui.card import Card
from gui.metric_bar import MetricBar


class VisualBalanceCard(Card):

    def __init__(self):
        super().__init__("Visual Balance Dashboard")

        self.setMinimumHeight(260)

        self.health_bar = MetricBar("Health Score")
        self.diversity_bar = MetricBar("Diversity")
        self.artist_entropy_bar = MetricBar("Artist Entropy")
        self.album_entropy_bar = MetricBar("Album Entropy")
        self.rating_coverage_bar = MetricBar("Rating Coverage")

        self.layout.addWidget(self.health_bar)
        self.layout.addWidget(self.diversity_bar)
        self.layout.addWidget(self.artist_entropy_bar)
        self.layout.addWidget(self.album_entropy_bar)
        self.layout.addWidget(self.rating_coverage_bar)

    def update_balance(self, analytics):

        self.health_bar.update_value(
            analytics["health_score"]
        )

        self.diversity_bar.update_value(
            analytics["diversity_score"]
        )

        self.artist_entropy_bar.update_value(
            analytics["artist_entropy_score"]
        )

        self.album_entropy_bar.update_value(
            analytics["album_entropy_score"]
        )

        self.rating_coverage_bar.update_value(
            analytics["rated_percentage"]
        )