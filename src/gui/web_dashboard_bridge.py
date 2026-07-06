from PySide6.QtCore import QObject, Signal, Slot


class WebDashboardBridge(QObject):
    previousRequested = Signal()
    playPauseRequested = Signal()
    nextRequested = Signal()

    previewRequested = Signal()
    queueRequested = Signal()

    ratingRequested = Signal(int)
    seekRequested = Signal(float)

    pageRequested = Signal(str)

    @Slot()
    def previous(self):
        self.previousRequested.emit()

    @Slot()
    def playPause(self):
        self.playPauseRequested.emit()

    @Slot()
    def next(self):
        self.nextRequested.emit()

    @Slot()
    def previewShuffle(self):
        self.previewRequested.emit()

    @Slot()
    def queueShuffle(self):
        self.queueRequested.emit()

    @Slot(int)
    def rateSong(self, rating):
        self.ratingRequested.emit(rating)

    @Slot(float)
    def seekToFraction(self, fraction):
        self.seekRequested.emit(fraction)

    @Slot(str)
    def openPage(self, page_name):
        self.pageRequested.emit(page_name)