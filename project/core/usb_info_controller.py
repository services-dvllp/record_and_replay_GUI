from __future__ import annotations

from project.communication.interface_manager import InterfaceManager


class UsbInfoController:
    def __init__(self, interface_manager: InterfaceManager):
        self.interface_manager = interface_manager

    def get_usb_info(self) -> list[str]:
        return self.interface_manager.get_usb_info()
