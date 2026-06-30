from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.queue_item import QueueItem


class PreviewPanel(Card):

    MAX_PREVIEW = 10

    def __init__(self):

        super().__init__("Upcoming Queue")

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setFrameShape(QScrollArea.NoFrame)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        container = QWidget()

        self.container = QVBoxLayout(container)

        self.container.setSpacing(8)

        self.container.setContentsMargins(0, 0, 0, 0)

        self.items = []

        # Create the queue widgets only ONCE
        for _ in range(self.MAX_PREVIEW):

            item = QueueItem()

            item.hide()

            self.items.append(item)

            self.container.addWidget(item)

        self.container.addStretch()

        scroll.setWidget(container)

        self.layout.addWidget(scroll)

    def show_tracks(self, tracks):

        # Hide everything first
        for item in self.items:
            item.hide()

        # Update only the widgets we need
        for widget, song in zip(self.items, tracks):

            widget.update_song(song)

            widget.show()