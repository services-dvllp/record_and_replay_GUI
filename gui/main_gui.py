from __future__ import annotations

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from communication.interface_manager import InterfaceManager, InterfaceSelection, InterfaceType
from core.record_controller import RecordController
from core.replay_controller import ReplayController
from core.usb_info_controller import UsbInfoController
from utils.connection_monitor import ConnectionMonitorThread


WIFI_INTERFACE_OPTION = "WiFi Interface"


class MainGui(QMainWindow):
    """GUI layer only. No direct serial/SSH calls are allowed here."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("GNSS Record and Replay")

        self.interface_manager = InterfaceManager()
        self.record_controller = RecordController(self.interface_manager)
        self.replay_controller = ReplayController(self.interface_manager)
        self.usb_info_controller = UsbInfoController(self.interface_manager)
        self.connection_monitor_thread: ConnectionMonitorThread | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        container = QWidget()
        root_layout = QVBoxLayout(container)

        form = QFormLayout()
        self.comboBox_comport = QComboBox()
        self.comboBox_comport.addItems(["COM3", "COM4", WIFI_INTERFACE_OPTION])

        self.lineEdit_ssid = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Interface", self.comboBox_comport)
        form.addRow("WiFi SSID", self.lineEdit_ssid)
        form.addRow("WiFi Password", self.lineEdit_password)

        root_layout.addLayout(form)

        button_layout = QHBoxLayout()
        self.pushButton_submit = QPushButton("Submit")
        self.pushButton_usb_info = QPushButton("USB Info")
        self.pushButton_submit.clicked.connect(self.on_submit_clicked)
        self.pushButton_usb_info.clicked.connect(self.on_usb_info_clicked)
        button_layout.addWidget(self.pushButton_submit)
        button_layout.addWidget(self.pushButton_usb_info)
        root_layout.addLayout(button_layout)

        root_layout.addWidget(QLabel("Responses"))
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        root_layout.addWidget(self.text_log)

        self.setCentralWidget(container)

    def _build_selection(self) -> InterfaceSelection:
        selected = self.comboBox_comport.currentText().strip()
        if selected == WIFI_INTERFACE_OPTION:
            return InterfaceSelection(
                interface_type=InterfaceType.WIFI,
                ssid=self.lineEdit_ssid.text().strip(),
                password=self.lineEdit_password.text().strip(),
            )
        return InterfaceSelection(interface_type=InterfaceType.COM, comport=selected)

    def on_submit_clicked(self) -> None:
        selection = self._build_selection()
        try:
            self.interface_manager.set_interface(selection)
            self.interface_manager.connect_interface()
        except Exception as exc:
            message = str(exc)
            if selection.interface_type == InterfaceType.COM:
                message = "You cannot open this COM Port!"
            elif "WiFi is not connected." in message:
                message = "WiFi is not connected."
            else:
                message = "Unable to establish SSH connection."
            QMessageBox.critical(self, "Connection Error", message)
            return

        self._append_log(f"Connected via {selection.interface_type.value}")
        self._start_connection_monitor_if_needed()

    def on_usb_info_clicked(self) -> None:
        try:
            usb_info = self.usb_info_controller.get_usb_info()
            self._append_log(usb_info)
        except Exception as exc:
            QMessageBox.warning(self, "USB Info", str(exc))

    def _start_connection_monitor_if_needed(self) -> None:
        if self.connection_monitor_thread and self.connection_monitor_thread.is_alive():
            return
        self.connection_monitor_thread = ConnectionMonitorThread(
            interface_manager=self.interface_manager,
            on_status=self._append_log,
            interval_s=2.0,
        )
        self.connection_monitor_thread.start()

    def _append_log(self, text: str) -> None:
        self.text_log.append(text)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainGui()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
