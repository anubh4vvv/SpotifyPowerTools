import requests

from PySide6.QtGui import QPixmap


def load_pixmap(url):

    response = requests.get(url)

    pixmap = QPixmap()

    pixmap.loadFromData(response.content)

    return pixmap