class ResponseReader:
    def __init__(self, interface_manager):
        self.interface_manager = interface_manager

    def read_response(self):
        return self.interface_manager.read_response()

    def read_until_end(self):
        return self.interface_manager.read_response()
