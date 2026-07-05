from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QFrame,
)

from PySide6.QtCore import Qt, QTimer

from gui.card import Card

from services.settings_service import load_settings


class QueuePreviewRow(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("QueuePreviewRow")
        self.setFixedHeight(42)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        self.index_label = QLabel("01")
        self.index_label.setObjectName("QueuePreviewIndex")
        self.index_label.setFixedWidth(30)
        self.index_label.setAlignment(Qt.AlignCenter)

        text_block = QVBoxLayout()
        text_block.setContentsMargins(0, 0, 0, 0)
        text_block.setSpacing(1)

        self.song_label = QLabel("")
        self.song_label.setObjectName("QueuePreviewSong")
        self.song_label.setWordWrap(False)

        self.reason_label = QLabel("")
        self.reason_label.setObjectName("QueuePreviewReason")
        self.reason_label.setWordWrap(False)

        self.artist_label = QLabel("")
        self.artist_label.setObjectName("QueuePreviewArtist")
        self.artist_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.artist_label.setMinimumWidth(105)

        text_block.addWidget(self.song_label)
        text_block.addWidget(self.reason_label)

        layout.addWidget(self.index_label)
        layout.addLayout(text_block, 1)
        layout.addWidget(self.artist_label)

    def update_item(self, index, item):

        if isinstance(item, dict):
            song = item.get("song")
            score = item.get("score")
            reasons = item.get("reasons", [])
        else:
            song = item
            score = None
            reasons = []

        if song is None:
            return

        self.index_label.setText(
            f"{index:02d}"
        )

        self.song_label.setText(
            song.name
        )

        self.artist_label.setText(
            song.artist
        )

        reason_text = self.format_reasons(
            score,
            reasons
        )

        self.reason_label.setText(
            reason_text
        )

        self.reason_label.setToolTip(
            reason_text
        )

    def format_reasons(self, score, reasons):

        cleaned = []

        for reason in reasons:
            if reason not in cleaned:
                cleaned.append(reason)

        if cleaned:
            reason_text = " • ".join(cleaned[:2])
        else:
            reason_text = "Smart shuffle selection"

        if score is None:
            return reason_text

        return f"Score {round(score, 1)} • {reason_text}"


class ShufflePanel(Card):

    def __init__(self):

        super().__init__("Smart Shuffle")

        self.setMinimumHeight(390)

        self.profile = QComboBox()
        self.profile.setObjectName("ShuffleMiniControl")
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
        self.queue_size.setObjectName("ShuffleMiniControl")
        self.queue_size.addItems([
            "10 songs",
            "25 songs",
            "50 songs",
            "100 songs"
        ])

        # These sliders are still kept for backend/settings compatibility.
        # They are hidden from the dashboard because the mockup has a cleaner Smart Shuffle card.
        self.artist_slider = QSlider(Qt.Horizontal)
        self.album_slider = QSlider(Qt.Horizontal)
        self.random_slider = QSlider(Qt.Horizontal)

        for slider in [
            self.artist_slider,
            self.album_slider,
            self.random_slider,
        ]:
            slider.setRange(0, 100)
            slider.setVisible(False)

        self.preview_button = QPushButton(
            "Preview Shuffle"
        )
        self.preview_button.setObjectName("SecondaryButton")

        self.apply_button = QPushButton(
            "queue songs into spotify"
        )
        self.apply_button.setEnabled(False)

        self.profile_tag = QLabel("adaptive")
        self.profile_tag.setObjectName("SmartShuffleBadge")
        self.profile_tag.setAlignment(Qt.AlignCenter)

        self.explanation = QLabel(
            "Leaning on your finish rate and recent replays — favoring tracks you sit through, "
            "easing off ones you tend to skip early."
        )
        self.explanation.setObjectName("ShuffleExplanation")
        self.explanation.setWordWrap(True)

        self.layout.setSpacing(12)

        self.build_controls()
        self.build_preview_area()
        self.build_buttons()

        self.profile.currentTextChanged.connect(
            self.update_profile_tag
        )

        self.apply_settings(
            load_settings()
        )

    def build_controls(self):

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(10)

        label = QLabel("profile")
        label.setObjectName("ShuffleControlLabel")

        queue_label = QLabel("queue")
        queue_label.setObjectName("ShuffleControlLabel")

        top_row.addWidget(label)
        top_row.addWidget(self.profile, 1)
        top_row.addWidget(queue_label)
        top_row.addWidget(self.queue_size, 1)
        top_row.addWidget(self.profile_tag)

        self.layout.addLayout(top_row)
        self.layout.addWidget(self.explanation)

    def build_preview_area(self):

        self.preview_frame = QFrame()
        self.preview_frame.setObjectName("QueuePreviewFrame")

        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(5)

        self.empty_preview_label = QLabel(
            "Preview your smart queue here. The first few songs will appear in this card."
        )
        self.empty_preview_label.setObjectName("QueueEmptyText")
        self.empty_preview_label.setWordWrap(True)

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(5)

        self.rows = []

        preview_layout.addWidget(self.empty_preview_label)
        preview_layout.addLayout(self.rows_layout)

        self.layout.addWidget(self.preview_frame, 1)

    def build_buttons(self):

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(10)

        button_row.addWidget(
            self.preview_button,
            1
        )

        button_row.addWidget(
            self.apply_button,
            1
        )

        self.layout.addLayout(button_row)

    def update_profile_tag(self):

        self.profile_tag.setText(
            self.profile.currentText().lower()
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

        self.update_profile_tag()

    def get_settings(self):

        return {
            "queue_size": self.get_queue_limit(),
            "shuffle_profile": self.profile.currentText(),
            "artist_weight": self.artist_slider.value(),
            "album_weight": self.album_slider.value(),
            "randomness": self.random_slider.value(),
        }

    def set_profile(self, profile_name):

        index = self.profile.findText(
            profile_name
        )

        if index < 0:
            return False

        self.profile.setCurrentIndex(
            index
        )

        self.update_profile_tag()

        return True

    def highlight(self):

        self.setStyleSheet(
            """
            QFrame#Card {
                background:#221c16;
                border:2px solid #e3a857;
                border-radius:10px;
            }
            """
        )

        QTimer.singleShot(
            900,
            self.clear_highlight
        )

    def clear_highlight(self):

        self.setStyleSheet("")

    def get_queue_limit(self):

        text = self.queue_size.currentText()

        number = text.split()[0]

        return int(number)

    def clear_rows(self):

        for row in self.rows:
            row.setParent(None)
            row.deleteLater()

        self.rows = []

    def show_tracks(self, tracks):

        self.clear_rows()

        tracks = tracks or []

        if not tracks:

            self.empty_preview_label.show()
            self.empty_preview_label.setText(
                "No preview yet. Click Preview Shuffle to generate your smart queue."
            )
            return

        self.empty_preview_label.hide()

        visible_tracks = tracks[:4]

        for index, item in enumerate(
            visible_tracks,
            start=1
        ):

            row = QueuePreviewRow()

            row.update_item(
                index,
                item
            )

            self.rows.append(
                row
            )

            self.rows_layout.addWidget(
                row
            )