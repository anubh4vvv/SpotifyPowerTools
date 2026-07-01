from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QPushButton,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.queue_item import QueueItem


class QueuePage(QWidget):

    MAX_ITEMS = 25

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

        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("Spotify Queue")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "View the songs currently waiting in your Spotify queue."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.refresh_button = QPushButton("Refresh Queue")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.refresh_button)

        self.now_playing_card = Card("Currently Playing")

        self.now_playing_label = QLabel("No active playback")
        self.now_playing_label.setWordWrap(True)
        self.now_playing_label.setStyleSheet(
            "color:#DADADA; font-size:12pt;"
        )

        self.now_playing_card.layout.addWidget(
            self.now_playing_label
        )

        layout.addWidget(self.now_playing_card)

        self.queue_card = Card("Upcoming Queue")

        self.empty_label = QLabel("No queue data yet.")
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.queue_card.layout.addWidget(
            self.empty_label
        )

        self.queue_items = []

        for _ in range(self.MAX_ITEMS):

            item = QueueItem()
            item.hide()

            self.queue_items.append(item)

            self.queue_card.layout.addWidget(item)

        layout.addWidget(self.queue_card)
        layout.addStretch()

        scroll.setWidget(content)

        root_layout.addWidget(scroll)

    def set_loading(self, loading):

        if loading:
            self.refresh_button.setEnabled(False)
            self.refresh_button.setText("Loading Queue...")
            self.empty_label.show()
            self.empty_label.setText("Loading Spotify queue...")
        else:
            self.refresh_button.setEnabled(True)
            self.refresh_button.setText("Refresh Queue")


    def update_queue(self, queue_data):

        currently_playing = queue_data.get(
            "currently_playing"
        )

        queue = queue_data.get(
            "queue",
            []
        )

        if currently_playing is None:
            self.now_playing_label.setText(
                "No active playback"
            )
        else:
            self.now_playing_label.setText(
                f"{currently_playing.name} — {currently_playing.artist}"
            )

        for item in self.queue_items:
            item.hide()

        if not queue:
            self.empty_label.show()
            self.empty_label.setText(
                "Your Spotify queue is currently empty, or Spotify did not return queue data."
            )
            return

        self.empty_label.hide()

        for widget, song in zip(self.queue_items, queue):

            widget.update_song(song)
            widget.show()