import random

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import (
    QImage,
    QPainter,
    QPixmap,
    QColor,
)
from PySide6.QtWidgets import QWidget


class FilmGrainOverlay(QWidget):

    def __init__(self, parent=None, opacity=0.14, tile_size=180):
        super().__init__(parent)

        self.opacity = opacity
        self.tile_size = tile_size
        self.grain_tile = self.create_grain_tile(tile_size)

        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        if parent is not None:
            self.setGeometry(parent.rect())
            parent.installEventFilter(self)

        self.show()
        self.raise_()

    def create_grain_tile(self, size):
        image = QImage(
            size,
            size,
            QImage.Format_ARGB32
        )

        image.fill(Qt.transparent)

        random.seed(42)

        for y in range(size):
            for x in range(size):
                roll = random.randint(0, 255)

                if roll < 120:
                    alpha = random.randint(0, 36)
                    color = QColor(0, 0, 0, alpha)
                else:
                    alpha = random.randint(0, 28)
                    color = QColor(255, 238, 205, alpha)

                image.setPixelColor(x, y, color)

        return QPixmap.fromImage(image)

    def eventFilter(self, watched, event):
        if watched is self.parent() and event.type() == QEvent.Resize:
            self.setGeometry(watched.rect())
            self.raise_()

        return super().eventFilter(watched, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        painter.setOpacity(self.opacity)
        painter.drawTiledPixmap(
            self.rect(),
            self.grain_tile
        )