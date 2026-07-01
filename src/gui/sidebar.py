from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class Sidebar(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        self.buttons = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 28, 22, 24)
        layout.setSpacing(12)

        title = QLabel("Spotify\nPower Tools")
        title.setObjectName("SidebarTitle")
        title.setWordWrap(True)

        subtitle = QLabel("Smart Playlist Companion")
        subtitle.setObjectName("SidebarSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(28)

        self.dashboard_btn = self.make_button("Dashboard")
        self.shuffle_btn = self.make_button("Smart Shuffle")
        self.queue_btn = self.make_button("Queue")
        self.search_btn = self.make_button("Search")
        self.analytics_btn = self.make_button("Analytics")
        self.duplicates_btn = self.make_button("Duplicates")
        self.settings_btn = self.make_button("Settings")
        self.about_btn = self.make_button("About")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.shuffle_btn)
        layout.addWidget(self.queue_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.analytics_btn)
        layout.addWidget(self.duplicates_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.about_btn)

        layout.addStretch()

        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        version.setObjectName("SidebarVersion")

        layout.addWidget(version)

        self.set_active_button(
            self.dashboard_btn
        )

    def make_button(self, text):

        button = QPushButton(text)
        button.setObjectName("SidebarButton")
        button.setCursor(Qt.PointingHandCursor)

        self.buttons.append(
            button
        )

        return button

    def set_active_button(self, active_button):

        for button in self.buttons:

            if button == active_button:

                button.setStyleSheet("""
                    QPushButton#SidebarButton {
                        background:#1DB954;
                        color:#000000;
                        border:none;
                        border-radius:10px;
                        padding:12px 14px;
                        text-align:left;
                        font-size:11pt;
                        font-weight:800;
                    }
                """)

            else:

                button.setStyleSheet("")