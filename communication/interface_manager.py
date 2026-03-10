from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from communication.serial_interface import SerialConfig, SerialInterface
from communication.wifi_interface import WifiConfig, WifiInterface


class InterfaceType(str, Enum):
    COM = "COM"
    WIFI = "WIFI"


@dataclass
class InterfaceSelection:
    interface_type: InterfaceType
    comport: Optional[str] = None
    baudrate: int = 115200
    timeout: float = 1.0
    ssid: str = ""
    password: str = ""


class InterfaceManager:
    """Single entry point used by GUI/controllers; routes to active backend."""

    def __init__(self) -> None:
        self._serial = SerialInterface()
        self._wifi = WifiInterface()
        self._active_type: InterfaceType = InterfaceType.COM

    def set_interface(self, selection: InterfaceSelection) -> None:
        self._active_type = selection.interface_type
        if selection.interface_type == InterfaceType.COM:
            if not selection.comport:
                raise ValueError("COM port is required for COM interface.")
            self._serial.configure(
                SerialConfig(
                    port=selection.comport,
                    baudrate=selection.baudrate,
                    timeout=selection.timeout,
                )
            )
        else:
            self._wifi.configure(
                WifiConfig(ssid=selection.ssid, password=selection.password)
            )

    def _backend(self):
        return self._serial if self._active_type == InterfaceType.COM else self._wifi

    def connect_interface(self) -> None:
        self._backend().connect()

    def disconnect_interface(self) -> None:
        self._backend().disconnect()

    def check_connection(self) -> bool:
        return self._backend().check_connection()

    def reconnect_interface(self) -> None:
        self._backend().reconnect()

    def send_command(self, command: str) -> None:
        self._backend().send_command(command)

    def read_response(self) -> str:
        backend = self._backend()
        if self._active_type == InterfaceType.COM:
            return backend.read_response(mode="line")
        return backend.read_response()

    def get_usb_info(self) -> str:
        return self._backend().get_usb_info()

    @property
    def active_type(self) -> InterfaceType:
        return self._active_type
