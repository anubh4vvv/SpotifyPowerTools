from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSlider,
    QPushButton,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from gui.card import Card

from services.settings_service import (
    load_settings,
    save_settings,
    reset_settings,
)


class SettingsPage(QWidget):

    settings_saved = Signal(dict)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("Settings")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "Customize Spotify Power Tools and save your defaults."
        )
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.card = Card("Default Shuffle Settings")

        self.profile = QComboBox()
        self.profile.addItems([
            "Balanced",
            "Discovery",
            "Album",
            "Random",
            "Custom"
        ])

        self.queue_size = QComboBox()
        self.queue_size.addItems([
            "10 songs",
            "25 songs",
            "50 songs",
            "100 songs"
        ])

        self.artist_slider = QSlider(Qt.Horizontal)
        self.artist_slider.setRange(0, 100)

        self.album_slider = QSlider(Qt.Horizontal)
        self.album_slider.setRange(0, 100)

        self.random_slider = QSlider(Qt.Horizontal)
        self.random_slider.setRange(0, 100)

        self.artist_value = QLabel()
        self.album_value = QLabel()
        self.random_value = QLabel()

        self.add_setting_row(
            "Default Profile",
            self.profile
        )

        self.add_setting_row(
            "Default Queue Size",
            self.queue_size
        )

        self.add_slider_row(
            "Artist Weight",
            self.artist_slider,
            self.artist_value
        )

        self.add_slider_row(
            "Album Weight",
            self.album_slider,
            self.album_value
        )

        self.add_slider_row(
            "Randomness",
            self.random_slider,
            self.random_value
        )

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Save Settings")
        self.reset_button = QPushButton("Reset Defaults")

        self.reset_button.setObjectName("SecondaryButton")

        buttons.addWidget(self.save_button)
        buttons.addWidget(self.reset_button)

        self.card.layout.addLayout(buttons)

        self.message = QLabel("")
        self.message.setStyleSheet(
            "color:#1DB954; font-size:10pt;"
        )

        self.card.layout.addWidget(self.message)

        layout.addWidget(self.card)
        layout.addStretch()

        self.artist_slider.valueChanged.connect(
            self.update_value_labels
        )

        self.album_slider.valueChanged.connect(
            self.update_value_labels
        )

        self.random_slider.valueChanged.connect(
            self.update_value_labels
        )

        self.save_button.clicked.connect(
            self.save_current_settings
        )

        self.reset_button.clicked.connect(
            self.reset_to_defaults
        )

        self.load_from_saved()

    def add_setting_row(self, label_text, widget):

        label = QLabel(label_text)
        label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        self.card.layout.addWidget(label)
        self.card.layout.addWidget(widget)

    def add_slider_row(self, label_text, slider, value_label):

        row = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet(
            "color:#DADADA; font-size:11pt;"
        )

        value_label.setFixedWidth(40)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value_label)

        self.card.layout.addLayout(row)
        self.card.layout.addWidget(slider)

    def update_value_labels(self):

        self.artist_value.setText(
            str(self.artist_slider.value())
        )

        self.album_value.setText(
            str(self.album_slider.value())
        )

        self.random_value.setText(
            str(self.random_slider.value())
        )

    def load_from_saved(self):

        settings = load_settings()

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

        self.update_value_labels()

    def get_settings(self):

        queue_size_text = self.queue_size.currentText()

        return {
            "queue_size": int(queue_size_text.split()[0]),
            "shuffle_profile": self.profile.currentText(),
            "artist_weight": self.artist_slider.value(),
            "album_weight": self.album_slider.value(),
            "randomness": self.random_slider.value(),
        }

    def save_current_settings(self):

        settings = save_settings(
            self.get_settings()
        )

        self.message.setText(
            "Settings saved."
        )

        self.settings_saved.emit(
            settings
        )

    def reset_to_defaults(self):

        settings = reset_settings()

        self.load_from_saved()

        self.message.setText(
            "Defaults restored."
        )

        self.settings_saved.emit(
            settings
        )