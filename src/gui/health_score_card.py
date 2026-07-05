from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QHBoxLayout,
)

from PySide6.QtCore import Qt

from gui.card import Card


class HealthScoreCard(Card):

    def __init__(self):
        super().__init__("Playlist Health")

        self.setMinimumHeight(170)

        self.score_label = QLabel("0%")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet(
            "font-size:42pt; font-weight:900; color:white;"
        )

        self.status_label = QLabel("No Data")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "font-size:14pt; font-weight:700; color: #e3a857;"
        )

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)

        detail_row = QHBoxLayout()

        self.duplicates_label = QLabel("Duplicates: 0")
        self.diversity_label = QLabel("Diversity: 0%")

        for label in [
            self.duplicates_label,
            self.diversity_label,
        ]:
            label.setStyleSheet(
                "color:#A0A0A0; font-size:10.5pt;"
            )

        detail_row.addWidget(self.duplicates_label)
        detail_row.addStretch()
        detail_row.addWidget(self.diversity_label)

        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.progress)
        self.layout.addLayout(detail_row)

    def update_health(
        self,
        score,
        status,
        duplicate_count,
        diversity_score
    ):

        score_int = int(score)

        self.score_label.setText(
            f"{score}%"
        )

        self.status_label.setText(
            status
        )

        self.progress.setValue(
            score_int
        )

        self.duplicates_label.setText(
            f"Duplicates: {duplicate_count}"
        )

        self.diversity_label.setText(
            f"Diversity: {diversity_score}%"
        )