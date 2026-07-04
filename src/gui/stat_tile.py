from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import QColor


class StatTile(QFrame):

    def __init__(self, title):

        super().__init__()

        self.setObjectName("StatTile")
        self.setMinimumHeight(135)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 7)
        shadow.setColor(
            QColor(0, 0, 0, 65)
        )

        self.setGraphicsEffect(
            shadow
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        self.title = QLabel(title)
        self.title.setObjectName("StatTitle")
        self.title.setAlignment(Qt.AlignCenter)

        self.value = QLabel("--")
        self.value.setObjectName("StatValue")
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setWordWrap(True)

        layout.addWidget(
            self.title
        )

        layout.addStretch()

        layout.addWidget(
            self.value
        )

        layout.addStretch()

    def set_value(self, value):

        self.value.setText(
            str(value)
        )