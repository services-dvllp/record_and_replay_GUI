from __future__ import annotations

from project.communication.interface_manager import InterfaceManager


class RecordController:
    def __init__(self, interface_manager: InterfaceManager):
        self.interface_manager = interface_manager

    def start_record(self, command: str) -> list[str]:
        return self.interface_manager.send_command_and_read_until_end(command)

    def stop_record(self, stop_command: str) -> list[str]:
        return self.interface_manager.send_command_and_read_until_end(stop_command)
