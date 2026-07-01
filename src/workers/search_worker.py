from PySide6.QtCore import QObject, Signal, Slot


class SearchWorker(QObject):

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, controller, query, limit=10):
        super().__init__()

        self.controller = controller
        self.query = query
        self.limit = limit

    @Slot()
    def run(self):

        try:
            results = self.controller.search_tracks(
                self.query,
                limit=self.limit
            )

            self.finished.emit(results)

        except Exception as error:
            self.error.emit(str(error))