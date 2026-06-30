from PySide6.QtCore import QObject, Signal, Slot


class PreviewWorker(QObject):

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, controller, settings=None):
        super().__init__()

        self.controller = controller
        self.settings = settings

    @Slot()
    def run(self):

        try:

            preview = self.controller.preview_shuffle(
                settings=self.settings
            )

            self.finished.emit(preview)

        except Exception as e:

            self.error.emit(str(e))