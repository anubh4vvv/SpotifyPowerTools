from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt, Signal

from gui.image_loader import load_pixmap


class SearchResultItem(QWidget):

    add_clicked = Signal(object)

    def __init__(self, song):
        super().__init__()

        self.song = song

        self.setObjectName("SearchResultItem")
        self.setMinimumHeight(82)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(14)

        self.cover = QLabel()
        self.cover.setFixedSize(56, 56)

        if song.image_url:

            pixmap = load_pixmap(
                song.image_url
            )

            if not pixmap.isNull():

                self.cover.setPixmap(
                    pixmap.scaled(
                        56,
                        56,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                )

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        self.song_label = QLabel(song.name)
        self.song_label.setStyleSheet(
            "color:#FFFFFF; font-size:12pt; font-weight:700;"
        )

        self.artist_label = QLabel(
            f"{song.artist} • {song.album}"
        )
        self.artist_label.setStyleSheet(
            "color:#A0A0A0; font-size:10.5pt;"
        )

        text_layout.addWidget(self.song_label)
        text_layout.addWidget(self.artist_label)

        self.add_button = QPushButton("Add to Queue")
        self.add_button.setObjectName("SecondaryButton")
        self.add_button.setFixedWidth(150)

        self.add_button.clicked.connect(
            self.emit_add_clicked
        )

        layout.addWidget(self.cover)
        layout.addLayout(text_layout, 1)
        layout.addWidget(self.add_button)

        self.setStyleSheet("""
            QWidget#SearchResultItem {
                background:#151518;
                border:1px solid #2A2A2D;
                border-radius:12px;
            }
        """)

    def emit_add_clicked(self):

        self.add_clicked.emit(
            self.song
        )