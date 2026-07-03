from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
)

from PySide6.QtCore import Qt


class MetricBar(QWidget):

    def __init__(self, label):
        super().__init__()

        self.label_text = label

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.name_label = QLabel(label)
        self.name_label.setStyleSheet(
            "color:#EAEAEA; font-size:10.5pt; font-weight:700;"
        )

        self.value_label = QLabel("0%")
        self.value_label.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        self.value_label.setStyleSheet(
            "color:#A0A0A0; font-size:10pt; font-weight:700;"
        )

        top_row.addWidget(self.name_label)
        top_row.addStretch()
        top_row.addWidget(self.value_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(9)

        layout.addLayout(top_row)
        layout.addWidget(self.progress)

    def update_value(self, value, suffix="%"):

        if value is None:
            value = 0

        value_number = float(value)

        progress_value = int(
            max(
                0,
                min(100, round(value_number))
            )
        )

        self.progress.setValue(
            progress_value
        )

        if suffix:
            self.value_label.setText(
                f"{value}{suffix}"
            )
        else:
            self.value_label.setText(
                str(value)
            )