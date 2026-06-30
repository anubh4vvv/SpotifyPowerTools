from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
)

from PySide6.QtCore import Qt

from gui.card import Card


class BarChartCard(Card):

    def __init__(self, title, empty_message="No data yet"):
        super().__init__(title)

        self.empty_message = empty_message
        self.setMinimumHeight(250)

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(12)

        self.layout.addLayout(
            self.rows_layout
        )

    def clear_rows(self):

        while self.rows_layout.count():

            item = self.rows_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def set_data(self, items, max_items=5):

        self.clear_rows()

        if not items:
            self.add_empty_message()
            return

        cleaned_items = []

        for item in items[:max_items]:

            name, value = item

            cleaned_items.append(
                (
                    str(name),
                    int(value)
                )
            )

        if not cleaned_items:
            self.add_empty_message()
            return

        max_value = max(
            value
            for _, value in cleaned_items
        )

        if max_value <= 0:
            self.add_empty_message()
            return

        for index, item in enumerate(cleaned_items, start=1):

            name, value = item

            row = self.create_bar_row(
                index,
                name,
                value,
                max_value
            )

            self.rows_layout.addWidget(row)

        self.rows_layout.addStretch()

    def add_empty_message(self):

        label = QLabel(self.empty_message)
        label.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        self.rows_layout.addWidget(label)

    def create_bar_row(self, index, name, value, max_value):

        row = QWidget()

        layout = QVBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        name_label = QLabel(
            f"{index}. {name}"
        )
        name_label.setToolTip(name)
        name_label.setStyleSheet(
            "color:#EAEAEA; font-size:10.5pt; font-weight:600;"
        )

        value_label = QLabel(
            str(value)
        )
        value_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        value_label.setFixedWidth(45)
        value_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt;"
        )

        top_row.addWidget(name_label, 1)
        top_row.addWidget(value_label)

        bar = QProgressBar()
        bar.setRange(0, max_value)
        bar.setValue(value)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)

        layout.addLayout(top_row)
        layout.addWidget(bar)

        return row