# Refactoring Notes (v1.69 -> modular layout)

## New module tree

- `project/gui/main_gui.py`: GUI composition layer that keeps the legacy `Ui_MainWindow` widgets and routes communication via the abstraction.
- `project/communication/interface_manager.py`: backend routing and generic API.
- `project/communication/serial_interface.py`: serial backend implementation.
- `project/communication/wifi_interface.py`: WiFi/SSH backend implementation.
- `project/core/record_controller.py`: record business logic via interface manager.
- `project/core/replay_controller.py`: replay business logic via interface manager.
- `project/core/usb_info_controller.py`: USB info retrieval via active backend.
- `project/utils/connection_monitor.py`: interface-independent monitor thread.
- `project/utils/response_reader.py`: centralized response helpers.
- `project/utils/message_utils.py`: centralized message boxes.

## Mapping from old monolith patterns

- Repeated `serial.Serial(...)`, `ser.isOpen()`, `ser.close()` patterns -> `SerialInterface.connect_interface() / disconnect_interface() / reconnect_interface()`.
- COM/WiFi selection checks in GUI -> `InterfaceManager.set_interface()` with centralized routing.
- Scattered `ser.write(...)` and command echo marker logic -> `InterfaceManager.send_command_and_read_until_end()` + `utils.response_reader.add_end_marker()`.
- `read_Response_END`-style response loops -> `ResponseReader.read_until_end_marker()`.
- USB info from COM-only path -> `InterfaceManager.get_usb_info()` routed by active interface.
- COM-only connection polling -> `ConnectionMonitorThread` for COM/WiFi `check_connection()`.

## Integration assumptions

- Existing constants and widgets are preserved by loading the original `Ui_MainWindow` from `Record_and_Replay_v1.69.py`.
- WiFi setup uses a best-effort Windows `netsh wlan connect` command before opening SSH (`powershell ssh root@192.168.4.1`).
- Existing flows can migrate incrementally by replacing direct `ser` usage with `InterfaceManager` calls.
