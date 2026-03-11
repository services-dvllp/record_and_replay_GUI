import serial


def disconnect_interface(serial_connection):
    if serial_connection is not None and serial_connection.isOpen():
        serial_connection.close()


def connect_to_interface(serial_connection, comport, baudrate, timeout_value):
    disconnect_interface(serial_connection)
    try:
        return serial.Serial(comport, baudrate, timeout=timeout_value)
    except serial.SerialException:
        return None


def send_serial_command(interface_in_use, serial_connection, command):
    if interface_in_use == 0 and serial_connection is not None:
        return serial_connection.write(command)
    return None
