import subprocess
import time


class WifiInterface:
    """WiFi + SSH backend.

    Note: WiFi connect command is platform specific; this implementation uses Windows netsh.
    """

    def __init__(self, host: str = "192.168.4.1", user: str = "root"):
        self.host = host
        self.user = user
        self.ssh_process: subprocess.Popen | None = None
        self.ssid = ""
        self.password = ""

    def configure_wifi(self, ssid: str, password: str) -> None:
        self.ssid = ssid.strip()
        self.password = password

    def connect_wifi(self) -> bool:
        if not self.ssid:
            return False
        cmd = ["powershell", "-Command", f"netsh wlan connect name=\"{self.ssid}\""]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return False
        time.sleep(2)
        return True

    def connect(self) -> bool:
        if self.ssh_process and self.check_connection():
            return True
        self.ssh_process = subprocess.Popen(
            ["powershell", f"ssh {self.user}@{self.host}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        time.sleep(1)
        return self.check_connection()

    def disconnect(self) -> None:
        if self.ssh_process and self.ssh_process.poll() is None:
            try:
                self.ssh_process.stdin.write("exit\n")
                self.ssh_process.stdin.flush()
            except Exception:
                pass
            self.ssh_process.terminate()
        self.ssh_process = None

    def check_connection(self) -> bool:
        return bool(self.ssh_process and self.ssh_process.poll() is None)

    def reconnect(self) -> bool:
        self.disconnect()
        return self.connect()

    def send_command(self, command: bytes | str) -> int:
        if not self.check_connection() or not self.ssh_process.stdin:
            return 0
        cmd = command.decode("utf-8", errors="ignore") if isinstance(command, bytes) else command
        if not cmd.endswith("\n"):
            cmd += "\n"
        self.ssh_process.stdin.write(cmd)
        self.ssh_process.stdin.flush()
        return len(cmd)

    def read_response(self, timeout_s: float = 2.0) -> bytes:
        if not self.check_connection() or not self.ssh_process.stdout:
            return b""
        start = time.time()
        lines = []
        while time.time() - start < timeout_s:
            line = self.ssh_process.stdout.readline()
            if not line:
                break
            lines.append(line)
            if "END" in line or line.strip().endswith("#"):
                break
        return "".join(lines).encode("utf-8", errors="ignore")

    def read_until(self, marker: bytes) -> bytes:
        marker_s = marker.decode("utf-8", errors="ignore")
        data = self.read_response(timeout_s=3)
        return data if marker_s in data.decode("utf-8", errors="ignore") else b""

    def get_usb_info(self) -> str:
        self.send_command("lsusb ; echo END")
        return self.read_response().decode("utf-8", errors="ignore")
