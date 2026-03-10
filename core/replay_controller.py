class ReplayController:
    def __init__(self, interface_manager):
        self.interface_manager = interface_manager

    def start_replay(self, command: str):
        self.interface_manager.send_command(command)
        return self.interface_manager.read_response()
