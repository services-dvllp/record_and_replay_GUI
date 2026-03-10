from __future__ import annotations

import importlib.util
from pathlib import Path

from PyQt6 import QtWidgets

from project.communication.interface_manager import InterfaceManager
from project.core.record_controller import RecordController
from project.core.replay_controller import ReplayController
from project.core.usb_info_controller import UsbInfoController
from project.utils.connection_monitor import ConnectionMonitorThread
from project.utils.message_utils import show_error, show_info

WIFI_INTERFACE_OPTION = "WiFi Interface"


def _load_legacy_ui_class():
    legacy_path = Path(__file__).resolve().parents[2] / "Record_and_Replay_v1.69.py"
    spec = importlib.util.spec_from_file_location("legacy_record_replay", legacy_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load legacy UI file")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Ui_MainWindow


class MainGuiWindow(QtWidgets.QMainWindow):
    """Keeps existing UI but routes IO through interface-independent controllers."""

    def __init__(self):
        super().__init__()
        Ui_MainWindow = _load_legacy_ui_class()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.interface_manager = InterfaceManager(parent=self)
        self.record_controller = RecordController(self.interface_manager)
        self.replay_controller = ReplayController(self.interface_manager)
        self.usb_info_controller = UsbInfoController(self.interface_manager)

        self.monitor = ConnectionMonitorThread(
            self.interface_manager,
            on_disconnect=self._on_connection_lost,
            interval_s=2.0,
        )

        self.ui.comboBox_comport.currentIndexChanged.connect(self._on_interface_changed)
        self.ui.pushButton_usb_info.clicked.disconnect()
        self.ui.pushButton_usb_info.clicked.connect(self.open_usb_info)

    def _on_interface_changed(self):
        selected = self.ui.comboBox_comport.currentText()
        if selected == WIFI_INTERFACE_OPTION:
            self.interface_manager.set_interface(
                interface_type=InterfaceManager.INTERFACE_WIFI,
                ssid=self.ui.lineEdit_ssid.text(),
                password=self.ui.lineEdit_password.text(),
            )
        else:
            self.interface_manager.set_interface(
                interface_type=InterfaceManager.INTERFACE_COM,
                comport=selected,
                baudrate=int(self.ui.comboBox_baudrate.currentText()),
            )

    def connect_selected_interface(self) -> bool:
        connected = self.interface_manager.connect_interface()
        if connected and not self.monitor.is_alive():
            self.monitor.start()
        return connected

    def _on_connection_lost(self) -> None:
        if not self.interface_manager.reconnect_interface():
            show_error("Connection lost and reconnect failed.", parent=self)

    def open_usb_info(self):
        if not self.interface_manager.check_connection() and not self.connect_selected_interface():
            return
        lines = self.usb_info_controller.get_usb_info()
        show_info("\n".join(lines) if lines else "No USB info received.", title="USB info", parent=self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainGuiWindow()
    window.show()
    app.exec()
