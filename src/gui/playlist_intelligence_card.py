from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from PySide6.QtCore import Qt, Signal

from gui.card import Card


class PlaylistIntelligenceCard(Card):

    apply_profile_requested = Signal(str)
    export_report_requested = Signal()

    def __init__(self):
        super().__init__("Playlist Intelligence")

        self.setMinimumHeight(330)

        self.current_profile = "Balanced"

        self.summary_label = QLabel("No intelligence data yet.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "color:#FFFFFF; font-size:12.5pt; font-weight:900;"
        )

        self.reason_label = QLabel("")
        self.reason_label.setWordWrap(True)
        self.reason_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.reason_label.setStyleSheet(
            "color:#DADADA; font-size:10.5pt;"
        )

        self.cleanup_label = QLabel("")
        self.cleanup_label.setWordWrap(True)
        self.cleanup_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.cleanup_label.setStyleSheet(
            "color:#FFCC66; font-size:10.5pt;"
        )

        self.hidden_favorites_label = QLabel("")
        self.hidden_favorites_label.setWordWrap(True)
        self.hidden_favorites_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.hidden_favorites_label.setStyleSheet(
            "color:#1DB954; font-size:10.5pt;"
        )

        button_row = QHBoxLayout()

        self.apply_button = QPushButton("Apply Recommended Profile")
        self.export_button = QPushButton("Export Playlist Report")
        self.export_button.setObjectName("SecondaryButton")

        button_row.addWidget(
            self.apply_button
        )

        button_row.addWidget(
            self.export_button
        )

        self.layout.addWidget(
            self.summary_label
        )

        self.layout.addWidget(
            self.reason_label
        )

        self.layout.addSpacing(8)

        self.layout.addWidget(
            self.cleanup_label
        )

        self.layout.addSpacing(8)

        self.layout.addWidget(
            self.hidden_favorites_label
        )

        self.layout.addSpacing(10)

        self.layout.addLayout(
            button_row
        )

        self.apply_button.clicked.connect(
            self.emit_apply_profile
        )

        self.export_button.clicked.connect(
            self.export_report_requested.emit
        )

    def emit_apply_profile(self):

        self.apply_profile_requested.emit(
            self.current_profile
        )

    def format_items(self, title, items):

        lines = [
            title
        ]

        if not items:
            lines.append(
                "  No items found."
            )
            return "\n".join(lines)

        for index, item in enumerate(
            items,
            start=1
        ):

            lines.append(
                f"  {index}. {item['name']} — {item['artist']}"
            )

            reason = item.get(
                "reason",
                ""
            )

            if reason:
                lines.append(
                    f"     {reason}"
                )

        return "\n".join(lines)

    def update_intelligence(self, data):

        profile = data.get(
            "recommended_profile",
            "Balanced"
        )

        confidence = data.get(
            "recommendation_confidence",
            "Low"
        )

        reason = data.get(
            "recommendation_reason",
            ""
        )

        self.current_profile = profile

        self.summary_label.setText(
            f"Recommended Profile: {profile}  •  Confidence: {confidence}"
        )

        if reason:
            self.reason_label.setText(
                reason
            )
        else:
            self.reason_label.setText(
                "No recommendation reason available yet."
            )

        self.cleanup_label.setText(
            self.format_items(
                "Skip-aware Cleanup Suggestions:",
                data.get("cleanup_suggestions", [])
            )
        )

        self.hidden_favorites_label.setText(
            self.format_items(
                "Hidden Favorites:",
                data.get("hidden_favorites", [])
            )
        )