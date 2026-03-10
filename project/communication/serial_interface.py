from __future__ import annotations

import serial

from project.utils.response_reader import ResponseReader


class SerialInterface:
    def __init__(self, baudrate: int = 115200, timeout: float = 1.0):
        self.comport: str | None = None
        self.baudrate = baudrate
        self.timeout = timeout
        self._serial: serial.Serial | None = None
        self.reader = ResponseReader(self._readline, self.flush_input)

    def set_interface(self, comport: str, baudrate: int | None = None, timeout: float | None = None) -> None:
        self.comport = comport
        if baudrate is not None:
            self.baudrate = int(baudrate)
        if timeout is not None:
            self.timeout = timeout

    def connect_interface(self) -> bool:
        self.disconnect_interface()
        if not self.comport:
            return False
        self._serial = serial.Serial(self.comport, self.baudrate, timeout=self.timeout)
        return True

    def disconnect_interface(self) -> None:
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._serial = None

    def reconnect_interface(self) -> bool:
        return self.connect_interface()

    def check_connection(self) -> bool:
        return bool(self._serial and self._serial.is_open)

    def send_command(self, command: str) -> None:
        if not self.check_connection():
            raise serial.SerialException("Serial interface is not connected")
        if not command.endswith("\n"):
            command += "\n"
        self._serial.write(command.encode())
        self._serial.flush()

    def _readline(self) -> str:
        if not self.check_connection():
            return ""
        data = self._serial.readline()
        return data.decode(errors="ignore") if data else ""

    def read_response(self, timeout_s: float = 5.0, end_marker: str | None = None) -> list[str]:
        if end_marker:
            return self.reader.read_until_end_marker(end_marker=end_marker, timeout_s=timeout_s)
        return self.reader.read_available()

    def flush_input(self) -> None:
        if self.check_connection():
            self._serial.reset_input_buffer()

    def get_usb_info(self) -> list[str]:
        self.send_command("lsusb")
        return self.read_response(timeout_s=3.0)
