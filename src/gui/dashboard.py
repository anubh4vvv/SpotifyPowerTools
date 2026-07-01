from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QScrollArea,
)

from PySide6.QtCore import Qt

from gui.current_song_card import CurrentSongCard
from gui.player_controls_card import PlayerControlsCard
from gui.playlist_card import PlaylistCard
from gui.shuffle_panel import ShufflePanel
from gui.preview_panel import PreviewPanel


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content = QWidget()

        layout = QGridLayout(content)

        layout.setContentsMargins(25, 25, 25, 25)

        layout.setHorizontalSpacing(24)

        layout.setVerticalSpacing(28)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 2)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 0)
        layout.setRowStretch(2, 1)

        self.current_song_card = CurrentSongCard()

        self.player_controls_card = PlayerControlsCard()

        self.playlist_card = PlaylistCard()

        self.shuffle_panel = ShufflePanel()

        self.preview_panel = PreviewPanel()

        layout.addWidget(
            self.current_song_card,
            0,
            0
        )

        layout.addWidget(
            self.player_controls_card,
            0,
            1
        )

        layout.addWidget(
            self.playlist_card,
            1,
            0
        )

        layout.addWidget(
            self.shuffle_panel,
            1,
            1
        )

        layout.addWidget(
            self.preview_panel,
            2,
            0,
            1,
            2
        )

        scroll.setWidget(content)

        root_layout.addWidget(scroll)