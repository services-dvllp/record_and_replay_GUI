import threading
import time


class ConnectionMonitorThread(threading.Thread):
    def __init__(self, interface_manager, on_disconnect=None, interval_s: float = 2.0):
        super().__init__(daemon=True)
        self.interface_manager = interface_manager
        self.on_disconnect = on_disconnect
        self.interval_s = interval_s
        self._running = True

    def run(self):
        while self._running:
            if not self.interface_manager.check_connection():
                reconnected = self.interface_manager.reconnect_interface()
                if not reconnected and self.on_disconnect:
                    self.on_disconnect()
            time.sleep(self.interval_s)

    def stop(self):
        self._running = False
