# Refactor Mapping: `Record_and_Replay_v1.69.py` -> Modular Architecture

## New file tree

```text
project/
├── Record_and_Replay_v1.69.py
├── legacy/
│   └── Record_and_Replay_v1.69_legacy.py
├── gui/
│   ├── __init__.py
│   └── main_gui.py
├── communication/
│   ├── __init__.py
│   ├── interface_manager.py
│   ├── serial_interface.py
│   └── wifi_interface.py
├── core/
│   ├── __init__.py
│   ├── record_controller.py
│   ├── replay_controller.py
│   └── usb_info_controller.py
├── utils/
│   ├── __init__.py
│   ├── connection_monitor.py
│   └── response_reader.py
└── docs/
    └── refactor_mapping.md
```

## Responsibility mapping

| Legacy area | New module(s) |
|---|---|
| Global `ser` state, `send_command()`, repeated serial open/close checks | `communication/serial_interface.py` |
| New WiFi + SSH flow (`WiFi Interface` option, SSID/password, SSH shell) | `communication/wifi_interface.py` |
| Interface routing from GUI | `communication/interface_manager.py` |
| USB Info button backend handling | `core/usb_info_controller.py` |
| Record command flow | `core/record_controller.py` |
| Replay command flow | `core/replay_controller.py` |
| Repeated read logic (`readline/read/readlines`) centralization | `communication/interface_manager.py`, `utils/response_reader.py` |
| Connection health/reconnect loop | `utils/connection_monitor.py` |
| Submit button, dropdown selection, SSID/password widgets, popups | `gui/main_gui.py` |

## Specific legacy function mapping

| Legacy function (line) | New location |
|---|---|
| `send_command` (line ~192) | `InterfaceManager.send_command()`, with backend implementations in `SerialInterface.send_command()` and `WifiInterface.send_command()` |
| `list_hardware_com_ports` (line ~326) | GUI COM dropdown population responsibility in `main_gui.py` (can be extended with runtime serial enumeration) |
| `comport_is_On` / `comport_is_On_record_replay` (line ~335+) | `SerialInterface.check_connection()` and `InterfaceManager.check_connection()` |
| ad-hoc response parsing/reads scattered in class methods | `InterfaceManager.read_response()` + `ResponseReader.read_response()` |

## Assumptions

1. The original 3000+ line script remains available as `legacy/Record_and_Replay_v1.69_legacy.py` for behavior-by-behavior migration.
2. WiFi connection is OS-dependent; implementation supports Windows (`netsh`) and Linux (`nmcli`) command paths.
3. SSH is launched with PowerShell on Windows and native `ssh` on Linux.
4. GNSS command payloads are forwarded as plain text commands; command-specific parsing remains extendable in controllers.
5. Existing advanced UI flows from legacy code (all tabs and mode-specific operations) should be migrated incrementally into `core/*` while keeping communication decoupled.
