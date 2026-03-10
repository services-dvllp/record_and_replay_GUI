from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional

import serial


@dataclass
class SerialConfig:
    port: str
    baudrate: int = 115200
    timeout: float = 1.0


class SerialInterface:
    """Encapsulates all pyserial operations for the GNSS board."""

    def __init__(self) -> None:
        self._ser: Optional[serial.Serial] = None
        self._config: Optional[SerialConfig] = None
        self._lock = threading.Lock()

    def configure(self, config: SerialConfig) -> None:
        self._config = config

    def connect(self) -> None:
        if not self._config:
            raise ValueError("Serial configuration is not set.")

        with self._lock:
            self.disconnect()
            self._ser = serial.Serial(
                self._config.port,
                self._config.baudrate,
                timeout=self._config.timeout,
            )

    def disconnect(self) -> None:
        with self._lock:
            if self._ser and self._ser.is_open:
                self._ser.close()
            self._ser = None

    def check_connection(self) -> bool:
        return bool(self._ser and self._ser.is_open)

    def reconnect(self) -> None:
        if not self._config:
            raise ValueError("Serial configuration is not set.")
        self.connect()

    def send_command(self, command: str) -> None:
        if not self.check_connection():
            raise ConnectionError("Serial interface is not connected.")
        payload = command.encode("utf-8")
        assert self._ser is not None
        self._ser.write(payload)

    def read_response(self, mode: str = "line", size: int = 4096) -> str:
        if not self.check_connection():
            raise ConnectionError("Serial interface is not connected.")

        assert self._ser is not None
        if mode == "line":
            data = self._ser.readline()
        elif mode == "all_lines":
            data = b"".join(self._ser.readlines())
        else:
            data = self._ser.read(size)
        return data.decode("utf-8", errors="ignore")

    def get_usb_info(self) -> str:
        self.send_command("lsusb\n")
        return self.read_response(mode="all_lines")
