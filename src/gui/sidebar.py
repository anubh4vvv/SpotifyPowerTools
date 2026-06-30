from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
)


class Sidebar(QFrame):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout(self)

        title = QLabel("Spotify\nPower Tools")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addStretch()