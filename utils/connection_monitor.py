from __future__ import annotations

import threading
import time
from typing import Callable

from communication.interface_manager import InterfaceManager


class ConnectionMonitorThread(threading.Thread):
    """Background monitor that checks and reconnects the active interface."""

    def __init__(
        self,
        interface_manager: InterfaceManager,
        on_status: Callable[[str], None],
        interval_s: float = 2.0,
    ) -> None:
        super().__init__(daemon=True)
        self.interface_manager = interface_manager
        self.on_status = on_status
        self.interval_s = interval_s
        self._running = threading.Event()
        self._running.set()

    def run(self) -> None:
        while self._running.is_set():
            try:
                if not self.interface_manager.check_connection():
                    self.on_status("Connection lost. Attempting reconnection...")
                    self.interface_manager.reconnect_interface()
                    self.on_status("Reconnected successfully.")
            except Exception as exc:  # monitor must never crash UI
                self.on_status(f"Reconnection failed: {exc}")
            time.sleep(self.interval_s)

    def stop(self) -> None:
        self._running.clear()
