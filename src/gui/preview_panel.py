from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt

from gui.card import Card
from gui.image_loader import load_pixmap


class PreviewRow(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedHeight(118)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.index_label = QLabel("")
        self.index_label.setFixedWidth(28)
        self.index_label.setAlignment(
            Qt.AlignCenter
        )
        self.index_label.setStyleSheet(
            "color:#1DB954; font-size:10pt; font-weight:900;"
        )

        self.cover = QLabel()
        self.cover.setFixedSize(52, 52)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(3)

        self.song_label = QLabel("")
        self.song_label.setStyleSheet(
            "color:#FFFFFF; font-size:11pt; font-weight:800;"
        )

        self.artist_label = QLabel("")
        self.artist_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        self.reason_label = QLabel("")
        self.reason_label.setWordWrap(True)
        self.reason_label.setStyleSheet(
            "color:#1DB954; font-size:9.5pt; font-weight:600;"
        )

        text_layout.addWidget(self.song_label)
        text_layout.addWidget(self.artist_label)
        text_layout.addWidget(self.reason_label)

        layout.addWidget(self.index_label)
        layout.addWidget(self.cover)
        layout.addLayout(text_layout, 1)

        self.setStyleSheet("""
            PreviewRow {
                background:#151518;
                border:1px solid #2A2A2D;
                border-radius:12px;
            }

            PreviewRow:hover {
                border:1px solid #1DB954;
                background:#1B1B20;
            }
        """)

    def update_item(self, index, item):

        if isinstance(item, dict):
            song = item.get("song")
            score = item.get("score", 0)
            reasons = item.get("reasons", [])
        else:
            song = item
            score = None
            reasons = []

        if song is None:
            return

        self.index_label.setText(
            str(index)
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

        if song.image_url:

            pixmap = load_pixmap(
                song.image_url
            )

            if not pixmap.isNull():

                self.cover.setPixmap(
                    pixmap.scaled(
                        52,
                        52,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                )

                return

        self.cover.clear()

    def format_reasons(self, score, reasons):

        cleaned_reasons = []

        for reason in reasons:

            if reason not in cleaned_reasons:
                cleaned_reasons.append(
                    reason
                )

        priority_reasons = []

        priority_keywords = [
            "Recently skipped",
            "High skip percentage",
            "Moderate skip percentage",
            "Played very recently",
            "Played recently",
            "Recently finished",
            "Often replayed",
            "Strong completion rate",
            "Not recently played",
            "No listening memory",
        ]

        for keyword in priority_keywords:

            for reason in cleaned_reasons:

                if keyword in reason and reason not in priority_reasons:
                    priority_reasons.append(
                        reason
                    )

        for reason in cleaned_reasons:

            if reason not in priority_reasons:
                priority_reasons.append(
                    reason
                )

        cleaned_reasons = priority_reasons[:5]

        if not cleaned_reasons:

            cleaned_reasons = [
                "Smart shuffle selection"
            ]

        reason_text = " • ".join(
            cleaned_reasons
        )

        if score is None:
            return reason_text

        return f"Score {score} • {reason_text}"


class PreviewPanel(Card):

    def __init__(self):

        super().__init__("Upcoming Queue")

        self.setMinimumHeight(500)

        self.layout.setSpacing(12)

        self.helper_label = QLabel(
            "Preview of the smart-shuffled songs that will be added to your Spotify queue."
        )
        self.helper_label.setWordWrap(True)
        self.helper_label.setStyleSheet(
            "color:#8F97A3; font-size:10.5pt;"
        )

        self.empty_label = QLabel(
            "No preview yet. Click Preview Shuffle to generate upcoming songs."
        )
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(10)

        self.rows = []

        self.layout.addWidget(self.helper_label)
        self.layout.addWidget(self.empty_label)
        self.layout.addLayout(self.rows_layout)
        self.layout.addStretch()

    def clear_rows(self):

        for row in self.rows:
            row.setParent(None)
            row.deleteLater()

        self.rows = []

    def show_tracks(self, tracks):

        self.clear_rows()

        if not tracks:
            self.empty_label.show()
            self.empty_label.setText(
                "No preview available."
            )
            return

        self.empty_label.hide()

        self.helper_label.setText(
            f"Previewing {len(tracks)} songs with shuffle explanations."
        )

        for index, item in enumerate(
            tracks,
            start=1
        ):

            row = PreviewRow()

            row.update_item(
                index,
                item
            )

            self.rows.append(row)

            self.rows_layout.addWidget(row)