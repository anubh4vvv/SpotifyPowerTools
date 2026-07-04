from PySide6.QtWidgets import QLabel

from gui.card import Card


class WrappedStatCard(Card):

    def __init__(self, fallback_title, fallback_emoji="✨"):
        super().__init__()

        self.setObjectName("WrappedStatCard")
        self.setMinimumHeight(210)

        self.fallback_title = fallback_title
        self.fallback_emoji = fallback_emoji

        self.emoji_label = QLabel(fallback_emoji)
        self.emoji_label.setObjectName("WrappedEmoji")

        self.title_label = QLabel(fallback_title)
        self.title_label.setObjectName("WrappedTitle")
        self.title_label.setWordWrap(True)

        self.value_label = QLabel("No data yet")
        self.value_label.setObjectName("WrappedValue")
        self.value_label.setWordWrap(True)

        self.subtitle_label = QLabel("Keep listening to unlock this.")
        self.subtitle_label.setObjectName("WrappedSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.layout.addWidget(
            self.emoji_label
        )

        self.layout.addSpacing(6)

        self.layout.addWidget(
            self.title_label
        )

        self.layout.addWidget(
            self.value_label
        )

        self.layout.addWidget(
            self.subtitle_label
        )

        self.layout.addStretch()

    def update_card(self, data):

        self.emoji_label.setText(
            data.get("emoji", self.fallback_emoji)
        )

        self.title_label.setText(
            data.get("title", self.fallback_title)
        )

        self.value_label.setText(
            data.get("value", "No data yet")
        )

        self.subtitle_label.setText(
            data.get("subtitle", "Keep listening to unlock this.")
        )