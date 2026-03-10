import serial


class SerialInterface:
    """PySerial backend for GNSS board communication."""

    def __init__(self, port: str | None = None, baudrate: int | str = 115200, timeout: float = 1.0):
        self.port = port
        self.baudrate = int(baudrate) if baudrate is not None else 115200
        self.timeout = timeout
        self._serial: serial.Serial | None = None

    def configure(self, port: str, baudrate: int | str, timeout: float | None = None) -> None:
        self.port = port
        self.baudrate = int(baudrate)
        if timeout is not None:
            self.timeout = timeout

    def connect(self) -> bool:
        if self._serial and self._serial.is_open:
            return True
        if not self.port:
            return False
        self._serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        return self._serial.is_open

    def disconnect(self) -> None:
        if self._serial and self._serial.is_open:
            self._serial.close()

    def check_connection(self) -> bool:
        return bool(self._serial and self._serial.is_open)

    def reconnect(self) -> bool:
        self.disconnect()
        return self.connect()

    def send_command(self, command: bytes | str) -> int:
        if not self.check_connection():
            raise serial.SerialException("Serial interface is not connected")
        payload = command if isinstance(command, bytes) else command.encode("utf-8")
        return self._serial.write(payload)

    def read_response(self, size: int | None = None) -> bytes:
        if not self.check_connection():
            return b""
        if size:
            return self._serial.read(size)
        return self._serial.readline()

    def read_lines(self) -> list[bytes]:
        if not self.check_connection():
            return []
        return self._serial.readlines(self._serial.in_waiting)

    def read_until(self, marker: bytes) -> bytes:
        if not self.check_connection():
            return b""
        return self._serial.read_until(marker)

    def get_usb_info(self) -> str:
        self.send_command("lsusb ; (echo END) > /dev/null\n")
        return b"".join(self.read_lines()).decode("utf-8", errors="ignore")
