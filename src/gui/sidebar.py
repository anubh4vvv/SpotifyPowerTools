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
        self.setFixedWidth(260)

        self.buttons = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 28, 22, 24)
        layout.setSpacing(11)

        title = QLabel('Power<span style="color:#e3a857;">Tools</span>')
        title.setObjectName("SidebarTitle")
        title.setTextFormat(Qt.RichText)

        subtitle = QLabel("FOR SPOTIFY")
        subtitle.setObjectName("SidebarSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(26)

        self.dashboard_btn = self.make_button("Dashboard", "●")
        self.shuffle_btn = self.make_button("Smart Shuffle", "↝")
        self.analytics_btn = self.make_button("Analytics", "▥")
        self.queue_btn = self.make_button("Queue", "≡")
        self.search_btn = self.make_button("Search", "⌕")
        self.duplicates_btn = self.make_button("Duplicates", "□")
        self.settings_btn = self.make_button("Settings", "○")
        self.about_btn = self.make_button("About", "i")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.shuffle_btn)
        layout.addWidget(self.analytics_btn)
        layout.addWidget(self.queue_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.duplicates_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.about_btn)

        layout.addStretch()

        version = QLabel("connected · adaptive profile")
        version.setObjectName("SidebarVersion")
        version.setAlignment(Qt.AlignLeft)

        layout.addWidget(version)

        self.set_active_button(self.dashboard_btn)

    def make_button(self, text, icon):
        button = QPushButton(f"{icon}   {text}")
        button.setObjectName("SidebarButton")
        button.setCursor(Qt.PointingHandCursor)
        button.setProperty("active", "false")

        self.buttons.append(button)

        return button

    def refresh_button_style(self, button):
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def set_active_button(self, active_button):
        for button in self.buttons:
            if button == active_button:
                button.setProperty("active", "true")
            else:
                button.setProperty("active", "false")

            self.refresh_button_style(button)