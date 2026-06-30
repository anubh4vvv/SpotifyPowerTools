from PySide6.QtCore import QObject, Signal, Slot


class QueueShuffleWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, controller, limit):
        super().__init__()

        self.controller = controller
        self.limit = limit

    @Slot()
    def run(self):

        try:

            result = self.controller.queue_smart_shuffle(
                limit=self.limit
            )

            self.finished.emit(result)

        except Exception as error:

            self.error.emit(str(error))