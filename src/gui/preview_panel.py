from PySide6.QtWidgets import (
    QListWidget,
)

from gui.card import Card


class PreviewPanel(Card):

    def __init__(self):

        super().__init__("Upcoming Songs")

        self.list = QListWidget()

        self.layout.addWidget(self.list)

    def show_tracks(self, tracks):

        self.list.clear()

        for i, song in enumerate(
            tracks,
            start=1
        ):

            self.list.addItem(
                f"{i}. {song.name} — {song.artist}"
            )