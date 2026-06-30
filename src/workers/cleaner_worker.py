from PySide6.QtCore import QObject, Signal, Slot


class CleanerWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, controller):
        super().__init__()

        self.controller = controller

    @Slot()
    def run(self):

        try:

            result = self.controller.create_cleaned_playlist()

            self.finished.emit(result)

        except Exception as error:

            self.error.emit(str(error))