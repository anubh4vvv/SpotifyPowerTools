from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QFrame,
    QScrollArea,
)

from PySide6.QtCore import Qt, QTimer

from gui.card import Card
from services.settings_service import load_settings


class QueuePreviewRow(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("QueuePreviewRow")
        self.setFixedHeight(46)
        self.setMinimumWidth(760)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        self.index_label = QLabel("01")
        self.index_label.setObjectName("QueuePreviewIndex")
        self.index_label.setFixedWidth(34)
        self.index_label.setAlignment(Qt.AlignCenter)

        text_block = QVBoxLayout()
        text_block.setContentsMargins(0, 0, 0, 0)
        text_block.setSpacing(0)

        self.song_label = QLabel("")
        self.song_label.setObjectName("QueuePreviewSong")
        self.song_label.setMinimumWidth(330)

        self.reason_label = QLabel("")
        self.reason_label.setObjectName("QueuePreviewReason")
        self.reason_label.setMinimumWidth(430)

        self.artist_label = QLabel("")
        self.artist_label.setObjectName("QueuePreviewArtist")
        self.artist_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.artist_label.setMinimumWidth(150)

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

        self.index_label.setText(f"{index:02d}")
        self.song_label.setText(song.name)
        self.artist_label.setText(song.artist)

        reason_text = self.format_reasons(score, reasons)

        self.reason_label.setText(reason_text)
        self.reason_label.setToolTip(reason_text)

    def format_reasons(self, score, reasons):
        cleaned = []

        for reason in reasons:
            if reason not in cleaned:
                cleaned.append(reason)

        cleaned = cleaned[:3]

        if cleaned:
            reason_text = " • ".join(cleaned)
        else:
            reason_text = "Smart shuffle selection"

        if score is None:
            return reason_text

        return f"Score {round(score, 1)} • {reason_text}"


class ShufflePanel(Card):

    def __init__(self):
        super().__init__("SMART SHUFFLE")

        self.setObjectName("SmartShuffleCard")
        self.setMinimumHeight(400)
        self.setMaximumHeight(410)

        self.profile = QComboBox()
        self.profile.addItems([
            "Balanced",
            "Discovery",
            "Adaptive",
            "Album",
            "Random",
            "Weighted",
            "Custom",
        ])

        self.queue_size = QComboBox()
        self.queue_size.addItems([
            "10 songs",
            "25 songs",
            "50 songs",
            "100 songs",
        ])

        self.profile.setVisible(False)
        self.queue_size.setVisible(False)

        self.artist_slider = QSlider(Qt.Horizontal)
        self.album_slider = QSlider(Qt.Horizontal)
        self.random_slider = QSlider(Qt.Horizontal)

        for slider in (
            self.artist_slider,
            self.album_slider,
            self.random_slider,
        ):
            slider.setRange(0, 100)
            slider.setVisible(False)

        self.preview_button = QPushButton("Preview Shuffle")
        self.preview_button.setObjectName("GhostButton")

        self.apply_button = QPushButton("queue 25 tracks into spotify")
        self.apply_button.setObjectName("AmberButton")
        self.apply_button.setEnabled(False)

        self.profile_tag = QLabel("adaptive")
        self.profile_tag.setObjectName("SmartShuffleBadge")
        self.profile_tag.setAlignment(Qt.AlignCenter)

        self.explanation = QLabel(
            "Leaning on your finish rate and recent replays — favoring "
            "tracks you sit through, easing off ones you tend to skip early."
        )
        self.explanation.setObjectName("ShuffleExplanation")
        self.explanation.setWordWrap(True)

        self.rows = []

        self.layout.setSpacing(12)

        self.build_top()
        self.build_preview_area()
        self.build_buttons()

        self.profile.currentTextChanged.connect(
            self.update_profile_tag
        )

        self.queue_size.currentTextChanged.connect(
            self.update_queue_button_text
        )

        self.apply_settings(
            load_settings()
        )

    def build_top(self):
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(8)

        top_row.addStretch()
        top_row.addWidget(self.profile_tag)

        self.layout.addLayout(top_row)
        self.layout.addWidget(self.explanation)

    def build_preview_area(self):
        self.preview_frame = QFrame()
        self.preview_frame.setObjectName("QueuePreviewFrame")
        self.preview_frame.setMinimumHeight(194)
        self.preview_frame.setMaximumHeight(206)

        frame_layout = QVBoxLayout(self.preview_frame)
        frame_layout.setContentsMargins(8, 8, 8, 8)
        frame_layout.setSpacing(0)

        self.empty_preview_label = QLabel(
            "Preview your smart queue. Songs will appear here."
        )
        self.empty_preview_label.setObjectName("QueueEmptyText")
        self.empty_preview_label.setWordWrap(True)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("QueuePreviewScroll")
        self.scroll.setWidgetResizable(False)
        self.scroll.setFrameShape(QScrollArea.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("QueuePreviewScrollContent")
        self.scroll_content.setMinimumWidth(790)

        self.rows_layout = QVBoxLayout(self.scroll_content)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(4)

        self.rows_layout.addWidget(self.empty_preview_label)
        self.rows_layout.addStretch()

        self.scroll.setWidget(self.scroll_content)

        frame_layout.addWidget(self.scroll)

        self.layout.addWidget(self.preview_frame)

    def build_buttons(self):
        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 0, 0, 0)
        button_row.setSpacing(10)

        button_row.addWidget(self.preview_button, 1)
        button_row.addWidget(self.apply_button, 3)

        self.layout.addLayout(button_row)

    def update_profile_tag(self):
        self.profile_tag.setText(
            self.profile.currentText().lower()
        )

    def update_queue_button_text(self):
        self.apply_button.setText(
            f"queue {self.get_queue_limit()} tracks into spotify"
        )

    def set_preview_loading(self):
        self.preview_button.setText("Generating...")
        self.apply_button.setEnabled(False)

    def set_preview_ready(self):
        self.preview_button.setText("Preview Shuffle")
        self.apply_button.setEnabled(True)
        self.update_queue_button_text()

    def set_preview_failed(self):
        self.preview_button.setText("Preview Shuffle")
        self.apply_button.setEnabled(False)
        self.update_queue_button_text()

    def set_queue_idle(self):
        self.apply_button.setEnabled(True)
        self.update_queue_button_text()

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
        self.update_queue_button_text()

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

        self.profile.setCurrentIndex(index)
        self.update_profile_tag()

        return True

    def highlight(self):
        self.setStyleSheet(
            """
            QFrame#SmartShuffleCard {
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

    def rebuild_rows_layout(self):
        while self.rows_layout.count():
            item = self.rows_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)

        for row in self.rows:
            self.rows_layout.addWidget(row)

        self.rows_layout.addStretch()

        required_height = max(
            160,
            len(self.rows) * 50 + 12
        )

        self.scroll_content.setMinimumHeight(required_height)

    def show_tracks(self, tracks):
        self.clear_rows()

        tracks = tracks or []

        if not tracks:
            self.empty_preview_label.setText(
                "No preview yet. Click Preview Shuffle to generate your smart queue."
            )
            self.empty_preview_label.show()

            self.rows_layout.addWidget(self.empty_preview_label)
            self.rows_layout.addStretch()

            return

        self.empty_preview_label.hide()

        for index, item in enumerate(tracks, start=1):
            row = QueuePreviewRow()
            row.update_item(index, item)

            self.rows.append(row)

        self.rebuild_rows_layout()