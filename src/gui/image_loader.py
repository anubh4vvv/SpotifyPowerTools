import requests

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


_IMAGE_CACHE = {}
_SCALED_IMAGE_CACHE = {}

MAX_IMAGE_CACHE_ITEMS = 250
MAX_SCALED_CACHE_ITEMS = 500


def trim_cache(cache, max_items):

    while len(cache) > max_items:
        oldest_key = next(iter(cache))
        del cache[oldest_key]


def load_pixmap(url):
    """
    Downloads an image once and reuses it
    for the rest of the application's lifetime.
    """

    if not url:
        return QPixmap()

    if url in _IMAGE_CACHE:
        return _IMAGE_CACHE[url]

    try:
        response = requests.get(
            url,
            timeout=5
        )

        response.raise_for_status()

        pixmap = QPixmap()
        pixmap.loadFromData(
            response.content
        )

        _IMAGE_CACHE[url] = pixmap

        trim_cache(
            _IMAGE_CACHE,
            MAX_IMAGE_CACHE_ITEMS
        )

        return pixmap

    except Exception:
        return QPixmap()


def load_scaled_pixmap(
    url,
    width,
    height,
    aspect_mode=Qt.KeepAspectRatio,
    transform_mode=Qt.SmoothTransformation
):
    """
    Loads and scales a pixmap once.

    This avoids repeatedly scaling the same album artwork.
    """

    if not url:
        return QPixmap()

    cache_key = (
        url,
        int(width),
        int(height),
        str(aspect_mode),
        str(transform_mode),
    )

    if cache_key in _SCALED_IMAGE_CACHE:
        return _SCALED_IMAGE_CACHE[cache_key]

    pixmap = load_pixmap(
        url
    )

    if pixmap.isNull():
        return QPixmap()

    scaled = pixmap.scaled(
        width,
        height,
        aspect_mode,
        transform_mode
    )

    _SCALED_IMAGE_CACHE[cache_key] = scaled

    trim_cache(
        _SCALED_IMAGE_CACHE,
        MAX_SCALED_CACHE_ITEMS
    )

    return scaled


def clear_image_cache():

    _IMAGE_CACHE.clear()
    _SCALED_IMAGE_CACHE.clear()


def cache_size():

    return {
        "original": len(_IMAGE_CACHE),
        "scaled": len(_SCALED_IMAGE_CACHE),
    }