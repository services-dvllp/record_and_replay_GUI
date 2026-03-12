import socket
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import paramiko


@dataclass
class WifiSSHInterface:
    client: paramiko.SSHClient
    last_stdout_lines: List[bytes] = field(default_factory=list)
    last_stderr_lines: List[bytes] = field(default_factory=list)


def _parse_ssh_url(ssh_url: str) -> Tuple[Optional[str], str]:
    if "@" in ssh_url:
        username, host = ssh_url.split("@", 1)
        return username.strip() or None, host.strip()
    return None, ssh_url.strip()


def list_wifi_hosts():
    return []


def is_active_wifi_online(ssh_url, timeout_value=3):
    try:
        _, host = _parse_ssh_url(ssh_url)
        socket.create_connection((host, 22), timeout=timeout_value).close()
        return True
    except Exception:
        return False


def monitor_wifi_disconnect_status(
    is_running,
    ssh_url,
    set_disconnected_status,
    sleep_interval=0.5,
):
    import time

    while is_running():
        set_disconnected_status(not is_active_wifi_online(ssh_url))
        time.sleep(sleep_interval)


def disconnect_interface(wifi_connection):
    if wifi_connection is not None and getattr(wifi_connection, "client", None) is not None:
        wifi_connection.client.close()


def connect_to_interface(wifi_connection, ssh_url, ssh_password, timeout_value=10):
    disconnect_interface(wifi_connection)
    username_from_url, host = _parse_ssh_url(ssh_url)
    username = username_from_url or "root"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            host,
            username=username,
            password=ssh_password,
            timeout=timeout_value,
        )
        return WifiSSHInterface(client=ssh), None
    except paramiko.AuthenticationException:
        return None, "Authentication failed. Please verify SSH username/password."
    except socket.timeout:
        return None, "Connection timed out while reaching the WiFi host."
    except socket.gaierror:
        return None, "Hostname could not be resolved. Please verify ssh_url."
    except Exception as err:
        return None, str(err)


def send_wifi_command(wifi_connection, command):
    if wifi_connection is None:
        return None

    if isinstance(command, (bytes, bytearray)):
        command = command.decode(errors="ignore")

    stdin, stdout, stderr = wifi_connection.client.exec_command(command)
    _ = stdin

    wifi_connection.last_stdout_lines = stdout.readlines()
    wifi_connection.last_stderr_lines = stderr.readlines()
    return len(wifi_connection.last_stdout_lines)


def read_wifi_lines(wifi_connection):
    if wifi_connection is None:
        return []
    return wifi_connection.last_stdout_lines


def read_wifi_line(wifi_connection):
    if wifi_connection is None:
        return []
    return wifi_connection.last_stdout_lines[:1]


def read_wifi_decoded_line(wifi_connection):
    if wifi_connection is None:
        return ""
    if not wifi_connection.last_stdout_lines:
        return ""
    line = wifi_connection.last_stdout_lines[0]
    if isinstance(line, bytes):
        return line.decode(errors="ignore")
    return str(line)


def read_wifi_response_end(wifi_connection, file_path_to_read_response, current_datetime_func):
    if wifi_connection is None:
        return []

    lines = wifi_connection.last_stdout_lines
    with open(file_path_to_read_response, "a") as file:
        file.write(f"\n{current_datetime_func()}   {lines}\n\n")

    return lines
