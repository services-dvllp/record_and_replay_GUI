from __future__ import annotations

import time
from typing import Callable, Iterable


class ResponseReader:
    """Unified command-response helpers shared by COM and WiFi backends."""

    def __init__(self, read_line: Callable[[], str], flush_input: Callable[[], None] | None = None):
        self._read_line = read_line
        self._flush_input = flush_input

    def flush_input(self) -> None:
        if self._flush_input:
            self._flush_input()

    def read_available(self, max_lines: int = 1000) -> list[str]:
        lines: list[str] = []
        for _ in range(max_lines):
            line = self._read_line()
            if not line:
                break
            lines.append(line)
        return lines

    def read_until_end_marker(
        self,
        end_marker: str = "END",
        timeout_s: float = 5.0,
        include_marker: bool = False,
    ) -> list[str]:
        deadline = time.time() + timeout_s
        lines: list[str] = []
        while time.time() < deadline:
            line = self._read_line()
            if not line:
                time.sleep(0.02)
                continue
            clean = line.strip("\r\n")
            if clean == end_marker:
                if include_marker:
                    lines.append(clean)
                break
            lines.append(clean)
        return lines



def add_end_marker(command: str, marker: str = "END") -> str:
    command = command.rstrip("\n")
    return f"{command} ; echo {marker} > /dev/null"
