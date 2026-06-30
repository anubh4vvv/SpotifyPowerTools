from PySide6.QtWidgets import QLabel

from gui.card import Card


class PlaylistCard(Card):

    def __init__(self):

        super().__init__("Current Playlist")

        self.name = QLabel()

        self.name.setStyleSheet("""
            font-size:18pt;
            font-weight:bold;
        """)

        self.count = QLabel()

        self.layout.addWidget(self.name)

        self.layout.addWidget(self.count)

    def update_playlist(self, playlist, tracks):

        if playlist is None:

            self.name.setText("Nothing Playing")

            self.count.clear()

            return

        self.name.setText(
            playlist["name"]
        )

        self.count.setText(
            f"{len(tracks)} Songs"
        )