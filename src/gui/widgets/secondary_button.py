from PySide6.QtWidgets import QPushButton


class SecondaryButton(QPushButton):

    def __init__(self, text):

        super().__init__(text)

        self.setMinimumHeight(42)

        self.setObjectName("SecondaryButton")