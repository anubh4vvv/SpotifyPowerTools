from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
)

from PySide6.QtCore import Qt, Signal

from gui.card import Card
from gui.search_result_item import SearchResultItem


class SearchPage(QWidget):

    search_requested = Signal(str)
    add_to_queue_requested = Signal(object)

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(24)

        title = QLabel("Search Spotify")
        title.setObjectName("SectionTitle")

        subtitle = QLabel(
            "Search for tracks and add them directly to your Spotify queue."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        search_card = Card("Find a Song")

        search_row = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search song, artist, album..."
        )
        self.search_input.setMinimumHeight(42)

        self.search_button = QPushButton("Search")
        self.search_button.setMinimumHeight(42)

        search_row.addWidget(self.search_input, 1)
        search_row.addWidget(self.search_button)

        search_card.layout.addLayout(search_row)

        layout.addWidget(search_card)

        self.results_card = Card("Results")

        self.empty_label = QLabel(
            "No search yet. Type a song name and press Search."
        )
        self.empty_label.setWordWrap(True)
        self.empty_label.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.results_layout = QVBoxLayout()
        self.results_layout.setSpacing(12)

        self.results_card.layout.addWidget(
            self.empty_label
        )

        self.results_card.layout.addLayout(
            self.results_layout
        )

        layout.addWidget(self.results_card)
        layout.addStretch()

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

        self.search_button.clicked.connect(
            self.emit_search
        )

        self.search_input.returnPressed.connect(
            self.emit_search
        )

    def emit_search(self):

        query = self.search_input.text().strip()

        if not query:
            return

        self.search_requested.emit(
            query
        )

    def set_loading(self, loading):

        if loading:
            self.search_button.setEnabled(False)
            self.search_button.setText("Searching...")
            self.empty_label.show()
            self.empty_label.setText("Searching Spotify...")
        else:
            self.search_button.setEnabled(True)
            self.search_button.setText("Search")

    def clear_results(self):

        while self.results_layout.count():

            item = self.results_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def show_results(self, songs):

        self.clear_results()

        if not songs:
            self.empty_label.show()
            self.empty_label.setText(
                "No tracks found. Try a different search."
            )
            return

        self.empty_label.hide()

        for song in songs:

            item = SearchResultItem(
                song
            )

            item.add_clicked.connect(
                self.add_to_queue_requested.emit
            )

            self.results_layout.addWidget(
                item
            )