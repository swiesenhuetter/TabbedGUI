from PySide6.QtCore import (QObject,
                            Signal,
                            Slot,
                            QTimer,
                            QMutex,
                            QMutexLocker,
                            QThread)

from PySide6.QtWidgets import (QApplication,
                               QLabel,
                               QVBoxLayout,
                               QWidget,
                               QPushButton)

from random import randint
from threading import current_thread

# Model
class HardwareModel(QObject):
    data_changed = Signal(str)  # Signal to notify view of changes

    def __init__(self):
        super().__init__()
        self._data = "Initial data"
        self._mutex = QMutex()  # Protect access to _data
        self._update_timer = QTimer()
        self._update_timer.setInterval(100)  # Throttle to 100ms (10 updates per second)
        self._update_timer.timeout.connect(self._emit_update)
        self._update_timer.start()

    def update_data(self, new_data):
        # Thread-safe update of data
        with QMutexLocker(self._mutex):
            self._data = new_data

    def get_data(self):
        with QMutexLocker(self._mutex):  # Automatically locks and unlocks
            return self._data

    def _emit_update(self):
        # Thread-safe emission of data
        with QMutexLocker(self._mutex):
            data = self._data
        self.data_changed.emit(data)  # Emit the latest data

# View
class HardwareView(QWidget):
    connect_requested = Signal()  # Signal to notify controller of connect request
    disconnect_requested = Signal()  # Signal to notify controller of disconnect request

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.label = QLabel(self.model.get_data())
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(lambda *args: self.connect_requested.emit())
        layout.addWidget(connect_btn)
        disconnect_btn = QPushButton("Disconnect")
        disconnect_btn.clicked.connect(lambda *args: self.disconnect_requested.emit())
        layout.addWidget(disconnect_btn)
        # Connect model's signal to update the view
        self.model.data_changed.connect(self.update_label)

    @Slot(str)
    def update_label(self, data):
        self.label.setText(data)

    def connect_device(self):
        self.model.update_data("Connected")

class HardwareController(QObject):
    def __init__(self, hw_view: HardwareView, device):
        super().__init__()
        self.view = hw_view
        self.device = device

        # Connect the view's signal to the device's method
        self.view.connect_requested.connect(self.device.connect_device)
        self.view.disconnect_requested.connect(self.device.disconnect_device)

# Simulated hardware device (runs in a separate thread)
class HardwareDevice(QThread):
    def __init__(self, model: HardwareModel):
        super().__init__()
        self.model = model
        self.connected = False

    def connect_device(self):
        print("Connecting to device...")
        self.start()
        self.connected = True

    def disconnect_device(self):
        print("Disconnecting from device...")
        self.connected = False

    def run(self):
        # Simulate frequent hardware updates
        current_thread().name = "connection thread"
        while self.connected:
            i = randint(0, 100)
            self.model.update_data(f"Update {i}")
            self.msleep(100)  # Simulate hardware delay

# Main application
if __name__ == "__main__":
    app = QApplication()

    hw_model = HardwareModel()
    view = HardwareView(hw_model)
    view.show()

    hardware = HardwareDevice(hw_model)
    controller = HardwareController(view, hardware)

    app.exec()