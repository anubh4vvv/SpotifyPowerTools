import requests

from PySide6.QtGui import QPixmap


# Cache for downloaded album artwork
_IMAGE_CACHE = {}


def load_pixmap(url):
    """
    Downloads an image once and reuses it
    for the rest of the application's lifetime.
    """

    if not url:
        return QPixmap()

    # Already cached?
    if url in _IMAGE_CACHE:
        return _IMAGE_CACHE[url]

    try:

        response = requests.get(
            url,
            timeout=5
        )

        response.raise_for_status()

        pixmap = QPixmap()

        pixmap.loadFromData(response.content)

        _IMAGE_CACHE[url] = pixmap

        return pixmap

    except Exception:

        return QPixmap()


def clear_image_cache():
    """
    Clears every cached image.
    Useful if we ever implement a Refresh Cache button.
    """

    _IMAGE_CACHE.clear()


def cache_size():
    """
    Returns number of cached images.
    """

    return len(_IMAGE_CACHE)