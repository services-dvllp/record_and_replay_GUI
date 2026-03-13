import serial
import time
from serial.tools import list_ports

def list_hardware_com_ports():
    ports = list_ports.comports()
    hardware_ports = []
    for port in ports:
        if (port.description and "USB" in port.description.upper()) or (port.hwid and "USB" in port.hwid.upper()):
            hardware_ports.append(port.device)
    return hardware_ports

def is_active_comport_online(active_comport):
    ports = list_hardware_com_ports()
    if active_comport in ports:
        return True
    else:
        return False

def monitor_serial_disconnect_status(
    is_running,
    checked_both_without_hwusb,
    active_comport_used,
    active_com_port_used_for_rtcm,
    set_disconnected_status,
    sleep_interval=0.5,
):
    while is_running():
        ports = list_hardware_com_ports()
        if checked_both_without_hwusb:
            if active_comport_used and active_com_port_used_for_rtcm in ports:
                set_disconnected_status(False)
            else:
                set_disconnected_status(True)
            time.sleep(sleep_interval)
        else:
            if active_comport_used in ports:
                set_disconnected_status(False)
            else:
                set_disconnected_status(True)
            time.sleep(sleep_interval)

def disconnect_interface(serial_connection):
    if serial_connection is not None and serial_connection.isOpen():
        serial_connection.close()

def connect_to_interface(serial_connection, comport, baudrate, timeout_value):
    disconnect_interface(serial_connection)
    try:
        return serial.Serial(comport, baudrate, timeout=timeout_value)
    except serial.SerialException:
        return None

def send_serial_command(serial_connection, command):
    print(f"Sending command to serial connection: {serial_connection}")
    if serial_connection is not None:
        return serial_connection.write(command)
    return None

def read_serial_lines(serial_connection):
    print(f"Reading lines from serial connection: {serial_connection}")
    if serial_connection is None:
        print("Serial connection is None, returning empty list.")
        return []
    serial_output = serial_connection.read(serial_connection.in_waiting)
    print(f"Serial output read: {serial_output}")
    return serial_output

def read_serial_line(serial_connection):
    if serial_connection is None:
        return []
    return serial_connection.readlines(1)

def read_serial_decoded_line(serial_connection):
    if serial_connection is None:
        return ""
    return serial_connection.readline().decode(errors='ignore')

def read_serial_response_end(serial_connection, file_path_to_read_response, current_datetime_func):
    if serial_connection is None:
        return
    print("Reading response until END...")
    response = serial_connection.read_until(b'END\r\n')
    response = response.replace(b'\r',b'')
    response = response.replace(b'ENND',b'END')
    print(f"res2:{response}\n\n\n")
    if b'END' not in response:
        return
    print("Reading response until #...")
    res2 = serial_connection.read_until(b'#')
    print(f"res3:{res2}\n\n")
    lines = response.splitlines(keepends=True) + [res2]

    with open(file_path_to_read_response, 'a') as file:
        file.write(f'\n{current_datetime_func()}   {lines}\n\n')

    return lines
