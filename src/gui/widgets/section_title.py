from PySide6.QtWidgets import QLabel


class SectionTitle(QLabel):

    def __init__(self, text):

        super().__init__(text)

        self.setObjectName("SectionTitle")