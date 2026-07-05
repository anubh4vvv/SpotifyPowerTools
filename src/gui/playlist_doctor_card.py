from PySide6.QtWidgets import (
    QLabel,
)

from PySide6.QtCore import Qt

from gui.card import Card


class PlaylistDoctorCard(Card):

    def __init__(self):
        super().__init__("Playlist Doctor")

        self.setMinimumHeight(135)
        self.setMaximumHeight(155)

        self.summary_label = QLabel("No diagnosis yet.")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "color:#FFFFFF; font-size:13pt; font-weight:800;"
        )

        self.strengths_label = QLabel()
        self.strengths_label.setWordWrap(True)
        self.strengths_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.strengths_label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.warnings_label = QLabel()
        self.warnings_label.setWordWrap(True)
        self.warnings_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.warnings_label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.suggestions_label = QLabel()
        self.suggestions_label.setWordWrap(True)
        self.suggestions_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.suggestions_label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.layout.addWidget(
            self.summary_label
        )

        self.layout.addSpacing(12)

        self.layout.addWidget(
            self.strengths_label
        )

        self.layout.addWidget(
            self.warnings_label
        )

        self.layout.addWidget(
            self.suggestions_label
        )

    def format_section(self, title, items):

        lines = [
            title
        ]

        for item in items:
            lines.append(
                f"- {item}"
            )

        return "\n".join(lines)

    def update_diagnosis(self, diagnosis):

        self.summary_label.setText(
            diagnosis["summary"]
        )

        self.strengths_label.setText(
            self.format_section(
                "Strengths",
                diagnosis["strengths"]
            )
        )

        self.warnings_label.setText(
            self.format_section(
                "Warnings",
                diagnosis["warnings"]
            )
        )

        self.suggestions_label.setText(
            self.format_section(
                "Suggestions",
                diagnosis["suggestions"]
            )
        )