from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from PySide6.QtCore import Qt


class StatTile(QFrame):

    def __init__(self, title):

        super().__init__()

        self.setObjectName("StatTile")

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)

        layout.setSpacing(8)

        self.title = QLabel(title)

        self.title.setObjectName("StatTitle")

        self.title.setAlignment(Qt.AlignCenter)

        self.value = QLabel("--")

        self.value.setObjectName("StatValue")

        self.value.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.value)

        layout.addStretch()

    def set_value(self, value):

        self.value.setText(str(value))