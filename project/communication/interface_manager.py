from __future__ import annotations

import serial

from project.communication.serial_interface import SerialInterface
from project.communication.wifi_interface import WifiSshInterface
from project.utils.message_utils import show_error
from project.utils.response_reader import add_end_marker


class InterfaceManager:
    INTERFACE_COM = "COM"
    INTERFACE_WIFI = "WIFI"

    def __init__(self, parent=None):
        self.parent = parent
        self.interface_type = self.INTERFACE_COM
        self.serial_backend = SerialInterface()
        self.wifi_backend = WifiSshInterface()

    @property
    def active_backend(self):
        return self.serial_backend if self.interface_type == self.INTERFACE_COM else self.wifi_backend

    def set_interface(
        self,
        interface_type: str,
        comport: str | None = None,
        baudrate: int | None = None,
        ssid: str | None = None,
        password: str | None = None,
    ) -> None:
        self.interface_type = interface_type
        if interface_type == self.INTERFACE_COM:
            self.serial_backend.set_interface(comport=comport or "", baudrate=baudrate)
        else:
            self.wifi_backend.set_interface(ssid=ssid or "", password=password or "")

    def connect_interface(self) -> bool:
        try:
            if self.interface_type == self.INTERFACE_WIFI:
                if not self.wifi_backend.connect_wifi():
                    show_error("WiFi is not connected.", parent=self.parent)
                    return False
                if not self.wifi_backend.connect_interface():
                    show_error("Unable to establish SSH connection.", parent=self.parent)
                    return False
                return True
            return self.serial_backend.connect_interface()
        except serial.SerialException:
            show_error("You cannot open this COM Port!", parent=self.parent)
            return False

    def disconnect_interface(self) -> None:
        self.active_backend.disconnect_interface()

    def reconnect_interface(self) -> bool:
        return self.active_backend.reconnect_interface()

    def check_connection(self) -> bool:
        return self.active_backend.check_connection()

    def send_command(self, command: str) -> None:
        self.active_backend.send_command(command)

    def read_response(self, timeout_s: float = 5.0, end_marker: str | None = None) -> list[str]:
        return self.active_backend.read_response(timeout_s=timeout_s, end_marker=end_marker)

    def send_command_and_read_until_end(self, command: str, end_marker: str = "END", timeout_s: float = 5.0) -> list[str]:
        self.send_command(add_end_marker(command, marker=end_marker))
        return self.read_response(timeout_s=timeout_s, end_marker=end_marker)

    def get_usb_info(self) -> list[str]:
        return self.active_backend.get_usb_info()
