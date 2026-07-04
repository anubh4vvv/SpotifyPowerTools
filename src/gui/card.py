from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import QColor


class Card(QFrame):

    def __init__(self, title=""):
        super().__init__()

        self.setObjectName("Card")
        self.setMouseTracking(True)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 10)
        shadow.setColor(
            QColor(0, 0, 0, 90)
        )

        self.setGraphicsEffect(
            shadow
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 18, 20, 20)
        self.layout.setSpacing(14)

        if title:

            label = QLabel(title)
            label.setObjectName("CardTitle")
            label.setWordWrap(True)

            self.layout.addWidget(
                label
            )