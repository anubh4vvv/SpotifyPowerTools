from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QColor


class Header(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Header")
        self.setFixedHeight(64)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(26)
        shadow.setOffset(0, 8)
        shadow.setColor(
            QColor(0, 0, 0, 75)
        )

        self.setGraphicsEffect(
            shadow
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 14, 28, 14)
        layout.setSpacing(16)

        self.logo = QLabel("♫")
        self.logo.setObjectName("HeaderLogo")
        self.logo.setFixedSize(34, 34)
        self.logo.setAlignment(Qt.AlignCenter)

        text_block = QFrame()
        text_layout = QVBoxLayout(text_block)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self.title = QLabel("PowerTools")
        self.subtitle = QLabel("playlist intelligence, quietly")

        self.subtitle = QLabel("playlist intelligence, quietly")
        self.subtitle.setObjectName("HeaderSubtitle")

        text_layout.addWidget(
            self.title
        )

        text_layout.addWidget(
            self.subtitle
        )

        self.status = QLabel("● Connected")
        self.status.setObjectName("HeaderStatus")
        self.status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(
            self.logo
        )

        layout.addWidget(
            text_block
        )

        layout.addStretch()

        layout.addWidget(
            self.status
        )

    def set_connected(self, connected: bool):

        if connected:

            self.status.setText("● Connected")
            self.status.setObjectName("HeaderStatus")

        else:

            self.status.setText("● Disconnected")
            self.status.setObjectName("HeaderStatusError")

        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.status.update()