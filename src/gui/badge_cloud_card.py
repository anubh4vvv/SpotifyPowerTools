from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
)

from PySide6.QtCore import Qt

from gui.card import Card


class BadgeCloudCard(Card):

    def __init__(self):
        super().__init__("Playlist Badges")

        self.setMinimumHeight(250)

        self.badge_grid = QGridLayout()
        self.badge_grid.setSpacing(12)

        self.layout.addLayout(
            self.badge_grid
        )

    def clear_badges(self):

        while self.badge_grid.count():

            item = self.badge_grid.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def update_badges(self, badges):

        self.clear_badges()

        if not badges:

            empty = QLabel("No badges unlocked yet.")
            empty.setObjectName("BadgeEmpty")
            self.badge_grid.addWidget(
                empty,
                0,
                0
            )

            return

        for index, badge in enumerate(badges):

            row = index // 4
            column = index % 4

            label = QLabel(
                (
                    f"{badge.get('emoji', '✨')}  {badge.get('title', 'Badge')}\n"
                    f"{badge.get('description', '')}"
                )
            )

            label.setObjectName("BadgePill")
            label.setAlignment(
                Qt.AlignCenter
            )
            label.setWordWrap(True)
            label.setMinimumHeight(78)

            self.badge_grid.addWidget(
                label,
                row,
                column
            )