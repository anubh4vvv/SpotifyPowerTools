from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from gui.current_song_card import CurrentSongCard
from gui.playlist_card import PlaylistCard
from gui.shuffle_panel import ShufflePanel
from gui.preview_panel import PreviewPanel


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        self.current_song_card = CurrentSongCard()

        self.playlist_card = PlaylistCard()

        self.shuffle_panel = ShufflePanel()

        self.preview_panel = PreviewPanel()

        layout.addWidget(self.current_song_card)

        layout.addWidget(self.playlist_card)

        layout.addWidget(self.shuffle_panel)

        layout.addWidget(self.preview_panel)

        layout.addStretch()