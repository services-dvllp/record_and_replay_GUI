from __future__ import annotations

import threading
import time
from collections.abc import Callable

from project.communication.interface_manager import InterfaceManager


class ConnectionMonitorThread(threading.Thread):
    def __init__(
        self,
        interface_manager: InterfaceManager,
        on_disconnect: Callable[[], None],
        interval_s: float = 1.0,
    ):
        super().__init__(daemon=True)
        self.interface_manager = interface_manager
        self.on_disconnect = on_disconnect
        self.interval_s = interval_s
        self._running = threading.Event()
        self._running.set()

    def run(self) -> None:
        while self._running.is_set():
            if not self.interface_manager.check_connection():
                self.on_disconnect()
            time.sleep(self.interval_s)

    def stop(self) -> None:
        self._running.clear()
