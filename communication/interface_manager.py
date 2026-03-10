from __future__ import annotations

from communication.serial_interface import SerialInterface
from communication.wifi_interface import WifiInterface


class InterfaceManager:
    COM = "COM"
    WIFI = "WIFI"

    def __init__(self):
        self.interface_type = self.COM
        self.serial = SerialInterface()
        self.wifi = WifiInterface()

    @property
    def active(self):
        return self.wifi if self.interface_type == self.WIFI else self.serial

    def set_interface(self, interface_type: str, comport: str | None = None, baudrate: int | str | None = None,
                      ssid: str | None = None, password: str | None = None, timeout: float = 1.0):
        self.interface_type = interface_type
        if interface_type == self.COM:
            if comport and baudrate:
                self.serial.configure(comport, baudrate, timeout)
        else:
            self.wifi.configure_wifi(ssid or "", password or "")

    def connect_interface(self) -> bool:
        if self.interface_type == self.WIFI:
            if not self.wifi.connect_wifi():
                return False
            return self.wifi.connect()
        return self.serial.connect()

    def disconnect_interface(self) -> None:
        self.active.disconnect()

    def check_connection(self) -> bool:
        return self.active.check_connection()

    def send_command(self, command: bytes | str) -> int:
        return self.active.send_command(command)

    def read_response(self, *args, **kwargs) -> bytes:
        return self.active.read_response(*args, **kwargs)

    def reconnect_interface(self) -> bool:
        return self.active.reconnect()

    def get_usb_info(self) -> str:
        return self.active.get_usb_info()


class LegacyConnectionAdapter:
    """Serial-like adapter so old GUI code can use one object for both COM and WiFi."""

    def __init__(self, manager: InterfaceManager):
        self.manager = manager

    def isOpen(self):
        return self.manager.check_connection()

    @property
    def in_waiting(self):
        return 1

    def close(self):
        self.manager.disconnect_interface()

    def write(self, data):
        return self.manager.send_command(data)

    def read(self, size=1):
        return self.manager.read_response(size=size)

    def readline(self):
        return self.manager.read_response()

    def readlines(self, _=None):
        data = self.manager.read_response()
        return data.splitlines(keepends=True)

    def read_until(self, marker):
        active = self.manager.active
        if hasattr(active, "read_until"):
            return active.read_until(marker)
        return b""
