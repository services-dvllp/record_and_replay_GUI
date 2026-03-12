from serial_interface_utils import (
    connect_to_interface,
    disconnect_interface,
    send_serial_command,
    read_serial_line,
    read_serial_lines,
    read_serial_decoded_line,
    read_serial_response_end,
    list_hardware_com_ports,
    is_active_comport_online,
    monitor_serial_disconnect_status,
)

def send_command_interface_handle(command, ser, interface_in_use):
    if interface_in_use == 0:
        return send_serial_command(ser, command)
    else:
        print("send wifi command")

def read_lines_interface_handle(ser, interface_in_use):
    if interface_in_use == 0:
        return read_serial_lines(ser)
    else:
        print("read wifi lines")

def read_line_interface_handle(ser, interface_in_use):
    if interface_in_use == 0:
        return read_serial_line(ser)
    else:
        print("read wifi line")