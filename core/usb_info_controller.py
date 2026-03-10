class UsbInfoController:
    def __init__(self, interface_manager):
        self.interface_manager = interface_manager

    def get_usb_info(self) -> str:
        return self.interface_manager.get_usb_info()
