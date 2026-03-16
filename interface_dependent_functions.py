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
from wifi_interface_utils import (
    connect_to_interface as connect_to_wifi_interface,
    disconnect_interface_wifi,
    send_wifi_command,
    read_wifi_line,
    read_wifi_lines,
    read_wifi_decoded_line,
    read_wifi_response_end,
    is_active_wifi_online,
    monitor_wifi_disconnect_status,
)


def interface_is_online(active_comport, ssh_url, interface_in_use):
    if interface_in_use == 0:
        return is_active_comport_online(active_comport)
    else:
        return is_active_wifi_online(ssh_url)


def worker_run_interface_handle(
    ssh_url,
    interface_in_use,
    is_running,
    checked_both_without_hwusb,
    active_comport_used,
    active_com_port_used_for_rtcm,
    set_disconnected_status,
):
    if interface_in_use == 0:
        monitor_serial_disconnect_status(
            is_running=is_running,
            checked_both_without_hwusb=checked_both_without_hwusb,
            active_comport_used=active_comport_used,
            active_com_port_used_for_rtcm=active_com_port_used_for_rtcm,
            set_disconnected_status=set_disconnected_status,
        )
    else:
        print(f"Starting WiFi disconnect monitor for SSH URL: {ssh_url}")
        monitor_wifi_disconnect_status(
            is_running=is_running,
            ssh_url=ssh_url,
            set_disconnected_status=set_disconnected_status,
        )


def ensure_interface_disconnection_handle(ser, interface_in_use):
    if interface_in_use == 0:
        disconnect_interface(ser)
    else:
        disconnect_interface_wifi(ser)

def ensure_interface_connection_handle(
    ser,
    comport,
    baudrate,
    timeout_value,
    interface_in_use,
    show_disconnection_dialog,
    destroy_root,
    message_box_factory,
    open_after_disconnection,
    destroy_root_fn,
    warning_icon,
    ssh_url=None,
    ssh_password=None,
):
    if interface_in_use == 0:
        ser = connect_to_interface(ser, comport, baudrate, timeout_value)
        if ser is not None:
            return True, ser
        if show_disconnection_dialog:
            msg = message_box_factory()
            msg.setIcon(warning_icon)
            msg.setWindowTitle("Warning")
            msg.setText("COM port got disconnected!")
            msg.exec()
            if destroy_root:
                destroy_root_fn()
            open_after_disconnection()
        else:
            msg_box_2 = message_box_factory()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText("You cannot open this COM Port!")
            msg_box_2.exec()
        return False, ser
    else:
        ser, error_message = connect_to_wifi_interface(
            ser,
            ssh_url or "",
            ssh_password or "",
            timeout_value,
        )
        if ser is not None:
            print("WiFi SSH connection established successfully.")
            return True, ser

        msg_box = message_box_factory()
        if show_disconnection_dialog:
            msg_box.setIcon(warning_icon)
            msg_box.setWindowTitle("Warning")
            msg_box.setText(f"WiFi SSH connection failed: {error_message}")
            msg_box.exec()
            if destroy_root:
                destroy_root_fn()
            open_after_disconnection()
        else:
            msg_box.setWindowTitle("Error!")
            msg_box.setText(f"Unable to connect over WiFi SSH: {error_message}")
            msg_box.exec()
        return False, ser


def interface_check_handle(comport, wifi_interface_option, wifi_interface_option_2):
    global board_wifi
    if comport == wifi_interface_option or comport == wifi_interface_option_2:
        if comport == wifi_interface_option:
            print("Router WiFi")
            board_wifi = False
        elif comport == wifi_interface_option_2:
            print("Board WiFi")
            board_wifi = True
        return 1
    else:
        return 0


def read_decoded_line_interface_handle(ser, interface_in_use):
    if interface_in_use == 0:
        return read_serial_decoded_line(ser)
    else:
        return read_wifi_decoded_line(ser)


def read_response_end_interface_handle(
    ser,
    interface_in_use,
    file_path_to_read_response,
    get_current_datetime,
):
    if interface_in_use == 0:
        return read_serial_response_end(
            ser,
            file_path_to_read_response,
            get_current_datetime,
        )
    else:
        return read_wifi_response_end(
            ser,
            file_path_to_read_response,
            get_current_datetime,
        )

def send_command_interface_handle(command, ser, interface_in_use):
    if interface_in_use == 0:
        return send_serial_command(ser, command)
    else:
        return send_wifi_command(ser, command)

def read_lines_interface_handle(ser, interface_in_use):
    print(f"Reading lines from interface. Interface in use: {interface_in_use}")
    if interface_in_use == 0:
        return read_serial_lines(ser)
    else:
        return read_wifi_lines(ser)

def read_line_interface_handle(ser, interface_in_use):
    if interface_in_use == 0:
        return read_serial_line(ser)
    else:
        return read_wifi_line(ser)
