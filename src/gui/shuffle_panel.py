from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
)

from PySide6.QtCore import Qt

from gui.card import Card


class ShufflePanel(Card):

    def __init__(self):

        super().__init__("Smart Shuffle")

        self.profile = QComboBox()

        self.profile.addItems([
            "Balanced",
            "Discovery",
            "Album",
            "Random",
            "Custom"
        ])

        self.artist_slider = QSlider(
            Qt.Horizontal
        )

        self.artist_slider.setRange(0,100)

        self.artist_slider.setValue(50)

        self.album_slider = QSlider(
            Qt.Horizontal
        )

        self.album_slider.setRange(0,100)

        self.album_slider.setValue(50)

        self.random_slider = QSlider(
            Qt.Horizontal
        )

        self.random_slider.setRange(0,100)

        self.random_slider.setValue(50)

        self.preview_button = QPushButton(
            "Preview Shuffle"
        )

        self.apply_button = QPushButton(
            "Apply Shuffle"
        )

        self.apply_button.setEnabled(False)

        self.layout.addWidget(
            QLabel("Profile")
        )

        self.layout.addWidget(
            self.profile
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