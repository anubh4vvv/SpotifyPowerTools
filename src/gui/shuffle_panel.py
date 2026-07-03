from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
)

from PySide6.QtCore import Qt, QTimer

from gui.card import Card

from services.settings_service import load_settings


class ShufflePanel(Card):

    def __init__(self):

        super().__init__("Smart Shuffle")
        self.setMinimumHeight(300)

        self.profile = QComboBox()

        self.profile.addItems([
            "Balanced",
            "Discovery",
            "Adaptive",
            "Album",
            "Random",
            "Weighted",
            "Custom"
        ])

        self.queue_size = QComboBox()

        self.queue_size.addItems([
            "10 songs",
            "25 songs",
            "50 songs",
            "100 songs"
        ])

        self.artist_slider = QSlider(
            Qt.Horizontal
        )

        self.artist_slider.setRange(0, 100)

        self.album_slider = QSlider(
            Qt.Horizontal
        )

        self.album_slider.setRange(0, 100)

        self.random_slider = QSlider(
            Qt.Horizontal
        )

        self.random_slider.setRange(0, 100)

        self.preview_button = QPushButton(
            "Preview Shuffle"
        )

        self.apply_button = QPushButton(
            "Queue Smart Shuffle"
        )

        self.apply_button.setEnabled(False)

        self.layout.addWidget(
            QLabel("Profile")
        )

        self.layout.addWidget(
            self.profile
        )

        self.layout.addWidget(
            QLabel("Queue Size")
        )

        self.layout.addWidget(
            self.queue_size
        )

        self.layout.addWidget(
            QLabel("Artist Weight")
        )

        self.layout.addWidget(
            self.artist_slider
        )

        self.layout.addWidget(
            QLabel("Album Weight")
        )

        self.layout.addWidget(
            self.album_slider
        )

        self.layout.addWidget(
            QLabel("Randomness")
        )

        self.layout.addWidget(
            self.random_slider
        )

        buttons = QHBoxLayout()

        buttons.addWidget(
            self.preview_button
        )

        buttons.addWidget(
            self.apply_button
        )

        self.layout.addLayout(buttons)

        self.apply_settings(
            load_settings()
        )

    def apply_settings(self, settings):

        self.profile.setCurrentText(
            settings["shuffle_profile"]
        )

        self.queue_size.setCurrentText(
            f"{settings['queue_size']} songs"
        )

        self.artist_slider.setValue(
            settings["artist_weight"]
        )

        self.album_slider.setValue(
            settings["album_weight"]
        )

        self.random_slider.setValue(
            settings["randomness"]
        )

    def get_settings(self):

        return {
            "queue_size": self.get_queue_limit(),
            "shuffle_profile": self.profile.currentText(),
            "artist_weight": self.artist_slider.value(),
            "album_weight": self.album_slider.value(),
            "randomness": self.random_slider.value(),
        }

    def highlight(self):
        self.setStyleSheet(
            """
            QFrame#Card{
                background:#111113;
                border:2px solid #1DB954;
                border-radius:16px;
            }
            """
        )

        QTimer.singleShot(
            1200,
            self.clear_highlight
        )

    def clear_highlight(self):
        self.setStyleSheet("")


    def get_queue_limit(self):

        text = self.queue_size.currentText()

        number = text.split()[0]

        return int(number)