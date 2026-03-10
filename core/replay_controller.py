from __future__ import annotations

from communication.interface_manager import InterfaceManager


class ReplayController:
    def __init__(self, interface_manager: InterfaceManager) -> None:
        self.interface_manager = interface_manager

    def start_replay(self, command: str) -> str:
        self.interface_manager.send_command(command)
        return self.interface_manager.read_response()

    def stop_replay(self, command: str = "stop") -> str:
        self.interface_manager.send_command(command)
        return self.interface_manager.read_response()
