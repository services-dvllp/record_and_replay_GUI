from __future__ import annotations

import subprocess

from project.utils.response_reader import ResponseReader


class WifiSshInterface:
    def __init__(self, host: str = "root@192.168.4.1"):
        self.ssid: str = ""
        self.password: str = ""
        self.host = host
        self._ssh_process: subprocess.Popen[str] | None = None
        self.reader = ResponseReader(self._readline)

    def set_interface(self, ssid: str, password: str) -> None:
        self.ssid = ssid
        self.password = password

    def connect_wifi(self) -> bool:
        """Best-effort Windows profile connect. Returns True when command succeeds."""
        if not self.ssid:
            return False
        cmd = ["powershell", "-Command", f'netsh wlan connect name="{self.ssid}"']
        if self.password:
            # Password can be preconfigured in profile; command remains best-effort.
            pass
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

    def connect_interface(self) -> bool:
        self.disconnect_interface()
        self._ssh_process = subprocess.Popen(
            ["powershell", "ssh root@192.168.4.1"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return self.check_connection()

    def disconnect_interface(self) -> None:
        if self._ssh_process and self._ssh_process.poll() is None:
            self._ssh_process.terminate()
            try:
                self._ssh_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._ssh_process.kill()
        self._ssh_process = None

    def reconnect_interface(self) -> bool:
        return self.connect_interface()

    def check_connection(self) -> bool:
        return bool(self._ssh_process and self._ssh_process.poll() is None)

    def send_command(self, command: str) -> None:
        if not self.check_connection() or not self._ssh_process or not self._ssh_process.stdin:
            raise RuntimeError("SSH connection is not active")
        self._ssh_process.stdin.write(command.rstrip("\n") + "\n")
        self._ssh_process.stdin.flush()

    def _readline(self) -> str:
        if not self._ssh_process or not self._ssh_process.stdout:
            return ""
        return self._ssh_process.stdout.readline()

    def read_response(self, timeout_s: float = 5.0, end_marker: str | None = None) -> list[str]:
        if end_marker:
            return self.reader.read_until_end_marker(end_marker=end_marker, timeout_s=timeout_s)
        return self.reader.read_available()

    def get_usb_info(self) -> list[str]:
        self.send_command("lsusb")
        return self.read_response(timeout_s=3.0)
