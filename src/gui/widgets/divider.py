from PySide6.QtWidgets import QFrame


class Divider(QFrame):

    def __init__(self):

        super().__init__()

        self.setFrameShape(QFrame.HLine)

        self.setObjectName("Divider")