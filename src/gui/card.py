from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class Card(QFrame):

    def __init__(self, title=""):
        super().__init__()

        self.setObjectName("Card")

        self.layout = QVBoxLayout(self)

        if title:

            label = QLabel(title)

            label.setObjectName("CardTitle")

            self.layout.addWidget(label)