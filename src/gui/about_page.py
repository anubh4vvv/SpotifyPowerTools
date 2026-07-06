from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("AboutPage")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.web_view = QWebEngineView()
        self.web_view.setObjectName("WebAboutView")
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls,
            True,
        )

        self.web_view.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls,
            True,
        )

        html_path = (
            Path(__file__).resolve().parent
            / "web"
            / "about.html"
        )

        self.web_view.setUrl(
            QUrl.fromLocalFile(str(html_path))
        )

        root_layout.addWidget(self.web_view)