from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from PySide6.QtCore import Qt


class Header(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Header")
        self.setFixedHeight(78)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 14, 28, 14)

        title_block = QFrame()
        title_layout = QHBoxLayout(title_block)
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel("Spotify Power Tools")
        self.title.setObjectName("HeaderTitle")

        self.subtitle = QLabel("Your intelligent Spotify companion")
        self.subtitle.setObjectName("HeaderSubtitle")

        text_block = QFrame()
        text_layout = QHBoxLayout(text_block)
        text_layout.setContentsMargins(0, 0, 0, 0)

        vertical_text = QFrame()
        from PySide6.QtWidgets import QVBoxLayout
        vertical_layout = QVBoxLayout(vertical_text)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(2)

        vertical_layout.addWidget(self.title)
        vertical_layout.addWidget(self.subtitle)

        title_layout.addWidget(vertical_text)

        self.status = QLabel("● Connected")
        self.status.setObjectName("HeaderStatus")
        self.status.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(title_block)
        layout.addStretch()
        layout.addWidget(self.status)

    def set_connected(self, connected: bool):

        if connected:
            self.status.setText("● Connected")
            self.status.setObjectName("HeaderStatus")
        else:
            self.status.setText("● Disconnected")
            self.status.setObjectName("HeaderStatusError")

        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)