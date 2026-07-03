from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QComboBox,
)

from PySide6.QtCore import Qt

from gui.card import Card


class PlayerControlsCard(Card):

    def __init__(self):
        super().__init__("Playback Controls")

        self.setMinimumHeight(360)

        self.last_volume_percent = None
        self.last_shuffle_state = None
        self.last_repeat_state = None
        self.last_devices_signature = None

        self.layout.setSpacing(18)

        volume_title = QLabel("Volume")
        volume_title.setStyleSheet(
            "color:#DADADA; font-size:12pt; font-weight:700;"
        )

        volume_row = QHBoxLayout()

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.volume_value = QLabel("50%")
        self.volume_value.setFixedWidth(50)
        self.volume_value.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter
        )
        self.volume_value.setStyleSheet(
            "color:#A0A0A0; font-size:11pt;"
        )

        volume_row.addWidget(self.volume_slider, 1)
        volume_row.addWidget(self.volume_value)

        mode_title = QLabel("Playback Mode")
        mode_title.setStyleSheet(
            "color:#DADADA; font-size:12pt; font-weight:700;"
        )

        mode_row = QHBoxLayout()

        self.shuffle_button = QPushButton("Shuffle: Off")
        self.shuffle_button.setObjectName("SecondaryButton")

        self.repeat_combo = QComboBox()
        self.repeat_combo.addItems([
            "Repeat Off",
            "Repeat Track",
            "Repeat Playlist",
        ])

        mode_row.addWidget(self.shuffle_button)
        mode_row.addWidget(self.repeat_combo)

        device_title = QLabel("Spotify Device")
        device_title.setStyleSheet(
            "color:#DADADA; font-size:12pt; font-weight:700;"
        )

        device_row = QHBoxLayout()

        self.device_combo = QComboBox()
        self.device_combo.setMinimumWidth(260)
        self.device_combo.addItem(
            "Refresh devices",
            ""
        )

        self.refresh_devices_button = QPushButton("Refresh Devices")
        self.refresh_devices_button.setObjectName("SecondaryButton")

        device_row.addWidget(self.device_combo, 1)
        device_row.addWidget(self.refresh_devices_button)

        self.helper_label = QLabel(
            "Use this panel to control volume, shuffle, repeat mode, and Spotify Connect devices."
        )
        self.helper_label.setWordWrap(True)
        self.helper_label.setStyleSheet(
            "color:#8F97A3; font-size:10.5pt;"
        )

        self.volume_slider.valueChanged.connect(
            self.update_volume_label
        )

        self.layout.addWidget(volume_title)
        self.layout.addLayout(volume_row)
        self.layout.addSpacing(8)
        self.layout.addWidget(mode_title)
        self.layout.addLayout(mode_row)
        self.layout.addSpacing(8)
        self.layout.addWidget(device_title)
        self.layout.addLayout(device_row)
        self.layout.addSpacing(8)
        self.layout.addWidget(self.helper_label)
        self.layout.addStretch()

    def update_volume_label(self, value):

        self.volume_value.setText(
            f"{value}%"
        )

    def selected_device_id(self):

        return self.device_combo.currentData()

    def reset_playback_state(self):

        if (
            self.last_volume_percent == 0
            and self.last_shuffle_state is False
            and self.last_repeat_state == "off"
        ):
            return

        self.last_volume_percent = 0
        self.last_shuffle_state = False
        self.last_repeat_state = "off"

        self.shuffle_button.setText("Shuffle: Off")

        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(0)
        self.volume_slider.blockSignals(False)

        self.volume_value.setText("0%")

        self.repeat_combo.blockSignals(True)
        self.repeat_combo.setCurrentText("Repeat Off")
        self.repeat_combo.blockSignals(False)

    def update_playback_state(self, current):

        if current is None:
            self.reset_playback_state()
            return

        device = current.get(
            "device",
            {}
        )

        volume_percent = device.get(
            "volume_percent",
            0
        )

        if volume_percent is None:
            volume_percent = 0

        if (
            volume_percent != self.last_volume_percent
            and not self.volume_slider.isSliderDown()
        ):

            self.last_volume_percent = volume_percent

            self.volume_slider.blockSignals(True)
            self.volume_slider.setValue(
                volume_percent
            )
            self.volume_slider.blockSignals(False)

            self.volume_value.setText(
                f"{volume_percent}%"
            )

        shuffle_state = bool(
            current.get("shuffle_state")
        )

        if shuffle_state != self.last_shuffle_state:

            self.last_shuffle_state = shuffle_state

            if shuffle_state:
                self.shuffle_button.setText("Shuffle: On")
            else:
                self.shuffle_button.setText("Shuffle: Off")

        repeat_state = current.get(
            "repeat_state",
            "off"
        )

        if repeat_state != self.last_repeat_state:

            self.last_repeat_state = repeat_state

            repeat_label = {
                "off": "Repeat Off",
                "track": "Repeat Track",
                "context": "Repeat Playlist",
            }.get(
                repeat_state,
                "Repeat Off"
            )

            self.repeat_combo.blockSignals(True)
            self.repeat_combo.setCurrentText(
                repeat_label
            )
            self.repeat_combo.blockSignals(False)

    def make_devices_signature(self, devices, active_device_id):

        signature = []

        for device in devices:

            signature.append((
                device.get("id", ""),
                device.get("name", ""),
                device.get("type", ""),
                bool(device.get("is_active", False)),
                active_device_id,
            ))

        return tuple(signature)

    def update_devices(self, devices, active_device_id=None):

        devices = devices or []

        signature = self.make_devices_signature(
            devices,
            active_device_id
        )

        if signature == self.last_devices_signature:
            return

        self.last_devices_signature = signature

        self.device_combo.blockSignals(True)
        self.device_combo.clear()

        if not devices:

            self.device_combo.addItem(
                "No devices found",
                ""
            )

            self.device_combo.setEnabled(False)
            self.device_combo.blockSignals(False)

            return

        self.device_combo.setEnabled(True)

        active_index = 0

        for index, device in enumerate(devices):

            name = device.get(
                "name",
                "Unknown Device"
            )

            device_type = device.get(
                "type",
                "Unknown"
            )

            device_id = device.get(
                "id",
                ""
            )

            is_active = device.get(
                "is_active",
                False
            )

            label = f"{name} ({device_type})"

            if is_active:
                label += " • Active"

            self.device_combo.addItem(
                label,
                device_id
            )

            if is_active or device_id == active_device_id:
                active_index = index

        self.device_combo.setCurrentIndex(
            active_index
        )

        self.device_combo.blockSignals(False)