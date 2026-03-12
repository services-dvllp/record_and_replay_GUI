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


def interface_is_online(active_comport, interface_in_use):
    if interface_in_use == 0:
        return is_active_comport_online(active_comport)
    else:
        print("wifi")


def worker_run_interface_handle(
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
        print("wifi")


def ensure_interface_disconnection_handle(ser, interface_in_use):
    if interface_in_use == 0:
        disconnect_interface(ser)
    else:
        print("wifi")


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
        print("wifi")


def interface_check_handle(comport, wifi_interface_option):
    if comport == wifi_interface_option:
        return 1
    else:
        return 0


def read_decoded_line_interface_handle(ser, interface_in_use):
    if interface_in_use == 0:
        return read_serial_decoded_line(ser)
    else:
        print("Wifi")


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
        print("Wifi")

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
