from PySide6.QtCore import QObject, Signal, Slot


class QueueViewWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, controller, limit=25):
        super().__init__()

        self.controller = controller
        self.limit = limit

    @Slot()
    def run(self):

        try:
            queue_data = self.controller.get_user_queue(
                limit=self.limit
            )

            self.finished.emit(queue_data)

        except Exception as error:
            self.error.emit(str(error))