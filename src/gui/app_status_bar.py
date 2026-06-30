from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)


class AppStatusBar(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("AppStatusBar")
        self.setFixedHeight(34)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 6, 18, 6)

        self.message = QLabel("Ready")
        self.message.setObjectName("StatusMessage")

        layout.addWidget(self.message)
        layout.addStretch()

    def set_message(self, text):
        self.message.setText(text)