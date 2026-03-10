from __future__ import annotations

from communication.interface_manager import InterfaceManager


class ResponseReader:
    """Centralized response reading facade for all GUI/controllers."""

    def __init__(self, interface_manager: InterfaceManager) -> None:
        self.interface_manager = interface_manager

    def read_response(self) -> str:
        return self.interface_manager.read_response()
