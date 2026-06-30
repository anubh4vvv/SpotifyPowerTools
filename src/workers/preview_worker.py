from PySide6.QtCore import QObject, Signal, Slot


class PreviewWorker(QObject):

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    @Slot()
    def run(self):

        try:

            preview = self.controller.preview_shuffle()

            self.finished.emit(preview)

        except Exception as e:

            self.error.emit(str(e))