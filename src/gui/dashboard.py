from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from gui.current_song_card import CurrentSongCard
from gui.playlist_card import PlaylistCard
from gui.shuffle_panel import ShufflePanel
from gui.preview_panel import PreviewPanel


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        layout.setContentsMargins(25, 25, 25, 25)

        layout.setHorizontalSpacing(24)

        layout.setVerticalSpacing(24)
        # Make both columns equal width
        # Give the left column more room
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)

        # Keep both rows equal height
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        self.current_song_card = CurrentSongCard()

        self.playlist_card = PlaylistCard()

        self.shuffle_panel = ShufflePanel()

        self.preview_panel = PreviewPanel()

        # Top row
        layout.addWidget(
            self.current_song_card,
            0,
            0
        )

        layout.addWidget(
            self.playlist_card,
            0,
            1
        )

        # Bottom row
        layout.addWidget(
            self.shuffle_panel,
            1,
            0
        )

        layout.addWidget(
            self.preview_panel,
            1,
            1
        )

        # Analytics placeholder
        #
        # Future:
        #
        # layout.addWidget(
        #     self.analytics_panel,
        #     2,
        #     0,
        #     1,
        #     2
        # )