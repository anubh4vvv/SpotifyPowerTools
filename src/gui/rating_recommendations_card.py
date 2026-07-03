from PySide6.QtWidgets import QLabel

from PySide6.QtCore import Qt

from gui.card import Card


class RatingRecommendationsCard(Card):

    def __init__(self):
        super().__init__("Smart Rating Recommendations")

        self.setMinimumHeight(220)

        self.summary_label = QLabel("No rating recommendations yet.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "color:#FFFFFF; font-size:12.5pt; font-weight:800;"
        )

        self.recommendations_label = QLabel()
        self.recommendations_label.setWordWrap(True)
        self.recommendations_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.recommendations_label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.layout.addWidget(
            self.summary_label
        )

        self.layout.addSpacing(10)

        self.layout.addWidget(
            self.recommendations_label
        )

    def update_recommendations(self, data):

        self.summary_label.setText(
            data["summary"]
        )

        lines = []

        for item in data["recommendations"]:
            lines.append(
                f"- {item}"
            )

        self.recommendations_label.setText(
            "\n".join(lines)
        )