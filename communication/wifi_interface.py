from __future__ import annotations

import platform
import subprocess
import threading
from dataclasses import dataclass
from typing import Optional


@dataclass
class WifiConfig:
    ssid: str
    password: str
    host: str = "192.168.4.1"
    username: str = "root"


class WifiInterface:
    """Handles WiFi association + interactive SSH command channel."""

    def __init__(self) -> None:
        self._config: Optional[WifiConfig] = None
        self._ssh_process: Optional[subprocess.Popen[str]] = None
        self._lock = threading.Lock()

    def configure(self, config: WifiConfig) -> None:
        self._config = config

    def connect_wifi(self) -> bool:
        if not self._config:
            raise ValueError("WiFi configuration is not set.")

        system = platform.system().lower()
        if "windows" in system:
            # Requires an existing WLAN profile for SSID in most environments.
            cmd = ["netsh", "wlan", "connect", f"name={self._config.ssid}"]
        elif "linux" in system:
            cmd = ["nmcli", "dev", "wifi", "connect", self._config.ssid, "password", self._config.password]
        else:
            return False

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    def connect_ssh(self) -> None:
        if not self._config:
            raise ValueError("WiFi configuration is not set.")

        with self._lock:
            self.disconnect()
            target = f"{self._config.username}@{self._config.host}"
            if "windows" in platform.system().lower():
                cmd = ["powershell", "-Command", f"ssh {target}"]
            else:
                cmd = ["ssh", target]

            self._ssh_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

    def connect(self) -> None:
        if not self.connect_wifi():
            raise ConnectionError("WiFi is not connected.")
        self.connect_ssh()
        if not self.check_connection():
            raise ConnectionError("Unable to establish SSH connection.")

    def disconnect(self) -> None:
        with self._lock:
            if self._ssh_process:
                self._ssh_process.terminate()
                self._ssh_process = None

    def check_connection(self) -> bool:
        if not self._ssh_process:
            return False
        return self._ssh_process.poll() is None

    def reconnect(self) -> None:
        self.connect()

    def send_command(self, command: str) -> None:
        if not self.check_connection():
            raise ConnectionError("SSH interface is not connected.")
        assert self._ssh_process and self._ssh_process.stdin
        self._ssh_process.stdin.write(command + "\n")
        self._ssh_process.stdin.flush()

    def read_response(self) -> str:
        if not self.check_connection():
            raise ConnectionError("SSH interface is not connected.")
        assert self._ssh_process and self._ssh_process.stdout
        line = self._ssh_process.stdout.readline()
        return line or ""

    def get_usb_info(self) -> str:
        self.send_command("lsusb")
        return self.read_response()
