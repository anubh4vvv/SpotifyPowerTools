from PySide6.QtCore import QObject, Signal, Slot


class SearchWorker(QObject):

    finished = Signal(str, list)
    error = Signal(str, str)

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

            self.finished.emit(
                self.query,
                results
            )

        except Exception as error:
            self.error.emit(
                self.query,
                str(error)
            )