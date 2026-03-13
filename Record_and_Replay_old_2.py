import os
import re
import sys
import math
import time
import datetime
import threading
#from datetime import datetime
import serial
import serial.tools.list_ports
from serial.tools import list_ports
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
from wifi_interface_utils import connect_to_interface as connect_to_wifi_interface
from interface_dependent_functions import (
    send_command_interface_handle,
    #read_lines_interface_handle,
    #read_line_interface_handle,
    interface_is_online as interface_is_online_handle,
    worker_run_interface_handle,
    ensure_interface_disconnection_handle,
    ensure_interface_connection_handle,
    interface_check_handle,
    #read_decoded_line_interface_handle,
    read_response_end_interface_handle,
)

from PIL import Image, ImageTk
from pyubx2 import UBXReader

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTime, QTimer, QSize, QThread
from PyQt6.QtGui import QPixmap, QIcon, QFont, QPainter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog,
    QLabel, QVBoxLayout, QWidget, QMessageBox, QDialog, QComboBox
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt

ssh_username = "root"
ssh_fixed_url = f"{ssh_username}@192.168.4.1"
ssh_password = "root"
active_com_port_used_for_rtcm = None
ssh_url = None
########## User and Developer Code ############
Commands_file_user = True
browse_folder_for_HWUSB = False
browse_file_for_HWUSB = False
############ Variables #########
bandwidth = None
Sampling_frequency = None
log_duration = None
log_duration_2 = None
bits_2 = None
bandwidth_2 = None
Sampling_frequency_2 = None
bits = None
center_frequency = None
center_frequency_2 = None
ser = None
ser_rtcm = None
lo_value_1 = None
lo_value_2 = None
root_gui = None
comport = ""
previous_port = []
current_port = ""
previous_port_rtcm = []
current_port_rtcm = ""
RTCM_ports = False
non_rtcm_ports = False
root_create_popup = False
timeout_time = 1
SSD_free_space = None
HW_USB_in_use = False
HW_USB_Size = 2000000000
#################################
folder_HW_USB = ""
version = "Version - 1.69"                     #The GUI version
file_name_command = "Commands.txt"             #File name that logs the commands
file_name_response = "Response.txt"
filename_txt = "selected_files.txt"            # File name to track selected files for replay via switches
nvmelabel_file = "nvme_label.txt"
read_selected_file_path = "/home/root/adc4bits/HW_files/"        #Directory of the filename_txt
base_path = "/run/media/"                      #Initial path
fs_system = "/dev/"
executable_rx = "nice --20 /home/root/adc4bits/libiio/build/examples/guirx"
executable_rx_fixed = "nice --20 /home/root/adc4bits/libiio/build/examples/guirx"
executable_tx = "nice --20 /home/root/adc4bits/libiio/build/examples/guitx"
executable_tx_fixed = "nice --20 /home/root/adc4bits/libiio/build/examples/guitx"
col = "#2"
col_title = "Rx 1"
Lg_path = ""
folder_name = ""
reboot_command = "sudo reboot\n"
shutdown_command = "sudo reboot => shutdown -r now\n"
current_path = base_path
available_memory = 0
file_count = 0
current_count = 0
file_count_variable = 1
count_one = 0
count_one_replay = 0
count_seconds = 0
developer_executable_rx = "nice --20 /home/root/adc4bits/libiio/build/examples/guirx"
developer_executable_tx = "nice --20 /home/root/adc4bits/libiio/build/examples/guitx"
click_count = 0
line_tx_rx_count = 0
active_comport_used = ""
wifi_interface_selected = False
default_gain_rx = "Slow attack"
default_gain_tx = "-20"
previous_data = b""
nvmelabel_lebel_txt = ""
filename = ""
pdf_path = r"GNSS_Record_Replay_Usermanual.pdf"
disconnect_HW_USB_record_replay = "killall RTCMrx RTCMtx"
device_id = ""
bus_no = ""
log_file_size = 1000000 #1MB
satellite_clicks = 5 #satellite clicks to move to developer mode
WIFI_INTERFACE_OPTION = "Router WiFi"
WIFI_INTERFACE_OPTION_2 = "Board WiFi"
############ Flags ####################
center_frequency_flag = False
center_frequency_flag_2 = False
bandwidthflag = False
Sampling_frequency_flags = False
log_durationflags = False
bits_flags = False
bandwidthflag_2 = False
Sampling_frequency_flags_2 = False
bits_flags_2 = False
back_btn_clicked = False
comport_connected = False
recording_started = False
replay_started = False
refile = False
browse_files = False
browse_folder = False
submitted = False
created_new_file = False
config_button = False
config_browse_file = False
deleting_on_progress = False
delete_gui = False
file_name_starts_with_dot = False
submit_btn_clicked = True
Edit_btn_clicked = False
hide_path_btn_active = False
hide_path_btn_active_rtcm = False
show_path_btn_active = True
show_path_btn_active_rtcm = True
hide_path_btn_active_replay = False
show_path_btn_active_replay = True
dual_channel_in_Replay = False
nvme_label_found = True
record_tab = False
replay_tab = False
nolog_high = False
selected_inside_folder = False
gui_opened = False
back_from_nolog = False
boot = False
match_timer = False
rx1_checked = True
rx2_checked = False
rtcm_folder_name = ""
rtcm_folder_path = ""
rtcm_file_name = ""
rtcm_file_path= ""
ad9361_checked = True
rtcm_checked = False
checked_both_without_HWUSB = False
only_rtcm = True
only_ad9361 = False
show_path_btn_active_replay_rtcm = True
hide_path_btn_active_replay_rtcm = False
single_channel_rx1_replay = False
Dual_channel_replay = False
single_channel_rx2_replay = False
developer_rx_tx = False
recorded_time = False
replayed_time = False
disconnected_comport_while_recording_replaying = False
flag_raised_for_stop_Recording = False
usb_button_flag = False
################################################################################
recording_dual_channel = False
recording_rx1_channel = False
recording_rx2_channel = False
check_flag = False
flag_raised = False

no_adc_4_bits = False
no_HW_files = False
no_nvme_label = False
no_selected_files = False
read_response = True
terminated = False
read_Replay_response = True
replay_terminated = False
check_comport = True
present = False

comport_1_checked = False
comport_2_checked = False
main_func_called = False
###############################################################################
###############################################################################
def send_command(command):
    send_command_interface_handle(command, ser, interface_in_use)

def read_lines():
    if interface_in_use == 0:
        return read_serial_lines(ser)
    else:
        return read_wifi_lines(ser)

def read_line():
    if interface_in_use == 0:
        return read_serial_line(ser)
    else:
        return read_wifi_line(ser)

###############################################################################
###############################################################################
def read_serial_lines(serial_connection):
    if serial_connection is None:
        return []
    serial_output = serial_connection.read(serial_connection.in_waiting)
    return serial_output

def read_serial_line(serial_connection):
    if serial_connection is None:
        return []
    return serial_connection.readlines(1)

def read_serial_decoded_line(serial_connection):
    if serial_connection is None:
        return ""
    return serial_connection.readline().decode(errors='ignore')

def read_wifi_lines(wifi_connection):
    print(f"wifi connection: {wifi_connection}")
    if wifi_connection is None:
        return []
    lines =  wifi_connection.last_stdout_lines
    encoded_lines = [line.encode() if isinstance(line, str) else line for line in lines]
    return encoded_lines

def read_wifi_line(wifi_connection):
    if wifi_connection is None:
        return []
    lines = wifi_connection.last_stdout_lines[:1]
    encoded_lines = [line.encode() if isinstance(line, str) else line for line in lines]
    return encoded_lines

def read_wifi_decoded_line(wifi_connection):
    if wifi_connection is None:
        print("wifi connection is None")
        return ""
    if not wifi_connection.last_stdout_lines:
        print("No lines in wifi connection")
        return ""
    line = wifi_connection.last_stdout_lines
    print(f"line: {line}")
    return line
    """if isinstance(line, bytes):
        x = line.decode(errors="ignore")
        print(f"decoded line: {x}")
        return line.decode(errors="ignore")"""
###############################################################################
###############################################################################

####################### Get the Current Date and Time ##########################
def get_current_datetime():
    timestamp = time.time()
    # Constants for time conversions
    seconds_per_day = 24 * 60 * 60
    seconds_per_hour = 60 * 60
    seconds_per_minute = 60
    # Calculate days, hours, minutes, and seconds
    days_since_epoch = int(timestamp / seconds_per_day)
    remainder = timestamp % seconds_per_day
    hours = int(remainder / seconds_per_hour)
    remainder %= seconds_per_hour
    minutes = int(remainder / seconds_per_minute)
    seconds = int(remainder % seconds_per_minute)
    # Get the current date in YYYY-MM-DD format
    current_time_struct = time.localtime(timestamp)
    date = time.strftime("%Y-%m-%d", current_time_struct)
    # Combine the date with the time in the desired format
    start_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    start_time_in_format = f"{date}_{hours:02d}:{minutes:02d}:{seconds:02d}"
    #print(start_time_in_format)
    return start_time_in_format

def extract_sections_folder(lines):
    directories = []
    section = None  # track which section we are in
    for line in lines:
        line = line.strip()
        if line == "=== Directories ===":
            section = "dirs"
            continue
        if line == "--- Done listing directories ---":
            section = None
            continue
        if section == "dirs" and line:
            directories.append(f"{line}")
    return directories
################################################################################
def extract_sections(lines):
    only_directory = False
    directories = []
    bin_files = []
    rtcm_files = []
    section = None  # track which section we are in
    
    for line in lines:
        line = line.strip()
        print(f"line: {line}")
        if "Mode: dirs" in line:
            print("Mode: dirs")
            only_directory = True
        if line == "=== Directories ===":
            section = "dirs"
            continue
        if line == "--- Done listing directories ---":
            section = None
            continue
        if line == "=== .bin Files ===":
            section = "bins"
            continue
        if line == "--- Done listing .bin files ---":
            section = None
            continue
        if line == "=== .rtcm Files ===":
            section = "rtcms"
            continue
        if line == "--- Done listing .rtcm files ---":
            section = None
            continue
        if section == "dirs" and line:
            if (only_directory): directories.append(f"{line}")
            else: directories.append(f"(d)  {line}")
        elif section == "bins" and line:
            bin_files.append(line)
        elif section == "rtcms" and line:
            rtcm_files.append(line)

    print(f"directories: {directories}")
    print(f"bin_files: {bin_files}")
    print(f"rtcm_files: {rtcm_files}")
    if browse_file_for_HWUSB:
        return directories, rtcm_files
    else:
        return directories, bin_files
################################################################################

date_time = get_current_datetime()
date = date_time.split("_")[0]
start_time = date_time.split("_")[1]

######################## Commands will be logged into a file ####################
if Commands_file_user:
    # Determine the Downloads directory path
    # Base Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    # Create a subfolder "debug_RR" inside Downloads
    debug_folder = os.path.join(downloads_path, "debug_RR")
    os.makedirs(debug_folder, exist_ok=True)  # Create folder if it doesn't exist

    # File paths inside debug_RR
    file_path = os.path.join(debug_folder, file_name_command)
    file_path_to_read_response = os.path.join(debug_folder, file_name_response)
    files_to_write = [file_path, file_path_to_read_response]
    for file_paths in files_to_write:
        if os.path.exists(file_paths):
            file_size = os.path.getsize(file_paths)
            if file_size > 10 * 1024 * 1024:  # 10MB
                with open(file_paths, 'rb') as file:
                    # Seek to the last 1MB of the file
                    file.seek(file_size - 1 * 1024 * 1024)
                    last_1mb = file.read()
                
                # Write only the last 1MB back to the file
                with open(file_paths, 'wb') as file:
                    file.write(last_1mb)
        else:
            with open(file_paths, 'w') as file:
                #file.write("************************************************")
                file.write("****************  Opened GUI  ******************")
                file.write(f"\nDate: {date}\nTime: {start_time}\n\n")
                created_new_file = True

        if not created_new_file:
            created_new_file = False
            with open(file_paths, 'a') as file:
                file.write("************************************************")
                file.write("\n\n****************  Opened GUI  ******************")
                file.write(f"\nDate: {date}\nTime: {start_time}\n\n")

##################################################################################
def interface_is_online(active_comport):
    return interface_is_online_handle(active_comport, ssh_url, interface_in_use)
    
def interface_is_onlineRTCM(active_comport):
    ports = list_hardware_com_ports()
    if active_comport in ports:
        return True
    else:
        return False

def comport_is_On_record_replay(active_comport):
    global disconnected_comport_while_recording_replaying
    if interface_in_use == 0:
        while True:
            ports = list_hardware_com_ports()
            if active_comport in ports:
                disconnected_comport_while_recording_replaying = False
                print(ports)
            else:
                disconnected_comport_while_recording_replaying = True
                print("error")
            time.sleep(1)
    else:
        print("wifi")
###################### Verify file name and folder name ##########################
def validate_file_and_folder_name_linux(file_name):
    global file_name_starts_with_dot
    # Define the invalid characters and control characters for Linux
    invalid_chars = r'[\/\x00-\x1F]'  # Includes forward slash and ASCII control characters
    # Rule 1: Check for invalid characters
    if re.search(invalid_chars, file_name):
        return False, "File name contains invalid characters: forward slash (/) or control characters."  
    if file_name.strip() != file_name:
        return False, "File name cannot have leading or trailing spaces."  
    if len(file_name) > 255:
        return False, "File name exceeds the maximum length of 255 characters."   
    special_chars = r'[*? ]'  # Include special characters like '*', '?', and spaces
    if re.search(special_chars, file_name):
        return False, "File name should not contain special characters like '*', '?', or spaces."
    if file_name.startswith('.'):
        file_name_starts_with_dot = True
        print("Warning: File name starts with a dot (.) and will be hidden.")
    return True, "File name is valid."

############################ Validate the Time ###################################
# The set of functions that used to get the time in HH:MM:SS format
def second_to_hhmmss(seconds):
    if not type(seconds) == int:
        seconds = int(seconds)  # Convert seconds to an integer
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)

def minutes_to_hhmmss(mm_ss):
    # Split the input into minutes and seconds
    minutes, seconds = map(int, mm_ss.split(':'))
    # Calculate hours from minutes
    hours = minutes // 60
    remaining_minutes = minutes % 60
    # Format the time as HH:MM:SS
    hh_mm_ss = f"{hours:02}:{remaining_minutes:02}:{seconds:02}"
    return hh_mm_ss

def validate_time(string_time):
    parts = string_time.split(":")
    try:
        parts = [int(part) for part in parts]  # Convert all parts to integers
    except ValueError:
        return None

    if len(parts) == 1:  # Only seconds provided
        seconds = parts[0]
        if seconds <= 59:
            return f"00:00:{seconds:02}"
        return second_to_hhmmss(seconds)

    elif len(parts) == 2:  # Minutes and seconds provided
        minutes, seconds = parts
        if seconds >= 60:
            return None
        if minutes <= 59:
            return f"00:{minutes:02}:{seconds:02}"
        return minutes_to_hhmmss(f"{minutes}:{seconds}")

    elif len(parts) == 3:  # Hours, minutes, and seconds provided
        hours, minutes, seconds = parts
        if minutes >= 60 or seconds >= 60:
            return None
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    return None  # Invalid format if more than 3 parts

####################################### Time Conversion #########################################
# This function is used to substract two times in HH:MM:SS and return the differance in Seconds #
def subtract_two_times(time1, time2):
    def time_to_seconds(time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    def seconds_to_time(seconds):
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    total_seconds = time_to_seconds(time1) - time_to_seconds(time2)
    # Handle negative results by converting to positive duration if needed
    if total_seconds < 0:
        total_seconds = abs(total_seconds)
    return seconds_to_time(total_seconds)

#Function used to convert time into seconds
def time_to_seconds(time_str):
    # Split the input string into hours, minutes, and seconds
    h, m, s = map(int, time_str.split(':'))
    # Convert the time to seconds
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds

def compare_times(time_str1, time_str2):
    """Compare two time strings in HH:MM:SS format."""
    seconds1 = time_to_seconds(time_str1)
    seconds2 = time_to_seconds(time_str2)
    
    if seconds1 < seconds2:
        return f"{time_str1} is earlier than {time_str2}"
    elif seconds1 > seconds2:
        return f"{time_str1} is later than {time_str2}"
    else:
        return f"{time_str1} is the same as {time_str2}"
    
#The function that Adds two times
def add_two_times(time1, time2):
    def time_to_seconds(time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
    
    def seconds_to_time(seconds):
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    total_seconds = time_to_seconds(time1) + time_to_seconds(time2)
    return seconds_to_time(total_seconds)
#####################################################################################
def convert_size(size_bytes):
    print(f"size_bytes: {size_bytes}")
    if size_bytes == None:
        return "Not found"
    if size_bytes == 0:
        return "0B"
    
    size_units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_units) - 1:
        size_bytes /= 1024.0
        i += 1
    
    #return f"{size_bytes:.2f} {size_units[i]}"
    return f"{int(size_bytes)} {size_units[i]}"

#File_system_pth = "/dev/nvme0n1p1" 
def parse_df_output(output):
    filesystems = []
    for line in output[1:-1]:
        ld = line.decode();
        print(ld)
        parts = ld.split()
        if len(parts) >= 6:
            filesystem = {
                'filesystem': parts[0],
                'size': parts[1],
                'used': parts[2],
                'avail': parts[3],
                'use_percent': parts[4],
                'mounted_on': parts[5]
            }
            filesystems.append(filesystem)
            print(f"filesystem: {filesystems}")        
    return filesystems

def get_available_space(filesystem,output):
    filesystems = parse_df_output(output)
    print(f"filesystems2: {filesystems}")
    for fs in filesystems:
        print(f"fs {fs}")
        if fs['filesystem'] == filesystem:
            avail = int(fs['avail']) * 1024  # Convert to bytes
            print(f"available : {avail}")
            return avail
    return None
#####################################################################################
def get_memory_available(fs_system):
    print(fs_system)
    global ser
    ########################################################
    bss = read_lines()
    #########################################################
    #########################################################
    send_command(bytearray('df\n','ascii'))
    if Commands_file_user:
        with open(file_path, 'a') as file:
            file.write(f'{get_current_datetime()}   df\n')
    # time.sleep(1) 
    bs = read_lines()
    print(bs)
    if Commands_file_user:
                            with open(file_path_to_read_response, 'a') as file:
                                file.write(f'{get_current_datetime()} :Response for df')
                                file.write(f'\n{get_current_datetime()}   {bs}\n\n')
    memavil = get_available_space(fs_system,bs)
    print(memavil)
    if Commands_file_user:
                            with open(file_path_to_read_response, 'a') as file:
                                file.write(f'{get_current_datetime()} :Available space')
                                file.write(f'\n{get_current_datetime()}   {memavil}\n\n')
    #print("Available space on {}: {} bytes".format(fs_system, memavil)) 
    #memavil = 5*60*5e6*4
    return memavil

def memory_check_for_rx_log_2(mem_avail_bytes, lg_time_s, Sampling_frequency_record_1, ADC_bits_1, Sampling_frequency_record_2, ADC_bits_2):
        #Sampling_frequency = 5e6
        Bytes_perSample_1 = (ADC_bits_1*2)/8
        bytes_req_1 = lg_time_s * Sampling_frequency_record_1 * Bytes_perSample_1
        mem_avail_time = lg_time_s

        Bytes_perSample_2 = (ADC_bits_2*2)/8
        bytes_req_2 = lg_time_s * Sampling_frequency_record_2 * Bytes_perSample_2
        mem_avail_time = lg_time_s
        bytes_req = int(bytes_req_1 + bytes_req_2)
        print(bytes_req)
        print(mem_avail_bytes)

        if mem_avail_bytes is None:
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Oops!\nResponse not received within the timeout, please retry!\n\nPlease check the NVME label/ Connections and baudrate")
            msg_box_11.exec()
            mem_avail_time = 0
            mem_avail_bytes = int(bytes_req_1 + bytes_req_2)+ 10
            #return  

        if (bytes_req*file_count_variable) > mem_avail_bytes:
            # Calculate available time based on memory
            mem_avail_time = math.floor(mem_avail_bytes / (Sampling_frequency_record_1 * Bytes_perSample_1))
            mem_avail_time = math.floor(mem_avail_time/2)
            mem_avail_time = math.floor(mem_avail_time/file_count_variable)

            msg_box_compare = QMessageBox()
            msg_box_compare.setWindowTitle("Memory Warning")
            msg_box_compare.setText("Memory available for only {}.".format(second_to_hhmmss(mem_avail_time)))
            #msg_box_compare.setInformativeText("You have exceeded the available memory, Do you want to log within the available memory?")
            msg_box_compare.setIcon(QMessageBox.Icon.Warning)
            msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
            msg_box_compare.addButton(QMessageBox.StandardButton.No)
            msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
            reply_3 = msg_box_compare.exec()

            # Check the user's choice
            if reply_3 == QMessageBox.StandardButton.Yes:
                print("Logging within available memory...")
            else:
                # User chose not to log within available memory
                print("Logging not performed.")
                mem_avail_time = 0

        return mem_avail_time
##########################################################################################################
def memory_check_for_rx_log(mem_avail_bytes, lg_time_s, Sampling_frequency_record_1, ADC_bits_1):
        #Sampling_frequency = 5e6
        Bytes_perSample_1 = (ADC_bits_1*2)/8
        bytes_req_1 = lg_time_s * (Sampling_frequency_record_1) * (Bytes_perSample_1)
        mem_avail_time = lg_time_s

        if mem_avail_bytes is None:
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Oops!\nResponse not received within the timeout, please retry!\n\nPlease check the NVME label/ Connections and baudrate")
            msg_box_11.exec()
            mem_avail_time = 0
            mem_avail_bytes = int(bytes_req_1) + 10
            #return      
        
        print(bytes_req_1)
        print(mem_avail_bytes)

        if int(bytes_req_1*file_count_variable) > mem_avail_bytes:
            mem_avail_time = math.floor(mem_avail_bytes / (Sampling_frequency_record_1 * Bytes_perSample_1))
            if int(mem_avail_time) == 0:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Size error")
                msg_box_11.setText(f"No space left!")
                msg_box_11.exec()
                return
            
            # Calculate available time based on memory
            #mem_avail_time = math.floor(mem_avail_bytes / (Sampling_frequency_record * Bytes_perSample))
            mem_avail_time = math.floor(mem_avail_time/file_count_variable)
            msg_box_compare = QMessageBox()
            msg_box_compare.setWindowTitle("Memory Warning")
            msg_box_compare.setText("Memory available for only {}.".format(second_to_hhmmss(mem_avail_time)))
            msg_box_compare.setInformativeText("Do you want to log within the available memory?")
            msg_box_compare.setIcon(QMessageBox.Icon.Warning)
            msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
            msg_box_compare.addButton(QMessageBox.StandardButton.No)
            msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
            reply_3 = msg_box_compare.exec()

            # Check the user's choice
            if reply_3 == QMessageBox.StandardButton.Yes:
                print("Logging within available memory...")
            else:
                # User chose not to log within available memory
                print("Logging not performed.")
                mem_avail_time = 0

        return mem_avail_time

def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

######################################################################################################
def check_value_lo(value):
    value_1 = float(value)
    value = float(f"{value}e6")
    if not (70e6 < value < 6e9):
        value_1 = None
        print("error")
    return value_1


def check_command(string):
    return f'"{string}"'

def filename_txt_string_editor(string):
    string = str(string).split("/")
    string = "\/".join(string)
    return string

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

import socket
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import paramiko


@dataclass
class WifiSSHInterface:
    client: paramiko.SSHClient
    last_stdout_lines: List[bytes] = field(default_factory=list)
    last_stderr_lines: List[bytes] = field(default_factory=list)

def _parse_ssh_url(ssh_url: str) -> Tuple[Optional[str], str]:
    if "@" in ssh_url:
        username, host = ssh_url.split("@", 1)
        return username.strip() or None, host.strip()
    return None, ssh_url.strip()

def is_active_wifi_online(ssh_url, timeout_value=3):
    try:
        print(f"Checking WiFi host connectivity for {ssh_url}...")
        _, host = _parse_ssh_url(ssh_url)
        socket.create_connection((host, 22), timeout=timeout_value).close()
        print(f"Host {host} is reachable on port 22.")
        return True
    except Exception:
        print(f"Host {host} is not reachable on port 22.")
        return False
    
def monitor_wifi_disconnect_status(
    is_running,
    ssh_url,
    set_disconnected_status,
    sleep_interval=0.5,
):
    import time

    while is_running():
        set_disconnected_status(not is_active_wifi_online(ssh_url))
        #set_disconnected_status(False)
        time.sleep(sleep_interval)
#######################################################################################################
class Worker(QThread):
    def __init__(self):
        super().__init__()
        self.running = True  # Flag to control the thread's loop
    def run(self):
        global disconnected_comport_while_recording_replaying
        # Infinite loop controlled by `self.running`
        if interface_in_use == 0:
            monitor_serial_disconnect_status(
                is_running=lambda: self.running,
                checked_both_without_hwusb=checked_both_without_HWUSB,
                active_comport_used=active_comport_used,
                active_com_port_used_for_rtcm=active_com_port_used_for_rtcm,
                set_disconnected_status=lambda value: globals().__setitem__(
                    "disconnected_comport_while_recording_replaying", value
                ),
            )
        else:
            print(f"Starting WiFi disconnect monitor for SSH URL: {ssh_url}")
            monitor_wifi_disconnect_status(
                is_running=lambda: self.running,
                ssh_url=ssh_url,
                set_disconnected_status=lambda value: globals().__setitem__(
                    "disconnected_comport_while_recording_replaying", value
                ),
            )

        
        """worker_run_interface_handle(
            ssh_url=ssh_url,    
            interface_in_use=interface_in_use,
            is_running=lambda: self.running,
            checked_both_without_hwusb=checked_both_without_HWUSB,
            active_comport_used=active_comport_used,
            active_com_port_used_for_rtcm=active_com_port_used_for_rtcm,
            set_disconnected_status=lambda value: globals().__setitem__(
                "disconnected_comport_while_recording_replaying", value
            ),
        )"""
    def stop(self):
        self.running = False  # Set flag to stop the loop
#############################################################################################################
class Ui_SecondWindow(object):
    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(200, 100)
        SecondWindow.setWindowTitle("Second Window")
        SecondWindow.setStyleSheet("background-color: white; color: black;")  # Dark background with white text
        # Set window flags to remove decorations
        SecondWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # Create a central widget and set it as the main widget
        central_widget = QtWidgets.QWidget(SecondWindow)
        SecondWindow.setCentralWidget(central_widget)
        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        # Create the label
        self.label = QtWidgets.QLabel("Deleting...", central_widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Add the label to the layout
        layout.addWidget(self.label)
        # Center the label within the window
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
###########################################################################################################
class Ui_MainWindow(object):
    def GPIO_record_replay(self, *args):
        # Unpack arguments
        result = None
        print(f"args: {args}")
        pathforfile_folder = args[0]
        file_foldername = args[1]
        durationforlog = args[2]
        start_offset_replay = args[3]
        print(f"pathforfile_folder: {pathforfile_folder}")
        print(f"file_foldername: {file_foldername}")
        print(f"durationforlog: {durationforlog}")
        print(f"start_offset_replay: {start_offset_replay}")
        try:
            autoplayreplay = args[4]
            print(f"autoplayreplay: {autoplayreplay}")
        except IndexError:
            autoplayreplay = False
        print(f"{autoplayreplay}")
        global ser
        test = False
        if not test:
            if record_tab:
                if self.radioButton_GPIO_Record.isChecked():
                    print("GPIO Record is selected")
                    xyz = f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR record {pathforfile_folder}{file_foldername} {int(durationforlog)+1} > {pathforfile_folder}{file_foldername}log 2>&1 &"
                    send_command(bytearray(f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR record {pathforfile_folder}{file_foldername} {int(durationforlog)+1} > {pathforfile_folder}{file_foldername}log 2>&1 &\n", 'ascii'))
                    with open(file_path, 'a') as file:
                        file.write(f'\n{xyz}\n')
            if replay_tab:
                if self.radioButton_GPIO_Replay.isChecked():
                    if autoplayreplay == False:
                        send_command(bytearray(f"chmod +x /home/root/adc4bits/libiio/gpio_check.sh; /home/root/adc4bits/libiio/gpio_check.sh {pathforfile_folder}{file_foldername}; (echo END) > /dev/null\n", 'ascii'))
                        x = f"chmod +x /home/root/adc4bits/libiio/gpio_check.sh {pathforfile_folder}{file_foldername}; (echo END) > /dev/null"
                        with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {x}\n')
                        lines = self.read_Response_END()  # Call the function
                        if lines is None:
                            result = 0
                            return result
                        print(lines)
                        decoded_lines = [line.decode() for line in lines]
                        print(decoded_lines)
                        for line in decoded_lines:
                            if "File exists:" in line:
                                result = 1
                            elif "File not found:" in line:
                                result = 2
                        #print(f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR replay {pathforfile_folder}{file_foldername} {int(durationforlog)+1} {start_offset_replay}&")
                    else:
                        result = 1
                    if result == 1:
                        send_command(bytearray(f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR replay {pathforfile_folder}{file_foldername} {int(durationforlog)+1} {start_offset_replay}&\n", 'ascii'))
                        x = f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR replay {pathforfile_folder}{file_foldername} {int(durationforlog)+1} {start_offset_replay}&"
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   {x}\n')
        return result
    
    def stop_GPIO_record_replay(self):
        global ser
        send_command(bytearray(f'killall -9 GPIO_RR\n', 'ascii'))
        with open(file_path, 'a') as file:
            file.write(f'\n{get_current_datetime()}   killall -9 GPIO_RR\n')
        print("Stopping GPIO Record/Replay")

    def populate_table(self):
        global deleting_on_progress
        # Clear the table first
        self.table_widget.clearContents()
        
        # Populate the table with variables and delete buttons
        for i in range(7):
            if i < len(self.variable_names):
                variable_name = self.variable_names[i]
            elif i < 4:
                variable_name = "Not Selected"
            else:
                variable_name = "Reserved"

            item = QtWidgets.QTableWidgetItem(variable_name)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(i, 0, item)

            delete_button = QtWidgets.QPushButton("Remove")
            delete_button.clicked.connect(lambda checked, row=i: self.remove_variable(row))

            # Disable the button if the row is "Reserved"
            if variable_name == "Reserved":
                delete_button.setEnabled(False)

            self.table_widget.setCellWidget(i, 1, delete_button)
            if deleting_on_progress:
                 #self.close_second_window()
                 deleting_on_progress = False

    def show_popup_table(self, item):
        global root
        def on_close():
            global root, config_browse_file
            config_browse_file = False
            root.destroy()

        global current_path, ser, config_browse_file, file_path

        text = item.text()
        print(text)
        if text == "Reserved":
             return
        if not text == "Not Selected" and not config_browse_file:
                    global filename, params_table, proceed_button, back_to_files, response, decoded_lines, label1, filename_1
                    filename = str(str(text))
                    for line in selected_files_paths:
                        if filename in line:
                            file_path_of_file = str(line).strip()
                     
                    comport_is_active = interface_is_online(self.comport)
                    actual_directory = check_command(file_path_of_file)
                    actual_filename = check_command(filename)
                    if comport_is_active: 
                        send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --mode contents --file {actual_directory}.log; (echo END) > /dev/null\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --mode contents --file {actual_directory}.log; (echo END) > /dev/null\n')
                            lines = self.read_Response_END()  # Call the function
                            if lines is None:
                                    messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                                    return
                            decoded_lines = [line.decode() for line in lines]
                            print(decoded_lines)
                        else:
                            messagebox.showwarning("Warning", "COM port got disconnected!")
                            root.destroy()
                            self.open_after_disconnection()
                            return
                        
                        error_in_file_path = False
                        for line in decoded_lines:
                            if "Error" in line:
                                error_in_file_path = True
                    
                    if not error_in_file_path:
                        import tkinter as tk
                        from tkinter import ttk, simpledialog, messagebox                                        
                        import serial, time
                        root = tk.Tk()
                        root.title("Parameters")
                        root.minsize(500, 400)
                        #root.geometry("500x450")
                        root.resizable(True, False)
                        # Load the image using Pillow (PIL)
                        icon_image = Image.open("green_satellite_small.png")  # Replace with your image path
                        icon_photo = ImageTk.PhotoImage(icon_image)

                        # Set the image as the window icon6
                        root.iconphoto(False, icon_photo)
                        # Set window to be resizable
                        root.grid_columnconfigure(0, weight=1)
                        root.grid_rowconfigure(0, weight=1)
                        #root.geometry("500x500")
                        config_browse_file = True

                        main_frame = tk.Frame(root)
                        main_frame.pack(padx=10, pady=10)
                        label1 = tk.Label(root, text=f" File name: {text} ", foreground="green")
                        label1.pack(pady=10)
                                                    
                        def main(filename):
                            global log_duration_2,reference_Frequency_log, center_frequency_2, gainfile_2, gainfile_1, center_frequency, center_frequency_flag, center_frequency_flag_2, filename_1, bandwidth, bits_flags_2, bandwidth_2, back_to_files, Sampling_frequency,bandwidthflag_2,Sampling_frequency_flags_2, Sampling_frequency_2, bits_2 , log_duration, bits, bandwidthflag, Sampling_frequency_flags, log_durationflags, bits_flags, filename_1, total_bytes
                            filename = f'{filename}'
                            print(filename)
                            #if filename in resp:
                            filename_1 = filename.split(".log")[0]
                            print(filename_1)
                            ##print(decoded_lines)
                            log_duration = ""
                            center_frequency = ""
                            center_frequency_2 = ""
                            Sampling_frequency = ""
                            Sampling_frequency_2 = ""
                            bits = ""
                            bits_2 = ""
                            log_duration_2 = ""
                            bandwidth = ""
                            bandwidth_2 = ""
                            gainfile_1 = ""
                            gainfile_2 = ""
                            reference_Frequency_log = ""
                            mode_in_file = ""

                            for line in decoded_lines:
                                #print(f"line: {line}")
                                if "LO1 " in line:
                                    if "not found" in line:
                                        center_frequency = "Not found"
                                    else:
                                        center_frequency = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "LO2 " in line:
                                    if "not found" in line:
                                        center_frequency_2 = "Not found"
                                    else:
                                        #print(f"center_frequency_2: {line}")   
                                        center_frequency_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "Bandwidth1 " in line:
                                    if "not found" in line:  
                                        bandwidth = "Not found"
                                    else: 
                                        bandwidth = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "Bandwidth2 " in line:
                                    if "not found" in line:
                                        bandwidth_2 = "Not found"
                                    else:
                                        bandwidth_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "fSamp1 " in line:
                                    if "not found" in line:
                                        Sampling_frequency = "Not found"    
                                    else:
                                        #print(f"Sampling_frequency: {line}")
                                        Sampling_frequency = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "fSamp2 " in line:
                                    if "not found" in line:
                                        Sampling_frequency_2 = "Not found"
                                    else:
                                        #print(f"Sampling_frequency_2: {line}")
                                        Sampling_frequency_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                elif "ADC Bits1 " in line:
                                    #print(f"ADC Bits1: {line}")
                                    if "not found" in line:
                                        bits = "Not found"
                                    else:
                                        #print(f"bits: {line}")
                                        bits = line.split(":")[-1].strip().split(" ")[0].strip()
                                elif "ADC Bits2 " in line:
                                    if "not found" in line:
                                        bits_2 = "Not found"
                                    else:
                                        #print(f"bits_2: {line}")
                                        bits_2 = line.split(":")[-1].strip().split(" ")[0].strip()
                                elif "Total .bin File Size "  in line:
                                        if "not found" in line:
                                            total_bytes = "Not found"
                                        else:
                                            total_bytes = line.split(":")[-1].strip().split(" ")[0].strip()
                                            total_bytes = math.floor(int(total_bytes)-512)
                                elif "Gain2 " in line:
                                    if "not found" in line:
                                       gainfile_2 = "Not found"
                                    else:
                                        gainfile_2 = str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                elif "Gain1 " in line:
                                    if "not found" in line:
                                        gainfile_1 = "Not found"
                                    else:
                                        gainfile_1 = str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                elif "Gain1 " in line: 
                                    if not "not found" in line:
                                        gainfile_2 =  str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                    else:
                                        gainfile_2 = "Not found"
                                elif "Mode " in line:
                                    mode_in_file = int(line.split(":")[-1].strip())
                                    #print(f"mode_in_file: {mode_in_file}")
                                                    
                            if mode_in_file == "":
                                    log_duration = "Not found"
                                    log_duration_2 = "Not found"
                            if mode_in_file == 0:
                                    bytes_per_sample = ((int(bits)*2)/8)
                                    bytes_per_second = bytes_per_sample*Sampling_frequency
                                    log_duration = int((int(total_bytes) / int(bytes_per_second))/1000000)
                                    log_duration_2 = "Not found"
                            elif mode_in_file == 4:
                                    bytes_per_sample = ((int(bits_2)*2)/8)
                                    bytes_per_second = bytes_per_sample*Sampling_frequency_2
                                    log_duration_2 = int((int(total_bytes) / int(bytes_per_second))/1000000)
                                    log_duration = "Not found"
                            elif mode_in_file == 2:
                                    bytes_per_sample = ((int(bits)*2)/8)
                                    bytes_per_second = bytes_per_sample*Sampling_frequency
                                    log_duration_2 = int(int((int(total_bytes) / int(bytes_per_second))/1000000)/2)
                                    log_duration = log_duration_2
                            if reference_Frequency_log == "":
                                        reference_Frequency_log = "Not found"
                            
                            try:
                                duration = second_to_hhmmss(log_duration)
                            except:
                                duration =  log_duration

                            try:
                                duration_2 = second_to_hhmmss(log_duration_2)
                            except:
                                duration_2 =  log_duration_2

                            update_gui(bandwidth, Sampling_frequency, duration, duration_2, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2, gainfile_1, gainfile_2)

                        def update_gui(bandwidth, Sampling_frequency, log_duration, log_duration_2, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2, gainfile_1, gainfile_2):
                            params_table_3.insert("", tk.END, values=("Center Freq (MHz)", center_frequency, center_frequency_2), tags=("oddrow",))
                            params_table_3.insert("", tk.END, values=("#ADC Bits", bits, bits_2), tags=("evenrow",))
                            params_table_3.insert("", tk.END, values=("Bandwidth (MHz)", bandwidth, bandwidth_2), tags=("oddrow",))
                            params_table_3.insert("", tk.END, values=("Gain (dB)", gainfile_1, gainfile_2), tags=("evenrow",))
                            params_table_3.insert("", tk.END, values=("Sampling Freq (MHz)", Sampling_frequency, Sampling_frequency_2), tags=("oddrow",))
                            params_table_3.insert("", tk.END, values=("Log Duration", log_duration, log_duration_2), tags=("evenrow",))
                            params_table_3.insert("", tk.END, values=("Reference Freq (MHz)", reference_Frequency_log, reference_Frequency_log), tags=("oddrow",))

                        # Create a Treeview to display the parameters in a table with reduced size and alternating row colors
                        columns = ("Parameter", "Value1", "Value2")
                        params_table_3 = ttk.Treeview(root, columns=columns, show="headings", height=7)
                        params_table_3.heading("Parameter", text="Parameter")
                        params_table_3.heading("Value1", text="Rx 1")
                        params_table_3.heading("Value2", text="Rx 2")
                        params_table_3.column("Parameter", anchor="w", width=150)
                        params_table_3.column("Value1", anchor="w", width=150)
                        params_table_3.column("Value2", anchor="w", width=150)
                        params_table_3.pack(pady=20)
                        #params_table_3.pack(pady=(root.winfo_height() // 2 - params_table_3.winfo_height() // 2))             
                        # Apply styles for gridlines and alternating row colors
                        style = ttk.Style()
                        style.configure("Treeview", rowheight=45)
                        style.map("Treeview", background=[("selected", "#ececec")], foreground=[("selected", "black")])
                        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
                        params_table_3.tag_configure("oddrow", background="lightgreen")
                        params_table_3.tag_configure("evenrow", background="white")
                        root.protocol("WM_DELETE_WINDOW", on_close)
                        # Call the main function to process the file and update the GUI
                        main(filename)
                        
                        root.mainloop()

                    else:
                        file_ = f"{actual_filename.split(".log")[0]}.bin"
                        if comport_is_active:
                            send_command(bytearray(f'[ -f "{file_}" ] && echo "File exists." || echo "File does not exist."\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   [ -f "{file_}" ] && echo "File exists." || echo "File does not exist."\n')
                            lines = read_lines()
                            print(lines)
                            decoded_lines = [line.decode() for line in lines]
                            print(decoded_lines)
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return

                        if decoded_lines[-2] == "File does not exist.":
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error")
                            msg_box_11.setText(f"No such file or directory found!\nDirectory:{directory}")
                            msg_box_11.exec()
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Info")
                            msg_box_11.setText(f"No .log file found do display the parameters!")
                            msg_box_11.exec()

                                          
    def remove_variable(self, row):
        global ser, deleting_on_progress
        if not deleting_on_progress and not delete_gui:
            current_path_ = read_selected_file_path
            # Delete the variable only if it's not "Not Selected"
            if row < len(self.variable_names):
                file_name_needs_to_deleted = (self.variable_names[row])
                print(f"the file that needs to be deleted: {file_name_needs_to_deleted}")
                msg_box_delete = QMessageBox()
                msg_box_delete.setWindowTitle("Confirmation!")
                msg_box_delete.setText("Are you sure you want to remove this file?")
                #msg_box_delete.setInformativeText("Do you want to log within the available memory?")
                msg_box_delete.setIcon(QMessageBox.Icon.Warning)
                msg_box_delete.addButton(QMessageBox.StandardButton.Yes)
                msg_box_delete.addButton(QMessageBox.StandardButton.No)
                msg_box_delete.setDefaultButton(QMessageBox.StandardButton.Yes)
                reply_3 = msg_box_delete.exec()
                # Check the user's choice
                if reply_3 == QMessageBox.StandardButton.Yes:
                    deleting_on_progress = True
                    def edit_file_delete():
                        global ser, deleting_on_progress
                    #############################################################################
                        count=0
                        self.pushButton_browse_config.setEnabled(False)
                        self.pushButton_refresh_config.setEnabled(False)
                        self.pushButton_2.setEnabled(False)
                        self.pushButton_4.setEnabled(False)
                        self.pushButton_5.setEnabled(False)
                        self.pushButton_login.setEnabled(False)
                        self.fs_system_edit_btn.setEnabled(False)
                        self.fs_system_submit_btn.setEnabled(False)
                        self.label_fs_system_display.setEnabled(False)
                        #############################################################################
                        comport_is_active = interface_is_online(self.comport)
                        command = check_command(current_path_)
                        if comport_is_active:
                            send_command(bytearray(f'cd {command}\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'{get_current_datetime()}   cd {command}\n')
                            lines = read_lines()
                        else:
                            deleting_on_progress = False
                            self.pushButton_browse_config.setEnabled(True)
                            self.pushButton_refresh_config.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            self.fs_system_edit_btn.setEnabled(True)
                            self.fs_system_submit_btn.setEnabled(True)
                            self.label_fs_system_display.setEnabled(True)    
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"Comport disconnected could not remove the file")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        comport_is_active = interface_is_online(self.comport)
                        actual_filename = check_command(filename_txt)
                        
                        if comport_is_active:
                            send_command(bytearray(f'cat {actual_filename} ; (echo END) > /dev/null\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   cat {actual_filename} ; (echo END) > /dev/null\n')
                            lines = self.read_Response_END()  # Call the function
                            print(f"lines: {lines}")
                            if lines is None:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                                msg_box_11.exec()
                                return  # Stop execution
                        else:
                            deleting_on_progress = False
                            self.pushButton_browse_config.setEnabled(True)
                            self.pushButton_refresh_config.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            self.fs_system_edit_btn.setEnabled(True)
                            self.fs_system_submit_btn.setEnabled(True)
                            self.label_fs_system_display.setEnabled(True)
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"Comport disconnected could not remove the file")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        
                        if "null" in str(lines[1]):
                            print("null")
                            lines = lines[2:-2]
                        else:
                             lines = lines[1:-2]    
                        print(f"lines: {lines}")
                        decoded_lines = [line.decode() for line in lines]
                        print(f"decoded_lines: {decoded_lines}")
                        for line in decoded_lines:
                            print(line)
                            count += 1
                            print(f"count: {count}")
                            print(f"file_name_needs_to_deleted: {file_name_needs_to_deleted}")
                            print(f"line: {line}")
                            if file_name_needs_to_deleted in line:
                                #############################################################################
                                comport_is_active = interface_is_online(self.comport)
                                command = check_command(current_path_)
                                if comport_is_active:
                                    send_command(bytearray(f'cd {command}\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   cd {command}\n')
                                else:
                                    deleting_on_progress = False
                                    self.pushButton_browse_config.setEnabled(True)
                                    self.pushButton_refresh_config.setEnabled(True)
                                    self.pushButton_2.setEnabled(True)
                                    self.pushButton_4.setEnabled(True)
                                    self.pushButton_5.setEnabled(True)
                                    self.pushButton_login.setEnabled(True)
                                    self.fs_system_edit_btn.setEnabled(True)
                                    self.fs_system_submit_btn.setEnabled(True)
                                    self.label_fs_system_display.setEnabled(True)
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"Comport disconnected could not remove the file")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                comport_is_active = interface_is_online(self.comport)
                                actual_filename = check_command(filename_txt)
                                if comport_is_active:
                                    send_command(bytearray(f'sed -i "{count}d" {actual_filename} ; (echo END) > /dev/null\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   sed -i "{count}d" {actual_filename} ; (echo END) > /dev/null\n')
                                    response = self.read_Response_END()  # Call the function
                                    print(f"response: {response}")
                                else:
                                    deleting_on_progress = False
                                    self.pushButton_browse_config.setEnabled(True)
                                    self.pushButton_refresh_config.setEnabled(True)
                                    self.pushButton_2.setEnabled(True)
                                    self.pushButton_4.setEnabled(True)
                                    self.pushButton_5.setEnabled(True)
                                    self.pushButton_login.setEnabled(True)
                                    self.fs_system_edit_btn.setEnabled(True)
                                    self.fs_system_submit_btn.setEnabled(True)
                                    self.label_fs_system_display.setEnabled(True)
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"Comport disconnected could not remove the file")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active:
                                    send_command(bytearray(f'sed -i "/^$/d" {actual_filename} ; (echo END) > /dev/null\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   sed -i "/^$/d" {actual_filename} ; (echo END) > /dev/null\n')
                                    response = self.read_Response_END()  # Call the function
                                    print(f"response: {response}")
                                else:
                                    deleting_on_progress = False
                                    self.pushButton_browse_config.setEnabled(True)
                                    self.pushButton_refresh_config.setEnabled(True)
                                    self.pushButton_2.setEnabled(True)
                                    self.pushButton_4.setEnabled(True)
                                    self.pushButton_5.setEnabled(True)
                                    self.pushButton_login.setEnabled(True)
                                    self.fs_system_edit_btn.setEnabled(True)
                                    self.fs_system_submit_btn.setEnabled(True)
                                    self.label_fs_system_display.setEnabled(True)
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"COM port got disconnected!")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                
                                deleting_on_progress = False
                                self.pushButton_browse_config.setEnabled(True)
                                self.pushButton_refresh_config.setEnabled(True)
                                self.pushButton_2.setEnabled(True)
                                self.pushButton_4.setEnabled(True)
                                self.pushButton_5.setEnabled(True)
                                self.pushButton_login.setEnabled(True)
                                self.fs_system_edit_btn.setEnabled(True)
                                self.fs_system_submit_btn.setEnabled(True)
                                self.label_fs_system_display.setEnabled(True)
                    #self.open_second_window()
                    edit_file_delete()
                    #threading.Thread(target=edit_file_delete).start()
                    
                    del self.variable_names[row]
            self.populate_table()

    def update_baud_rates_rtcm(self):
        baud_rates = [38400, 9600, 19200, 57600, 230400, 460800, 921600]
        self.comboBox_baudrate_rtcm.clear()
        self.comboBox_baudrate_rtcm.addItem("115200")  # Add the placeholder item
        for baud_rate in baud_rates:
            self.comboBox_baudrate_rtcm.addItem(str(baud_rate))

    def update_ref_freq(self):
        reference_Frequencies = ["40MHz (External)", "25MHz (RFMD)"]
        self.comboBox_ref_freq.clear()
        self.comboBox_ref_freq.addItem("AD9361 (single CH)")  # Add the placeholder item
        for frequency in reference_Frequencies:
            self.comboBox_ref_freq.addItem(str(frequency))

    def update_baud_rates(self):
        baud_rates = [9600, 19200, 38400, 57600, 230400, 460800, 921600]
        self.comboBox_baudrate.clear()
        self.comboBox_baudrate.addItem("115200")  # Add the placeholder item
        for baud_rate in baud_rates:
            self.comboBox_baudrate.addItem(str(baud_rate))

    def update_com_ports_rtcm(self):
        global previous_port_rtcm, present_rtcm, RTCM_ports
        present_rtcm = False
        RTCM_ports = False
        ports = list_ports.comports()
        #self.comboBox_comport_rtcm.clear()
        #self.comboBox_comport_rtcm.addItem("Select Port")

        # Filter hardware-connected COM ports
        hardware_ports = [port.device for port in ports
                        if (port.description and "USB" in port.description.upper()) or
                        (port.hwid and "USB" in port.hwid.upper())]

        # Add hardware-connected COM ports to the combobo
        if not hardware_ports == previous_port_rtcm:
            self.comboBox_comport_rtcm.clear()
            self.comboBox_comport_rtcm.addItem("Select Port")
            self.comboBox_comport_rtcm.addItem("HW USB")
            RTCM_ports = True
            for port in hardware_ports:
                if port == current_port_rtcm:
                    present_rtcm = True
                self.comboBox_comport_rtcm.addItem(port)
        
        previous_port_rtcm = hardware_ports
        print(present_rtcm)

    def update_com_ports(self):
        global previous_port, present, non_rtcm_ports
        print("helloo")
        present = False
        non_rtcm_ports = False
        ports = list_ports.comports()
        #if comport == "Select Port" or comport == "":
        # Filter hardware-connected COM ports
        hardware_ports = [port.device for port in ports
                        if (port.description and "USB" in port.description.upper()) or
                        (port.hwid and "USB" in port.hwid.upper())]
        # Add hardware-connected COM ports to the combobox
        if not hardware_ports == previous_port:
            self.comboBox_comport.clear()
            self.comboBox_comport.addItem("Select Port")
            self.comboBox_comport.addItem(WIFI_INTERFACE_OPTION)
            self.comboBox_comport.addItem(WIFI_INTERFACE_OPTION_2)
            non_rtcm_ports = True
            for port in hardware_ports:
                if port == current_port:
                    present = True
                self.comboBox_comport.addItem(port)
        previous_port = hardware_ports
        self.update_wifi_interface_state()

    def update_wifi_interface_state(self):
        global wifi_interface_selected
        wifi_interface_selected = (self.comboBox_comport.currentText() == WIFI_INTERFACE_OPTION)
        if hasattr(self, "comboBox_baudrate"):
            self.comboBox_baudrate.setEnabled(not wifi_interface_selected)
    
    def check_comport_Regularly(self):
        while True:
            if check_comport:
                print("hiiii")
                self.update_com_ports()
                self.update_com_ports_rtcm()  # Call get_comport if read_Replay_response is True
                time.sleep(1)  # Wait 0.5 seconds before checking again
            else:
                break

    def setupUi(self, MainWindow):
        self.msg_box_2_shown = False
        self.msg_box_error_shown = False
        self.second_window = None
        self.port = None
        self.running = False
        self.thread = None
        self.worker = Worker()
        #self.elapsed_time = 0
        """comport_thread = threading.Thread(target=self.check_comport_Regularly)
        comport_thread.start()"""

        MainWindow.setObjectName("GNSS Record and Replay")
        MainWindow.resize(700, 520)
        MainWindow.setFixedSize(700, 610)
        icon = QPixmap("green_satellite_small.png")  # Replace with the path to your icon file
        MainWindow.setWindowIcon(QtGui.QIcon(icon))
         # Set a modern background color or image
        MainWindow.setStyleSheet("background-color: #2C3E50; color: white;")  # Dark background with white text
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 871, 591))
        font = QtGui.QFont()
        font.setBold(True)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(140, 465, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText("please enter the file name")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(40, 465, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(40, 510, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 510, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setPlaceholderText("HH:MM:SS")
        self.lineEdit_2.setObjectName("lineEdit")
        self.lineEdit_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(560, 480, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{"
                                         "background-color:green;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "border-width: 5px;"
                                         "border-color: black;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: black;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: gray;"  # Change color when pressed if desired
                                         "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 540, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{"
                                         "background-color:red;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: black;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: gray;"  # Change color when pressed if desired
                                         "}")
        
        self.pushButton_3.setObjectName("pushButton_3")

        ################################### IMAGE REPLAY ###########################################
        # Add the image label
        self.green_light = QtWidgets.QLabel(self.frame)
        self.green_light.setGeometry(QtCore.QRect(285, 338, 18, 18))  # Adjust size and position as needed
        self.green_light.setObjectName("green_light")
        
        # Load and set the image
        #pixmap = QPixmap("green_light.png")  # Replace with your image path
        pixmap = QPixmap("green_light.png")
        self.green_light.setPixmap(pixmap)
        self.green_light.setScaledContents(True)
        
        # Add this after defining your other widgets

        # Add the image label
        self.red_light = QtWidgets.QLabel(self.frame)
        self.red_light.setGeometry(QtCore.QRect(285, 338, 18, 18))  # Adjust size and position as needed
        self.red_light.setObjectName("red_light")
        # Load and set the image
        #pixmap = QPixmap("xyz_nw_v03/xyz/red_light.png")  # Replace with your image path
        pixmap = QPixmap("red_light.png")
        
        self.red_light.setPixmap(pixmap)
        self.red_light.setScaledContents(True)
        # Add this after defining your other widgets
        ########################################################################################

        ################################### IMAGE RECORD ###########################################
        # Add the image label
        self.green_light_record = QtWidgets.QLabel(self.frame)
        self.green_light_record.setGeometry(QtCore.QRect(240, 562, 18, 18))  # Adjust size and position as needed
        self.green_light_record.setObjectName("green_light_record")
        
        # Load and set the image
        #pixmap = QPixmap("xyz_nw_v03/xyz/green_light.png")  # Replace with your image path
        pixmap = QPixmap("green_light.png")
        self.green_light_record.setPixmap(pixmap)
        self.green_light_record.setScaledContents(True)
        
        # Add this after defining your other widgets

        # Add the image label
        self.red_light_record = QtWidgets.QLabel(self.frame)
        self.red_light_record.setGeometry(QtCore.QRect(240, 562, 18, 18))  # Adjust size and position as needed
        self.red_light_record.setObjectName("red_light_record")
        # Load and set the image
        #pixmap = QPixmap("xyz_nw_v03/xyz/red_light.png")  # Replace with your image path
        pixmap = QPixmap("red_light.png")
        
        self.red_light_record.setPixmap(pixmap)
        self.red_light_record.setScaledContents(True)
        # Add this after defining your other widgets
        ########################################################################################
        self.label_developer = QtWidgets.QLabel(self.frame)
        self.label_developer.setGeometry(QtCore.QRect(660, 575, 100, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_developer.setFont(font)
        self.label_developer.setObjectName("label_ref_freq")
        self.label_developer.setText("DEV")
        self.label_developer.setStyleSheet("""
            QLabel {
                color: #ECF0F1;  # Text color
            }
        """)
        self.label_developer.setVisible(False)

        self.label_ssid = QtWidgets.QLabel(self.frame)
        self.label_ssid.setGeometry(QtCore.QRect(280, 350, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_ssid.setFont(font)
        self.label_ssid.setObjectName("label_ssid")
        self.label_ssid.setText("")
        self.label_ssid.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
            }
        """)

        self.lineEdit_hostname = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_hostname.setGeometry(QtCore.QRect(300, 400, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_hostname.setFont(font)
        self.lineEdit_hostname.setPlaceholderText("Enter Hostname")
        self.lineEdit_hostname.setObjectName("lineEdit_hostname")
        self.lineEdit_hostname.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                    """)
        self.lineEdit_hostname.setText("zbd")

        self.label_hostname = QtWidgets.QLabel(self.frame)
        self.label_hostname.setGeometry(QtCore.QRect(160, 400, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_hostname.setFont(font)
        self.label_hostname.setObjectName("label_hostname")
        self.label_hostname.setText("Host name")
        self.label_hostname.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
            }
        """)

        self.lineEdit_password = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_password.setGeometry(QtCore.QRect(450, 400, 120, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setPlaceholderText("Enter Password")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_hostname.setVisible(False)
        self.lineEdit_password.setVisible(False)
        self.label_hostname.setVisible(False)
        self.label_ssid.setVisible(False)


        self.label_ref_freq = QtWidgets.QLabel(self.frame)
        self.label_ref_freq.setGeometry(QtCore.QRect(210, 430, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_ref_freq.setFont(font)
        self.label_ref_freq.setObjectName("label_ref_freq")
        self.label_ref_freq.setText("Please select the reference frequency")
        self.label_ref_freq.setStyleSheet("""
            QLabel {
                color: #ECF0F1;  # Text color
            }
        """)
        self.label_ref_freq.setVisible(False)

        self.comboBox_ref_freq = QtWidgets.QComboBox(self.frame)
        self.comboBox_ref_freq.setGeometry(QtCore.QRect(280, 480, 130, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox_ref_freq.setFont(font)
        self.comboBox_ref_freq.setObjectName("comboBox_ref_freq")
        self.comboBox_ref_freq.setVisible(False)

        # Apply the same modern style
        self.comboBox_ref_freq.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)
        ######################################################################
        self.comboBox_ref_freq.setEnabled(False)
        self.comboBox_ref_freq.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
        self.update_ref_freq()
        ########################################################################################
        self.label_gpiomode = QtWidgets.QLabel(self.frame)
        self.label_gpiomode.setGeometry(QtCore.QRect(190, 70, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_gpiomode.setFont(font)
        self.label_gpiomode.setObjectName("label_gpiomode")
        self.label_gpiomode.setText("GPIO mode")
        self.label_gpiomode.setStyleSheet("""
            QLabel {
                color: #ECF0F1;  # Text color
            }
        """)

        self.radioButton_gpiomode = QtWidgets.QCheckBox("Record/Replay", self.frame)
        self.radioButton_gpiomode.setGeometry(QtCore.QRect(310, 80, 150, 30))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(10)
        font_checkbox.setBold(False)
        self.radioButton_gpiomode.setFont(font_checkbox)
        self.radioButton_gpiomode.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        
        # Second Radio Button (Dual Channel)
        self.radioButton_rfmdmode = QtWidgets.QCheckBox("RFMD", self.frame)
        self.radioButton_rfmdmode.setGeometry(QtCore.QRect(450, 80, 150, 30))
        self.radioButton_rfmdmode.setFont(font_checkbox)
        self.radioButton_rfmdmode.setStyleSheet(self.radioButton_gpiomode.styleSheet())

        # Button Group for radio buttons
        self.radio_group = QtWidgets.QButtonGroup(self.frame)
        self.radio_group.addButton(self.radioButton_gpiomode)
        self.radio_group.addButton(self.radioButton_rfmdmode)
        self.radioButton_gpiomode.setChecked(True)

        self.label_gpiomode.setVisible(False)
        self.radioButton_gpiomode.setVisible(False)
        self.radioButton_rfmdmode.setVisible(False)

        self.label_radio = QtWidgets.QLabel(self.frame)
        self.label_radio.setGeometry(QtCore.QRect(190, 120, 350, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_radio.setFont(font)
        self.label_radio.setObjectName("label_radio")
        self.label_radio.setText("Please select the number of Tx/Rx channels")
        self.label_radio.setStyleSheet("""
            QLabel {
                color: #ECF0F1;  # Text color
            }
        """)
        self.radioButton_single = QtWidgets.QCheckBox("Single", self.frame)
        self.radioButton_single.setGeometry(QtCore.QRect(250, 170, 150, 30))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(10)
        font_checkbox.setBold(False)
        self.radioButton_single.setFont(font_checkbox)
        self.radioButton_single.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        
        # Second Radio Button (Dual Channel)
        self.radioButton_double = QtWidgets.QCheckBox("Dual", self.frame)
        self.radioButton_double.setGeometry(QtCore.QRect(390, 170, 150, 30))
        self.radioButton_double.setFont(font_checkbox)
        self.radioButton_double.setStyleSheet(self.radioButton_single.styleSheet())

        # Button Group for radio buttons
        self.radio_group = QtWidgets.QButtonGroup(self.frame)
        self.radio_group.addButton(self.radioButton_single)
        self.radio_group.addButton(self.radioButton_double)
        self.radioButton_single.setChecked(True)

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(164, 20, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")

        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(298, 20, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_4.setObjectName("pushButton_4")
        #########################################################################################################################
        #########################################################################################################################
        self.comboBox_comport = QtWidgets.QComboBox(self.frame)
        self.comboBox_comport.setGeometry(QtCore.QRect(300, 255, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox_comport.setFont(font)
        self.comboBox_comport.setObjectName("comboBox_comport")

        # Apply modern style
        self.comboBox_comport.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)
        self.update_com_ports()
        self.comboBox_comport.showPopup = self.comboBox_comport_popup
        
        #self.comboBox_comport.addItem("Select Port")

        self.comboBox_baudrate = QtWidgets.QComboBox(self.frame)
        self.comboBox_baudrate.setGeometry(QtCore.QRect(420, 255, 100, 30))
        self.comboBox_baudrate.setFont(font)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")

        # Apply the same modern style
        self.comboBox_baudrate.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)
        self.update_baud_rates()

        self.comboBox_comport_rtcm = QtWidgets.QComboBox(self.frame)
        self.comboBox_comport_rtcm.setGeometry(QtCore.QRect(300, 300, 100, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox_comport_rtcm.setFont(font)
        self.comboBox_comport_rtcm.setObjectName("comboBox_comport_rtcm")
        self.comboBox_comport_rtcm.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
        self.update_com_ports_rtcm()
        if not RTCM_ports:
            self.comboBox_comport_rtcm.addItem("Select Port")
            self.comboBox_comport_rtcm.addItem("HW USB")

        if not non_rtcm_ports:
            self.comboBox_comport.addItem("Select Port") 
            self.comboBox_comport.addItem(WIFI_INTERFACE_OPTION) 
            self.comboBox_comport.addItem(WIFI_INTERFACE_OPTION_2)
        
        self.comboBox_comport_rtcm.setEnabled(False)
        self.comboBox_comport_rtcm.showPopup = self.comboBox_comport_rtcm_popup

        self.comboBox_baudrate_rtcm = QtWidgets.QComboBox(self.frame)
        self.comboBox_baudrate_rtcm.setGeometry(QtCore.QRect(420, 300, 100, 30))
        self.comboBox_baudrate_rtcm.setFont(font)
        self.comboBox_baudrate_rtcm.setObjectName("comboBox_baudrate_rtcm")

        # Apply the same modern style
        self.comboBox_baudrate_rtcm.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
        self.update_baud_rates_rtcm()
        self.comboBox_baudrate_rtcm.setEnabled(False)
        self.radioButton_rtcm = QtWidgets.QCheckBox("RTCM", self.frame)
        self.radioButton_rtcm.setGeometry(QtCore.QRect(195, 300, 100, 30))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.radioButton_rtcm.setFont(font_checkbox)
        self.radioButton_rtcm.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        

        self.radioButton_ad9361 = QtWidgets.QCheckBox("RR Board", self.frame)
        self.radioButton_ad9361.setGeometry(QtCore.QRect(195, 255, 100, 30))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.radioButton_ad9361.setFont(font_checkbox)
        self.radioButton_ad9361.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.radioButton_ad9361.setVisible(True)
        self.radioButton_ad9361.setChecked(True)
        self.radioButton_ad9361.setEnabled(False)
        #######################################################################################################################

        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(565, 20, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_login = QtWidgets.QPushButton(self.frame)
        self.pushButton_login.setGeometry(QtCore.QRect(30, 20, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_login.setFont(font)
        self.pushButton_login.setStyleSheet("QPushButton{"
                                         "background-color: #1ABC9C;"
                                         "color: white;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_login.setObjectName("pushButton_login")
        ####################################################################################

        ############################# Pushbutton-Selectfiles ###############################
        self.pushButton_select_file = QtWidgets.QPushButton(self.frame)
        self.pushButton_select_file.setGeometry(QtCore.QRect(430, 20, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_select_file.setFont(font)
        self.pushButton_select_file.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_select_file.setObjectName("pushButton_select_file")
        self.pushButton_select_file.setText("Files")
        self.pushButton_select_file.clicked.connect(self.open_select_file_dialog)

        self.label_config = QtWidgets.QLabel(self.frame)
        self.label_config.setGeometry(QtCore.QRect(230, 260, 245, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_config.setFont(font)
        self.label_config.setObjectName("label_config")
        self.label_config.setText("Please select the required files")

        self.pushButton_browse_config = QtWidgets.QPushButton(self.frame)
        self.pushButton_browse_config.setGeometry(QtCore.QRect(300, 295, 55, 31))
        self.pushButton_browse_config.setObjectName("pushButton_browse_record")
        self.pushButton_browse_config.setText("Browse..")
        self.pushButton_browse_config.clicked.connect(self.browse_file)
        self.pushButton_browse_config.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        
        self.pushButton_refresh_config = QtWidgets.QPushButton(self.frame)
        self.pushButton_refresh_config.setGeometry(QtCore.QRect(370, 295, 31, 31))
        self.pushButton_refresh_config.setObjectName("pushButton_refresh_config")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("Refresh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_refresh_config.setIcon(icon)
        self.pushButton_refresh_config.setIconSize(QSize(30, 30))  # Set icon size
        # Connect the button to the clicked action
        self.pushButton_refresh_config.clicked.connect(self.check_selected_files_availability)

        self.pushButton_refresh_config_maxduration = QtWidgets.QPushButton(self.frame)
        self.pushButton_refresh_config_maxduration.setGeometry(QtCore.QRect(265, 515, 31, 31))
        self.pushButton_refresh_config_maxduration.setObjectName("pushButton_refresh_config")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("Refresh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_refresh_config_maxduration.setIcon(icon)
        self.pushButton_refresh_config_maxduration.setIconSize(QSize(30, 30))  # Set icon size
        # Connect the button to the clicked action
        self.pushButton_refresh_config_maxduration.clicked.connect(self.get_max_duration)
        self.pushButton_refresh_config_maxduration.setVisible(False)
        
        
        # QTableWidget added below the QLineEdit
        self.table_widget = QtWidgets.QTableWidget(self.frame)
        self.table_widget.setGeometry(QtCore.QRect(135, 340, 420, 238))
        
        # Enable gridlines
        self.table_widget.setShowGrid(True)

        # Set the background color of the table, gridline color, and text color
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2C3E50;
                gridline-color: #1ABC9C; /* Ensures gridlines are visible */
            }
            QHeaderView::section {
                background-color: #2C3E50;
                color: white;
                border: 1px solid #1ABC9C; /* Add border to the header */
            }
            QTableWidget::item {
                color: white;
                border: 1px solid #1ABC9C; /* Ensures items have borders */
            }
        """)

        
        self.table_widget.setRowCount(7)  # Set the number of rows
        self.table_widget.setColumnCount(2)  # Set the number of columns
        self.table_widget.setHorizontalHeaderLabels(["Files", "Action"])

        # Set the row numbers from 0 to 6
        self.table_widget.setVerticalHeaderLabels([str(i) for i in range(7)])

        # Set the column width
        self.table_widget.setColumnWidth(0, 300)
        self.table_widget.setColumnWidth(1, 100)

        # Populate the table with some data (example)
        self.variable_names = []
        self.populate_table()

        # Style the QTableWidget
        self.table_widget.itemClicked.connect(self.show_popup_table)

        self.label_config.setVisible(False)
        self.table_widget.setVisible(False)

        self.pushButton_browse_config.setVisible(False)
        self.pushButton_refresh_config.setVisible(False)
        ####################################################################################

        ####################################################################################
        self.label_3 = QtWidgets.QCheckBox("", self.frame)
        self.label_3.setGeometry(QtCore.QRect(260, 210, 111, 51))
        label_3 = QtGui.QFont()
        label_3.setPointSize(12)
        label_3.setBold(False)
        self.label_3.setFont(label_3)
        self.label_3.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.label_3.setEnabled(False)
        self.label_3.setChecked(True)

        self.label_4 = QtWidgets.QCheckBox("", self.frame)
        self.label_4.setGeometry(QtCore.QRect(535, 210, 111, 51))
        label_4 = QtGui.QFont()
        label_4.setPointSize(12)
        label_4.setBold(False)
        self.label_4.setFont(label_4)
        self.label_4.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.label_4.setEnabled(False)
        self.label_4.setChecked(True)

        self.radioButton_Rx_1 = QtWidgets.QCheckBox("Rx 1", self.frame)
        self.radioButton_Rx_1.setGeometry(QtCore.QRect(260, 210, 111, 51))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(False)
        self.radioButton_Rx_1.setFont(font_checkbox)
        self.radioButton_Rx_1.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        
        self.radioButton_Rx_2 = QtWidgets.QCheckBox("Rx 2", self.frame)
        self.radioButton_Rx_2.setGeometry(QtCore.QRect(535, 210, 111, 51))
        self.radioButton_Rx_2.setFont(font_checkbox)
        self.radioButton_Rx_2.setStyleSheet(self.radioButton_Rx_1.styleSheet())

        # Button Group for radio buttons
        self.radio_group_Rx = QtWidgets.QButtonGroup(self.frame)
        self.radio_group_Rx.addButton(self.radioButton_Rx_1)
        self.radio_group_Rx.addButton(self.radioButton_Rx_2)
        self.radioButton_Rx_1.setChecked(True)


        self.radioButton_Rx_1.toggled.connect(self.show_popup)
        self.radioButton_Rx_2.toggled.connect(self.show_popup_2)
        
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 260, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setPlaceholderText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(460, 260, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setPlaceholderText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_bandwidth_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_bandwidth_2.setGeometry(QtCore.QRect(460, 350, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_bandwidth_2.setFont(font)
        self.lineEdit_bandwidth_2.setPlaceholderText("")
        self.lineEdit_bandwidth_2.setObjectName("lineEdit_bandwidth_2")
        self.lineEdit_bandwidth_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.label_bandwidth = QtWidgets.QLabel(self.frame)
        self.label_bandwidth.setGeometry(QtCore.QRect(40, 330, 5, 5))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_bandwidth.setFont(font)
        self.label_bandwidth.setObjectName("label_11")
        #self.label_bandwidth.setText("BW (MHz)|")

        self.label_gain = QtWidgets.QLabel(self.frame)
        self.label_gain.setGeometry(QtCore.QRect(40, 355, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_gain.setFont(font)
        self.label_gain.setObjectName("label_11")
        self.label_gain.setText("BW | Gain")
        self.label_gain.setVisible(False)
        
        
        self.label_samplingfreq = QtWidgets.QLabel(self.frame)
        self.label_samplingfreq.setGeometry(QtCore.QRect(40, 395, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_samplingfreq.setFont(font)
        self.label_samplingfreq.setObjectName("label_11")
        self.label_samplingfreq.setText("Samp frequency")
        self.label_sampling = QtWidgets.QLabel(self.frame)
        self.label_sampling.setGeometry(QtCore.QRect(40, 380, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_sampling.setFont(font)
        self.label_sampling.setObjectName("label_11")
        self.label_sampling.setText("Sampling")
        self.lineEdit_samplingfreq = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_samplingfreq.setGeometry(QtCore.QRect(190, 395, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_samplingfreq.setFont(font)
        self.lineEdit_samplingfreq.setPlaceholderText("")
        self.lineEdit_samplingfreq.setObjectName("lineEdit_samplingfreq")
        self.lineEdit_samplingfreq.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        

        self.lineEdit_samplingfreq_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_samplingfreq_2.setGeometry(QtCore.QRect(460, 395, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_samplingfreq_2.setFont(font)
        self.lineEdit_samplingfreq_2.setPlaceholderText("")
        self.lineEdit_samplingfreq_2.setObjectName("lineEdit_samplingfreq_2")
        self.lineEdit_samplingfreq_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        

        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(40, 305, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setGeometry(QtCore.QRect(20, 445, 657, 2))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_2.setStyleSheet("color: white; background-color: #1ABC9C; border: none; height: 1px;")
        
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(40, 260, 131, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")

        self.label_MHz_LO = QtWidgets.QLabel(self.frame)
        self.label_MHz_LO.setGeometry(QtCore.QRect(410, 260, 30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_MHz_LO.setFont(font)
        self.label_MHz_LO.setObjectName("label_MHz_LO")
        self.label_MHz_LO.setText("MHz")

        self.label_MHz_SF = QtWidgets.QLabel(self.frame)
        self.label_MHz_SF.setGeometry(QtCore.QRect(410, 395, 30, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_MHz_SF.setFont(font)
        self.label_MHz_SF.setObjectName("label_MHz_LO")
        self.label_MHz_SF.setText("MHz")

        self.label_MHz_BW = QtWidgets.QLabel(self.frame)
        self.label_MHz_BW.setGeometry(QtCore.QRect(400, 350, 55, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_MHz_BW.setFont(font)
        self.label_MHz_BW.setObjectName("label_MHz_BW")
        self.label_MHz_BW.setText("MHz | dB")
        self.label_MHz_BW.setVisible(False)
        self.label_MHz_LO.setVisible(False)
        self.label_MHz_SF.setVisible(False)
 


        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(40, 245, 51, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        ################################# fs_system ####################################
        self.label_SD_image_system_download = QtWidgets.QLabel(self.frame)
        self.label_SD_image_system_download.setGeometry(QtCore.QRect(415, 185, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_SD_image_system_download.setFont(font)
        self.label_SD_image_system_download.setObjectName("label_SD_image_system_download")
        self.label_SD_image_system_download.setText(f"Building in progress...(0%)")
        

        self.label_SD_image_system_download_2 = QtWidgets.QLabel(self.frame)
        self.label_SD_image_system_download_2.setGeometry(QtCore.QRect(448, 185, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_SD_image_system_download_2.setFont(font)
        self.label_SD_image_system_download_2.setObjectName("label_SD_image_system_download_2")
        self.label_SD_image_system_download_2.setText(f"Build completed!")
        self.label_SD_image_system_download_2.setVisible(False)
        self.label_SD_image_system_download.setVisible(False)

        self.label_SD_image_system = QtWidgets.QLabel(self.frame)
        self.label_SD_image_system.setGeometry(QtCore.QRect(405, 80, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_SD_image_system.setFont(font)
        self.label_SD_image_system.setObjectName("label_SD_image_system")
        self.label_SD_image_system.setText("Compilation of the libiio folder")
        self.label_SD_image_system.setVisible(False)

        self.label_SD_image_display = QtWidgets.QPushButton(self.frame)
        self.label_SD_image_display.setGeometry(QtCore.QRect(470, 145, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_SD_image_display.setFont(font)
        self.label_SD_image_display.setText("Rebuild")
        self.label_SD_image_display.setObjectName("label_SD_image_display")
        self.label_SD_image_display.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        self.label_SD_image_display.setVisible(False)
        self.label_SD_image_display.clicked.connect(self.rebuild_image)

        self.label_fs_system = QtWidgets.QLabel(self.frame)
        self.label_fs_system.setGeometry(QtCore.QRect(220, 80, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_fs_system.setFont(font)
        self.label_fs_system.setObjectName("label_fs_system")
        self.label_fs_system.setText("Please enter label of the nvme SSD")
        self.label_fs_system.setVisible(False)

        self.label_fs_system_display = QtWidgets.QPushButton(self.frame)
        self.label_fs_system_display.setGeometry(QtCore.QRect(310, 215, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.label_fs_system_display.setFont(font)
        self.label_fs_system_display.setText("NVME Info")
        self.label_fs_system_display.setObjectName("label_fs_system_display")
        self.label_fs_system_display.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        self.label_fs_system_display.setVisible(False)
        self.label_fs_system_display.clicked.connect(self.give_nvme_info)


        self.lineEdit_fs_system = QtWidgets.QLineEdit(self.frame)  # Add a QLineEdit for the timer
        self.lineEdit_fs_system.setGeometry(QtCore.QRect(251, 125, 200, 31))  # Adjust position to fit next to progress bar
        #self.lineEdit_fs_system.setText(f"{fs_system}")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_fs_system.setFont(font)
        self.lineEdit_fs_system.setObjectName("lineEdit_fs_system")
        self.lineEdit_fs_system.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_fs_system.setVisible(False)

        self.fs_system_submit_btn = QtWidgets.QPushButton(self.frame)
        self.fs_system_submit_btn.setGeometry(QtCore.QRect(325, 170, 50, 31))
        self.fs_system_submit_btn.setObjectName("pushButton_browse_record")
        self.fs_system_submit_btn.setText("Submit")
        self.fs_system_submit_btn.clicked.connect(self.submit_to_edit)
        self.fs_system_submit_btn.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        
        self.fs_system_edit_btn = QtWidgets.QPushButton(self.frame)
        self.fs_system_edit_btn.setGeometry(QtCore.QRect(325, 170, 50, 31))
        self.fs_system_edit_btn.setObjectName("pushButton_browse_record")
        self.fs_system_edit_btn.setText("Edit")
        self.fs_system_edit_btn.clicked.connect(self.edit_to_submit)
        self.fs_system_edit_btn.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        self.fs_system_edit_btn.setVisible(False)
        self.fs_system_submit_btn.setVisible(False)

        self.line_fs_system = QtWidgets.QFrame(self.frame)
        self.line_fs_system.setGeometry(QtCore.QRect(20, 255, 657, 2))
        self.line_fs_system.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_fs_system.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_fs_system.setObjectName("line_fs_system")
        self.line_fs_system.setStyleSheet("color: white; background-color: #1ABC9C; border: none; height: 1px;")
        self.line_fs_system.setVisible(False)

        self.vericalline_fs_system = QtWidgets.QFrame(self.frame)
        self.vericalline_fs_system.setGeometry(QtCore.QRect(350, 90, 2, 150))  # Width=2 (thin), Height=100 (tall)
        self.vericalline_fs_system.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.vericalline_fs_system.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.vericalline_fs_system.setObjectName("line_fs_system")
        self.vericalline_fs_system.setStyleSheet("background-color: #1ABC9C; border: none;")  # No height styling
        self.vericalline_fs_system.setVisible(False)
        #############################################################################
        self.label_connectivity = QtWidgets.QLabel(self.frame)
        self.label_connectivity.setGeometry(QtCore.QRect(182, 200, 350, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_connectivity.setFont(font)
        self.label_connectivity.setObjectName("label_connectivity")
        self.label_connectivity.setText("Please select required COM port and Baudrate")

        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(190, 305, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox:focus {
                border: 2px solid #2E5;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)

        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        """self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")"""
        self.comboBox_2 = QtWidgets.QComboBox(self.frame)
        self.comboBox_2.setGeometry(QtCore.QRect(460, 305, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        """self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")"""
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(40, 555, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)  # Add a QLineEdit for the timer
        self.lineEdit_6.setGeometry(QtCore.QRect(140, 555, 91, 31))  # Adjust position to fit next to progress bar
        self.lineEdit_6.setText("")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #1ABC9C;
                                            }
                                        """)
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_6.setReadOnly(True)  # Make the timer display read-only
        #self.lineEdit_6.setStyleSheet("background-color: white;")  # Set background color
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 38))
        self.menubar.setObjectName("menubar")
        self.menuEmbedded_Systems = QtWidgets.QMenu(self.menubar)
        self.menuEmbedded_Systems.setTitle("")
        self.menuEmbedded_Systems.setObjectName("menuEmbedded_Systems")
        MainWindow.setMenuBar(self.menubar)
        self.label_about_2 = QtWidgets.QLabel(self.frame)
        self.label_about_2.setGeometry(QtCore.QRect(230, 120, 260, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_about_2.setFont(font)
        self.label_about_2.setObjectName("label_2")
        self.label_about_3 = QtWidgets.QLabel(self.frame)
        self.label_about_3.setGeometry(QtCore.QRect(285, 160, 260, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_about_3.setFont(font)
        self.label_about_3.setObjectName("label_3")
        self.label_about_2.setText("GNSS Record and Replay")
        self.label_about_3.setText(version)
        ########################## SSD Space Note ################################
        self.label_SSD_capacity = QtWidgets.QLabel(self.frame)
        self.label_SSD_capacity.setGeometry(QtCore.QRect(300, 551, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.label_SSD_capacity.setFont(font)
        self.label_SSD_capacity.setObjectName("label_SSD_capacity")
        self.label_SSD_capacity.setVisible(False)

        self.label_available_Duration = QtWidgets.QLabel(self.frame)
        self.label_available_Duration.setGeometry(QtCore.QRect(300, 515, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.label_available_Duration.setFont(font)
        self.label_available_Duration.setObjectName("label_available_Duration")
        self.label_available_Duration.setText("Max Duration:")
        self.label_available_Duration.setVisible(False)
        
        #####################################################################################
        self.label_replay = QtWidgets.QLabel(self.frame)
        self.label_replay.setGeometry(QtCore.QRect(85, 330, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_replay.setFont(font)
        self.label_replay.setObjectName("label_replay")
        self.label_replay.setText("Progress")

        self.lineEdit_replay = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_replay.setGeometry(QtCore.QRect(185, 330, 91, 31))
        self.lineEdit_replay.setText("")
        self.lineEdit_replay.setObjectName("lineEdit_2")
        self.lineEdit_replay.setEnabled(False)
        self.lineEdit_replay.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #1ABC9C;
                                            }
                                        """)
        
        self.label_deviceid = QtWidgets.QLabel(self.frame)
        self.label_deviceid.setGeometry(QtCore.QRect(200, 350, 130, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_deviceid.setFont(font)
        self.label_deviceid.setObjectName("label_deviceid")
        self.label_deviceid.setText("Device ID")
        self.lineEdit_deviceid= QtWidgets.QLineEdit(self.frame)
        self.lineEdit_deviceid.setGeometry(QtCore.QRect(280, 350, 45, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_deviceid.setFont(font)
        self.lineEdit_deviceid.setPlaceholderText("")
        self.lineEdit_deviceid.setObjectName("lineEdit_deviceid")
        self.lineEdit_deviceid.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_deviceid.setPlaceholderText("ID")
        self.lineEdit_deviceid.setText("")
        self.lineEdit_deviceid.setVisible(True)
        self.label_deviceid.setVisible(True)

        
        
        self.label_busno = QtWidgets.QLabel(self.frame)
        self.label_busno.setGeometry(QtCore.QRect(340, 350, 130, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_busno.setFont(font)
        self.label_busno.setObjectName("label_busno")
        self.label_busno.setText("Bus no")
        self.lineEdit_busno= QtWidgets.QLineEdit(self.frame)
        self.lineEdit_busno.setGeometry(QtCore.QRect(400, 350, 45, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_busno.setFont(font)
        self.lineEdit_busno.setPlaceholderText("")
        self.lineEdit_busno.setObjectName("lineEdit_busno")
        self.lineEdit_busno.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_busno.setPlaceholderText("no")
        self.lineEdit_busno.setText("")
        
        self.pushButton_usb_info = QtWidgets.QPushButton(self.frame)
        self.pushButton_usb_info.setGeometry(QtCore.QRect(460, 350, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.pushButton_usb_info.setFont(font)
        self.pushButton_usb_info.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white; 
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QPushButton:pressed {
                background-color: #148F77;
            }
        """)
        self.pushButton_usb_info.setText("USB info")
        self.pushButton_usb_info.setObjectName("pushButton_usb_info")
        self.pushButton_usb_info.clicked.connect(self.open_usb_info)
        self.lineEdit_busno.setVisible(False)
        self.label_busno.setVisible(False)
        self.pushButton_usb_info.setVisible(False)
        self.lineEdit_deviceid.setVisible(False)
        self.label_deviceid.setVisible(False)
       

        self.label_rate = QtWidgets.QLabel(self.frame)
        self.label_rate.setGeometry(QtCore.QRect(390, 230, 130, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_rate.setFont(font)
        self.label_rate.setObjectName("label_rate")
        self.label_rate.setText("RTCM rate (Hz)")
        self.lineEdit_rate= QtWidgets.QLineEdit(self.frame)
        self.lineEdit_rate.setGeometry(QtCore.QRect(520, 230, 45, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_rate.setFont(font)
        self.lineEdit_rate.setPlaceholderText("")
        self.lineEdit_rate.setObjectName("lineEdit_rate")
        self.lineEdit_rate.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_rate.setPlaceholderText("Hz")
        self.lineEdit_rate.setText("1")
        self.lineEdit_rate.setVisible(False)
        self.label_rate.setVisible(False)

        self.radioButton_autoplay = QtWidgets.QCheckBox("Auto-replay", self.frame)
        self.radioButton_autoplay.setGeometry(QtCore.QRect(315, 330, 150, 31))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.radioButton_autoplay.setFont(font_checkbox)
        self.radioButton_autoplay.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.radioButton_autoplay.setVisible(False)
        ##########################################################################################
        self.label_Gain_Tx_2ch = QtWidgets.QCheckBox("", self.frame)
        self.label_Gain_Tx_2ch.setGeometry(QtCore.QRect(185, 230, 30, 31))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.label_Gain_Tx_2ch.setFont(font_checkbox)
        self.label_Gain_Tx_2ch.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.label_Gain_Tx_2ch.setVisible(False)
        self.label_Gain_Tx_2ch.setChecked(True)
        self.label_Gain_Tx_2ch.setEnabled(False)

        self.label_Gain_Tx_2_2ch = QtWidgets.QCheckBox("", self.frame)
        self.label_Gain_Tx_2_2ch.setGeometry(QtCore.QRect(280, 230, 30, 31))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.label_Gain_Tx_2_2ch.setFont(font_checkbox)
        self.label_Gain_Tx_2_2ch.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.label_Gain_Tx_2_2ch.setVisible(False)
        self.label_Gain_Tx_2_2ch.setChecked(True)
        self.label_Gain_Tx_2_2ch.setEnabled(False)

        self.label_Gain_Tx_3ch = QtWidgets.QLabel(self.frame)
        self.label_Gain_Tx_3ch.setGeometry(QtCore.QRect(82, 230, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_Gain_Tx_3ch.setFont(font)
        self.label_Gain_Tx_3ch.setObjectName("label_Gain_Tx_2ch")
        self.label_Gain_Tx_3ch.setText("Gain (dB)")
        self.label_Gain_Tx_3ch.setVisible(False)
        

        self.label_Gain_Tx = QtWidgets.QCheckBox("", self.frame)
        self.label_Gain_Tx.setGeometry(QtCore.QRect(185, 230, 100, 31))
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.label_Gain_Tx.setFont(font_checkbox)
        self.label_Gain_Tx.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        
        self.label_Gain_Tx_2 = QtWidgets.QCheckBox("", self.frame)
        self.label_Gain_Tx_2.setGeometry(QtCore.QRect(280, 230, 30, 31))
        self.label_Gain_Tx_2.setFont(font_checkbox)
        self.label_Gain_Tx_2.setStyleSheet(self.radioButton_Rx_1.styleSheet())

        # Button Group for radio buttons
        self.radio_group_Tx = QtWidgets.QButtonGroup(self.frame)
        self.radio_group_Tx.addButton(self.label_Gain_Tx)
        self.radio_group_Tx.addButton(self.label_Gain_Tx_2)
        self.label_Gain_Tx.setChecked(True)

        self.label_Gain_Tx.toggled.connect(self.show_tx_1)
        self.label_Gain_Tx_2.toggled.connect(self.show_tx_2)
        ##########################################################################################
        self.radioButton_GPIO_Replay = QtWidgets.QCheckBox("GPIOs", self.frame)
        self.radioButton_GPIO_Replay.setGeometry(QtCore.QRect(70, 190, 140, 30))
        self.radioButton_GPIO_Replay.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.radioButton_GPIO_Replay.setFont(font_checkbox)
        self.radioButton_GPIO_Replay.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                    spacing: 56 px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)
        self.lineEdit_Gain_Tx= QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Gain_Tx.setGeometry(QtCore.QRect(215, 230, 45, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_Gain_Tx.setFont(font)
        self.lineEdit_Gain_Tx.setPlaceholderText("")
        self.lineEdit_Gain_Tx.setObjectName("lineEdit_Gain_Tx")
        self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        #self.lineEdit_Gain_Tx.setPlaceholderText("dB")
        self.lineEdit_Gain_Tx.setText("")
        self.label_Gain_Tx.setVisible(False)
        self.lineEdit_Gain_Tx.setVisible(False)
        self.lineEdit_Gain_Tx.setText(default_gain_tx)

        self.lineEdit_Gain_Tx_2= QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Gain_Tx_2.setGeometry(QtCore.QRect(310, 230, 45, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_Gain_Tx_2.setFont(font)
        
        self.lineEdit_Gain_Tx_2.setObjectName("lineEdit_Gain_Tx_2")
        self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_Gain_Tx_2.setText(default_gain_tx)
        self.label_Gain_Tx_2.setVisible(False)
        self.lineEdit_Gain_Tx_2.setVisible(False)
        self.lineEdit_Gain_Tx.setEnabled(True)
        if self.radioButton_gpiomode.isChecked():
            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
        self.radioButton_GPIO_Replay.setEnabled(True)
        self.lineEdit_Gain_Tx_2.setEnabled(False)
        self.label_Gain_Tx_2_2ch.setVisible(False)
        self.label_Gain_Tx_2ch.setVisible(False)
        self.lineEdit_Gain_Tx.setPlaceholderText("Tx 1")
        self.lineEdit_Gain_Tx_2.setPlaceholderText("Tx 2")
        ##########################################################################################

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_started = False
        self.elapsed_time = QtCore.QTime(0, 0)

        # Create a QTimer object
        self.timer_1 = QtCore.QTimer()
        self.timer_1.timeout.connect(self.update_time_1)
        self.timer_started_1 = False
        self.elapsed_time_1 = QtCore.QTime(0, 0)

        # Connect the replay button to open the replay window
        self.pushButton_4.clicked.connect(self.open_replay_window)

        # Connect the replay button to open the replay window
        self.pushButton_2.clicked.connect(self.main_function)

        self.menuEmbedded_Systems = QtWidgets.QMenu(self.menubar)
        self.menuEmbedded_Systems.setTitle("Embedded_Systems")

        self.pushButton_5.clicked.connect(self.open_about_dialog)
        self.pushButton_login.clicked.connect(self.open_login_dialog)
        
        #submit button
        self.pushButton_submit = QtWidgets.QPushButton(self.frame)
        self.pushButton_submit.setGeometry(QtCore.QRect(320, 450, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.pushButton_submit.setFont(font)
        self.pushButton_submit.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white; 
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QPushButton:pressed {
                background-color: #148F77;
            }
        """)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.pushButton_submit.setText("Submit")

        ########################### To be deleted ###############################################
        """self.pushButton_deleted = QtWidgets.QPushButton(self.frame)
        self.pushButton_deleted.setGeometry(QtCore.QRect(298, 400, 40, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.pushButton_deleted.setFont(font)
        pixmap = QPixmap('hide_22.png')  # Replace with your image path
        icon = QIcon(pixmap.scaled(35, 35))  # Adjust size as needed
        self.pushButton_deleted.setIcon(icon)
        self.pushButton_deleted.setIconSize(QSize(30, 30))  # Set icon size"""

        """self.pushButton_deleted = QtWidgets.QPushButton(self.frame)
        self.pushButton_deleted.setGeometry(QtCore.QRect(298, 400, 40, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.pushButton_deleted.setFont(font)
        pixmap = QPixmap('show_22.png')  # Replace with your image path
        icon = QIcon(pixmap.scaled(35, 35))  # Adjust size as needed
        self.pushButton_deleted.setIcon(icon)
        self.pushButton_deleted.setIconSize(QSize(30, 30))  # Set icon size"""
        ########################################################################################

        # Create new buttons
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(350, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("QPushButton{"
                                         "background-color:red;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "border-width: 5px;"
                                         "border-color: black;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: black;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: gray;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_6.setObjectName("pushButton_6")

        
        self.pushButton_7 = QtWidgets.QPushButton(self.frame)
        self.pushButton_7.setGeometry(QtCore.QRect(230, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("QPushButton{"
                                         "background-color:green;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "border-width: 5px;"
                                         "border-color: black;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: black;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: gray;"  # Change color when pressed if desired
                                         "}")
        self.pushButton_7.setObjectName("pushButton_7")
        ###################################################################################
        self.pushButton_invisible = QtWidgets.QPushButton(self.frame)
        self.pushButton_invisible.setGeometry(QtCore.QRect(245, 270, 200, 200))
        #svg_renderer = QSvgRenderer("green_satellite.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(310, 310)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_invisible.setIcon(icon)
        self.pushButton_invisible.setIconSize(QSize(500, 500))
        self.pushButton_invisible.clicked.connect(self.invisible_button)
        self.pushButton_invisible.setVisible(False)
        

        self.pushButton_pdf = QtWidgets.QPushButton(self.frame)
        self.pushButton_pdf.setGeometry(QtCore.QRect(305, 210, 90, 30))
        self.pushButton_pdf.setObjectName("pushButton_browse_record")
        self.pushButton_pdf.setText("User Manual")
        self.pushButton_pdf.clicked.connect(self.open_pdf)
        self.pushButton_pdf.setStyleSheet("""
                                            QPushButton {
                                                background-color: #1ABC9C;
                                                color: #FFFFFF;
                                                border-radius: 10px;
                                                padding: 5px 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #3A7;
                                            }
                                            QPushButton:pressed {
                                                background-color: #2E5;
                                            }
                                        """)
        self.pushButton_pdf.setVisible(False)
        ###############################################################################################
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(290, 280, 115, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(383, 280, 91, 31))
        self.lineEdit_7.setText("")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_7.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_8.setGeometry(QtCore.QRect(185, 280, 91, 31))
        self.lineEdit_8.setText("")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_8.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        """self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(315, 190, 115, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")"""
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(85, 280, 95, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.lineEdit9 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit9.setGeometry(QtCore.QRect(185, 100, 286, 31))
        self.lineEdit9.setObjectName("lineEdit")
        self.lineEdit9.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        #######################################################################################
        self.lineEdit_replay_rtcm = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_replay_rtcm.setGeometry(QtCore.QRect(185, 150, 286, 31))
        self.lineEdit_replay_rtcm.setObjectName("lineEdit")
        self.lineEdit_replay_rtcm.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_replay_rtcm.setVisible(True)
        self.lineEdit_replay_rtcm.setReadOnly(True) 
        self.lineEdit_replay_rtcm.setPlaceholderText("Please select the file")

        self.pushButton_browse_replay_rtcm = QtWidgets.QPushButton(self.frame)
        self.pushButton_browse_replay_rtcm.setGeometry(QtCore.QRect(535, 150, 31, 31))
        self.pushButton_browse_replay_rtcm.setObjectName("pushButton_browse_replay_rtcm")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_browse_replay_rtcm.setIcon(icon)
        self.pushButton_browse_replay_rtcm.setIconSize(QSize(30, 30))  # Set icon size
        self.pushButton_browse_replay_rtcm.clicked.connect(self.browse_folder_Record_rtcm)
        self.pushButton_browse_replay_rtcm.setVisible(True)
        self.pushButton_browse_replay_rtcm.setEnabled(True)

        ########################################################################################
        self.pushButton_8 = QtWidgets.QPushButton(self.frame)
        self.pushButton_8.setGeometry(QtCore.QRect(535, 100, 31, 31))
        self.pushButton_8.setObjectName("pushButton_6")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_8.setIcon(icon)
        self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size

        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(85, 100, 95, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label")

        #################################################################################################
        self.label_files_rtcm = QtWidgets.QLabel(self.frame)
        self.label_files_rtcm.setGeometry(QtCore.QRect(85, 150, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_files_rtcm.setFont(font)
        self.label_files_rtcm.setObjectName("label_files_rtcm")
        self.label_files_rtcm.setText("RTCM")
        ################################################################################################
        self.line_vertical = QtWidgets.QFrame(self.frame)
        self.line_vertical.setGeometry(QtCore.QRect(288, 352, 2, 28))  # Adjust the x, y position and height
        self.line_vertical.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_vertical.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_vertical.setObjectName("line_vertical")
        self.line_vertical.setStyleSheet("color: #1ABC9C; background-color: #1ABC9C; border: none; width: 1px;")

        self.line_vertical_2 = QtWidgets.QFrame(self.frame)
        self.line_vertical_2.setGeometry(QtCore.QRect(558, 352, 2, 28))  # Adjust the x, y position and height
        self.line_vertical_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_vertical_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_vertical_2.setObjectName("line_vertical_2")
        self.line_vertical_2.setStyleSheet("color: #1ABC9C; background-color: #1ABC9C; border: none; width: 1px;")
        self.line_vertical.setVisible(False)
        self.line_vertical_2.setVisible(False)

        self.line_vertical_Replay = QtWidgets.QFrame(self.frame)
        self.line_vertical_Replay.setGeometry(QtCore.QRect(372, 230, 2, 28))  # Adjust the x, y position and height
        self.line_vertical_Replay.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_vertical_Replay.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_vertical_Replay.setObjectName("line_vertical_Replay")
        self.line_vertical_Replay.setStyleSheet("color: #1ABC9C; background-color: #1ABC9C; border: none; width: 1px;")
        self.line_vertical_Replay.setVisible(False)

        #################################################################################################
        self.radioButton_GPIO_Record = QtWidgets.QCheckBox("GPIOs", self.frame)
        self.radioButton_GPIO_Record.setGeometry(QtCore.QRect(25, 170, 140, 30))
        self.radioButton_GPIO_Record.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        font_checkbox = QtGui.QFont()
        font_checkbox.setPointSize(12)
        font_checkbox.setBold(True)
        self.radioButton_GPIO_Record.setFont(font_checkbox)
        self.radioButton_GPIO_Record.setStyleSheet("""
            QCheckBox {
                    color: #FFFFFF;
                    spacing: 58 px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                    image: url(tick.png);
                    border-radius: 3px;
                }
        """)

        self.line_record = QtWidgets.QFrame(self.frame)
        self.line_record.setGeometry(QtCore.QRect(20, 210, 657, 2))
        self.line_record.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_record.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_record.setObjectName("line_record")
        self.line_record.setStyleSheet("color: #1ABC9C; background-color: #1ABC9C; border: none; height: 1px;")
        self.label_browse_record = QtWidgets.QLabel(self.frame)
        self.label_browse_record.setGeometry(QtCore.QRect(40, 80, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_browse_record.setFont(font)
        self.label_browse_record.setObjectName("label_browse_record")
        self.label_browse_record.setText("AD9361")

        self.label_browse_record_rtcm = QtWidgets.QLabel(self.frame)
        self.label_browse_record_rtcm.setGeometry(QtCore.QRect(40, 130, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_browse_record_rtcm.setFont(font)
        self.label_browse_record_rtcm.setObjectName("label_browse_record_rtcm")
        self.label_browse_record_rtcm.setText("RTCM")
        self.label_browse_record_rtcm.setVisible(False)
        self.radioButton_GPIO_Record.setVisible(False)
        ######################################## Hide and display path in recording ####################################################
        self.show_path_btn = QtWidgets.QPushButton(self.frame)
        self.show_path_btn.setGeometry(QtCore.QRect(462, 80, 40, 31))
        self.show_path_btn.setObjectName("show_path_btn")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("sk.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.show_path_btn.setIcon(icon)
        self.show_path_btn.setIconSize(QSize(40, 40))  # Set icon size
        # Connect the button to the clicked action
        self.show_path_btn.clicked.connect(self.hide_to_show_path)
        self.show_path_btn.setVisible(False)
        
        self.hide_path_btn = QtWidgets.QPushButton(self.frame)
        self.hide_path_btn.setGeometry(QtCore.QRect(462, 80, 40, 31))
        self.hide_path_btn.setObjectName("hide_path_btn")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("skh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.hide_path_btn.setIcon(icon)
        self.hide_path_btn.setIconSize(QSize(40, 40))  # Set icon size
        self.hide_path_btn.clicked.connect(self.show_to_hide_path)
        self.hide_path_btn.setVisible(False)

        self.show_path_btn_rtcm = QtWidgets.QPushButton(self.frame)
        self.show_path_btn_rtcm.setGeometry(QtCore.QRect(462, 130, 40, 31))
        self.show_path_btn_rtcm.setObjectName("show_path_btn_rtcm")
        #self.hide_path_btn.setText("Hide path")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("sk.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.show_path_btn_rtcm.setIcon(icon)
        self.show_path_btn_rtcm.setIconSize(QSize(40, 40))  # Set icon size
        self.show_path_btn_rtcm.clicked.connect(self.hide_to_show_path_rtcm)
        self.show_path_btn_rtcm.setVisible(False)
        self.show_path_btn_rtcm.setEnabled(True)

        self.hide_path_btn_rtcm = QtWidgets.QPushButton(self.frame)
        self.hide_path_btn_rtcm.setGeometry(QtCore.QRect(462, 130, 40, 31))
        self.hide_path_btn_rtcm.setObjectName("hide_path_btn_rtcm")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("skh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.hide_path_btn_rtcm.setIcon(icon)
        self.hide_path_btn_rtcm.setIconSize(QSize(40, 40))  # Set icon size
        self.hide_path_btn_rtcm.clicked.connect(self.show_to_hide_path_rtcm)

        self.hide_path_btn_rtcm.setVisible(False)

        self.label_files_select = QtWidgets.QLabel(self.frame)
        self.label_files_select.setGeometry(QtCore.QRect(440, 465, 10, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_files_select.setFont(font)
        self.label_files_select.setObjectName("label_files_select")
        self.label_files_select.setText("#")
        

        self.comboBox_number_of_files = QtWidgets.QComboBox(self.frame)
        self.comboBox_number_of_files.setGeometry(QtCore.QRect(460, 465, 45, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.comboBox_number_of_files.setFont(font)
        self.comboBox_number_of_files.setObjectName("comboBox_number_of_files")
        self.comboBox_number_of_files.setStyleSheet("""
            QComboBox {
                background-color: #2C3E50;
                color: #FFFFFF;
                border: 2px solid #1ABC9C;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                width: 30px;  # Adjust the width of the drop-down arrow area
                border-left: 2px solid #1ABC9C;
                background-color: #2C3E50;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox::down-arrow:!editable {
                color: #FFFFFF;  # Set the color of the "v"
                text-align: center;
                content: "v";  # Use "v" as the dropdown arrow
            }
            QComboBox::hover {
                background-color: #3A7;
            }
            QComboBox QAbstractItemView {
                background-color: #2E2E2E;  # Match dropdown background with main background
                color: #FFFFFF;  # White text color
                border: 2px solid #1ABC9C;
                selection-background-color: #3A7;  # Color for selected item
            }
        """)
        self.comboBox_number_of_files.addItems([str(i) for i in range(1, 100)])
        self.label_current_file = QtWidgets.QLabel(self.frame)
        self.label_current_file.setGeometry(QtCore.QRect(518, 465, 22, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_current_file.setFont(font)
        self.label_current_file.setObjectName("label_current_file")
        #self.label_current_file.setText("0")
        self.comboBox_number_of_files.currentIndexChanged.connect(self.update_number_of_files)
        self.comboBox_number_of_files.setVisible(False)
        self.label_current_file.setStyleSheet("color: #1ABC9C;") 
        self.label_files_select.setVisible(False)
        self.label_current_file.setVisible(False)
        ########################################################################################################
        self.lineEdit_browse_record = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_browse_record.setGeometry(QtCore.QRect(140, 80, 305, 31))
        self.lineEdit_browse_record.setObjectName("lineEdit_browse_record")
        self.lineEdit_browse_record.setPlaceholderText("Please select the folder")
        self.lineEdit_browse_record.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2C3E50;
                                                        padding: 5px;
                                                        border: 2px solid #1ABC9C;
                                                        border-radius: 5px;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 2px solid #1ABC9C;
                                                    }
                                                    """)
        self.lineEdit_browse_record.setReadOnly(True)

        self.lineEdit_browse_record_rtcm = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_browse_record_rtcm.setGeometry(QtCore.QRect(140, 130, 305, 31))
        self.lineEdit_browse_record_rtcm.setObjectName("lineEdit_browse_record_rtcm")
        self.lineEdit_browse_record_rtcm.setPlaceholderText("Please select the folder")
        self.lineEdit_browse_record_rtcm.setStyleSheet("""
                                                    QLineEdit {
                                                        background-color: #2C3E50;
                                                        padding: 5px;
                                                        border: 2px solid #1ABC9C;
                                                        border-radius: 5px;
                                                    }
                                                    QLineEdit:focus {
                                                        border: 2px solid #1ABC9C;
                                                    }
                                                    """)
        self.lineEdit_browse_record_rtcm.setReadOnly(True)
        self.lineEdit_browse_record_rtcm.setVisible(False)
        
        self.pushButton_browse_record = QtWidgets.QPushButton(self.frame)
        self.pushButton_browse_record.setGeometry(QtCore.QRect(520, 80, 31, 31))
        self.pushButton_browse_record.setObjectName("pushButton_browse_record")
        # Load the SVG file using QSvgRenderer
        svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_browse_record.setIcon(icon)
        self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
        # Connect the button to the clicked action
        self.pushButton_browse_record.clicked.connect(self.browse_folder_Record)
        
        self.pushButton_browse_record_rtcm = QtWidgets.QPushButton(self.frame)
        self.pushButton_browse_record_rtcm.setGeometry(QtCore.QRect(520, 130, 31, 31))
        self.pushButton_browse_record_rtcm.setObjectName("pushButton_browse_record_rtcm")
        svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.pushButton_browse_record_rtcm.setIcon(icon)
        self.pushButton_browse_record_rtcm.setIconSize(QSize(30, 30))  # Set icon size
        #self.pushButton_browse_record_rtcm.setText("Browse..")
        self.pushButton_browse_record_rtcm.clicked.connect(self.browse_folder_Record_rtcm)
        self.pushButton_browse_record_rtcm.setVisible(False)
        self.pushButton_browse_record_rtcm.setEnabled(True)

        # Set text for the buttons
        self.pushButton_6.setText("Stop")
        self.pushButton_7.setText("Start")
        self.lineEdit_7.setPlaceholderText("HH:MM:SS")
        self.lineEdit_2.setPlaceholderText("HH:MM:SS")
        self.lineEdit.setPlaceholderText("Please enter the File name")
        self.lineEdit_8.setReadOnly(False)
        self.lineEdit_8.setPlaceholderText("HH:MM:SS")
        self.label_11.setText("Run time")
        self.label_12.setText("Start time")
        
        self.lineEdit_bandwidth = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_bandwidth.setGeometry(QtCore.QRect(190, 350, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_bandwidth.setFont(font)
        self.lineEdit_bandwidth.setPlaceholderText("")
        self.lineEdit_bandwidth.setObjectName("lineEdit_bandwidth")
        self.lineEdit_bandwidth.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        #########################################################################################
        self.lineEdit_gain_1 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_gain_1.setGeometry(QtCore.QRect(300, 350, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_gain_1.setFont(font)
        self.lineEdit_gain_1.setPlaceholderText("")
        self.lineEdit_gain_1.setObjectName("lineEdit_gain_1")
        self.lineEdit_gain_1.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_gain_1.setVisible(False)
        self.lineEdit_gain_1.setText(default_gain_rx)
        self.lineEdit_gain_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_gain_2.setGeometry(QtCore.QRect(570, 350, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.lineEdit_gain_2.setFont(font)
        self.lineEdit_gain_2.setPlaceholderText("")
        self.lineEdit_gain_2.setObjectName("lineEdit_gain_2")
        self.lineEdit_gain_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_gain_2.setVisible(False)
        self.lineEdit_gain_2.setText(default_gain_rx)
        self.lineEdit_gain_2.setEnabled(True)
        #########################################################################################
        self.pushButton_8.clicked.connect(self.browse_file)
        ########################################  Show and Hide path in replay  ################################################
        self.show_path_btn_replay = QtWidgets.QPushButton(self.frame)
        self.show_path_btn_replay.setGeometry(QtCore.QRect(485, 100, 40, 31))
        self.show_path_btn_replay.setObjectName("show_path_btn_replay")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("sk.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.show_path_btn_replay.setIcon(icon)
        self.show_path_btn_replay.setIconSize(QSize(40, 40))  # Set icon size
        self.show_path_btn_replay.clicked.connect(self.hide_to_show_path)
        self.show_path_btn_replay.setVisible(False)
        self.hide_path_btn_replay = QtWidgets.QPushButton(self.frame)
        self.hide_path_btn_replay.setGeometry(QtCore.QRect(485, 100, 40, 31))
        self.hide_path_btn_replay.setObjectName("hide_path_btn_replay")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("skh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.hide_path_btn_replay.setIcon(icon)
        self.hide_path_btn_replay.setIconSize(QSize(40, 40))  # Set icon size
        self.hide_path_btn_replay.clicked.connect(self.show_to_hide_path)       
        self.hide_path_btn_replay.setVisible(False)
        self.show_path_btn_replay_rtcm = QtWidgets.QPushButton(self.frame)
        self.show_path_btn_replay_rtcm.setGeometry(QtCore.QRect(485, 150, 40, 31))
        self.show_path_btn_replay_rtcm.setObjectName("show_path_btn_replay")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("sk.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.show_path_btn_replay_rtcm.setIcon(icon)
        self.show_path_btn_replay_rtcm.setIconSize(QSize(40, 40))  # Set icon size
        self.show_path_btn_replay_rtcm.clicked.connect(self.hide_to_show_path_rtcm)
        self.show_path_btn_replay_rtcm.setVisible(False)
        self.hide_path_btn_replay_rtcm = QtWidgets.QPushButton(self.frame)
        self.hide_path_btn_replay_rtcm.setGeometry(QtCore.QRect(485, 150, 40, 31))
        self.hide_path_btn_replay_rtcm.setObjectName("hide_path_btn_replay")
        #self.hide_path_btn.setText("Hide path")
        svg_renderer = QSvgRenderer("skh.svg")  # Replace with your SVG image path
        # Create a QPixmap and render the SVG onto it
        pixmap = QPixmap(45, 45)  # Set the size of the icon
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
        # Use QPainter to render the SVG on the QPixmap
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        # Set the rendered SVG as the icon for the QPushButton
        icon = QIcon(pixmap)
        self.hide_path_btn_replay_rtcm.setIcon(icon)
        self.hide_path_btn_replay_rtcm.setIconSize(QSize(40, 40))  # Set icon size
        self.hide_path_btn_replay_rtcm.clicked.connect(self.show_to_hide_path_rtcm)       
        self.hide_path_btn_replay_rtcm.setVisible(False)
        #############################################################################################################
        self.lineEdit9.setPlaceholderText("Please select the file")
        self.label_13.setText("AD9361")
        self.pushButton_7.clicked.connect(self.start_timer_replay)
        self.pushButton_6.clicked.connect(self.stop_timer_replay)
        self.pushButton_submit.clicked.connect(self.connectivity_done)
        self.selected_adc_bits2 = None
        self.selected_adc_bits1 = None
        self.file_name = None
        self.folder_name_rtcm = None
        self.number_of_files = 1
        self.baudrate = "115200"
        self.comport = None
        self.baudrate_rtcm = "115200"
        self.reference_frequency = "0"
        self.comport_rtcm = None
        self.duration_value = None
        self.selected_center_frequency1 = None
        self.selected_center_frequency1 = None
        self.start_time_value = None
        self.stop_time_value = None
        self.rate = None
        self.file_name_replay = None
        self.file_name_replay_rtcm = None
        self.bandwidth = None
        self.bandwidth_2 = None
        self.fs_system_GUI = None
        self.folder_name_record = None
        self.folder_name_record_rtcm = None
        self.samplingfreq_1 = None
        self.samplingfreq_2 = None
        self.progressrecording = None
        self.progressreplay = None
        self.lineEdit_6.textChanged.connect(self.get_recording_progress)
        self.lineEdit_replay.textChanged.connect(self.get_replay_progress)
        self.lineEdit_samplingfreq_2.textChanged.connect(self.get_samplingfreq_2)
        #self.lineEdit_samplingfreq_2.textChanged.connect(self.get_max_duration)
        self.lineEdit_samplingfreq.textChanged.connect(self.get_samplingfreq)
        #self.lineEdit_samplingfreq.textChanged.connect(self.get_max_duration)
        self.lineEdit_browse_record.textChanged.connect(self.get_folder_name)
        self.lineEdit_browse_record_rtcm.textChanged.connect(self.get_folder_name_rtcm)
        self.lineEdit9.textChanged.connect(self.get_file_name)
        self.lineEdit_replay_rtcm.textChanged.connect(self.get_file_name_rtcm)
        self.lineEdit_8.textChanged.connect(self.get_start_time)
        self.lineEdit_7.textChanged.connect(self.get_stop_time)
        self.lineEdit_rate.textChanged.connect(self.get_Rate)
        self.lineEdit_bandwidth.textChanged.connect(self.update_bandwidth)
        self.lineEdit_bandwidth_2.textChanged.connect(self.update_bandwidth_2)
        self.lineEdit_fs_system.textChanged.connect(self.update_fs_system)
        # Connect signals to update selected values
        #####################################################################
        self.comboBox.currentIndexChanged.connect(self.update_adc_bits1)
       # self.comboBox.currentIndexChanged.connect(self.get_max_duration)
        #####################################################################
        self.comboBox_2.currentIndexChanged.connect(self.update_adc_bits2)
       # self.comboBox_2.currentIndexChanged.connect(self.get_max_duration)
        self.comboBox_comport.currentIndexChanged.connect(self.get_comport)
        self.comboBox_baudrate.currentIndexChanged.connect(self.get_baudrate)
        self.comboBox_comport_rtcm.currentIndexChanged.connect(self.get_comport_rtcm)
        self.comboBox_baudrate_rtcm.currentIndexChanged.connect(self.get_baudrate_rtcm)
        self.comboBox_ref_freq.currentIndexChanged.connect(self.get_ref_freq)
        self.lineEdit.textChanged.connect(self.update_file_name)
        self.lineEdit_2.textChanged.connect(self.get_duration)
        self.lineEdit_3.textChanged.connect(self.upate_center_frequency1)
        self.lineEdit_4.textChanged.connect(self.upate_center_frequency2)
        self.radioButton_gpiomode.toggled.connect(self.handle_radio_button_rfmdmode)
        self.radioButton_rtcm.toggled.connect(self.handle_radio_button_rtcm)
        self.radioButton_ad9361.toggled.connect(self.handle_radio_button_ad9361)

        self.pushButton_6.setVisible(False)
        self.pushButton_7.setVisible(False)
        self.lineEdit_7.setVisible(False)
        self.lineEdit_8.setVisible(False)
        self.label_11.setVisible(False)
        self.label_12.setVisible(False)
        self.radioButton_GPIO_Replay.setVisible(False)
        self.pushButton_8.setVisible(False)
        self.lineEdit9.setVisible(False)
        self.lineEdit_replay_rtcm.setVisible(False)
        self.pushButton_browse_replay_rtcm.setVisible(False)
        self.label_files_rtcm.setVisible(False)
        self.label_13.setVisible(False)
        self.label_about_2.setVisible(False)
        self.label_about_3.setVisible(False)
        self.lineEdit_replay.setVisible(False)
        self.label_replay.setVisible(False)
        self.pushButton.setVisible(False)
        self.pushButton_2.setVisible(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setVisible(False)
        self.pushButton_4.setVisible(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setVisible(True)
        self.pushButton_5.setEnabled(True)
        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.lineEdit_4.setVisible(False)
        self.lineEdit_6.setVisible(False)
        self.label.setVisible(False)
        self.label_10.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_8.setVisible(False)
        self.label_9.setVisible(False)
        self.comboBox.setVisible(False)
        self.comboBox_2.setVisible(False)
        self.lineEdit9.setReadOnly(True)
        self.label_about_2.setVisible(False)
        self.label_about_3.setVisible(False)
        self.label_bandwidth.setVisible(False)
        self.label_gain.setVisible(False)
        self.lineEdit_bandwidth.setVisible(False)
        self.lineEdit_gain_1.setVisible(False)
        self.lineEdit_gain_2.setVisible(False)
        self.lineEdit_bandwidth_2.setVisible(False)
        self.line_2.setVisible(False)
        self.pushButton_login.setEnabled(False)
        self.line_record.setVisible(False)
        self.line_vertical.setVisible(False)
        self.line_vertical_2.setVisible(False)
        self.label_browse_record.setVisible(False)
        self.label_browse_record_rtcm.setVisible(False)
        self.radioButton_GPIO_Record.setVisible(False)
        self.lineEdit_browse_record.setVisible(False)
        self.lineEdit_browse_record_rtcm.setVisible(False)
        self.pushButton_browse_record.setVisible(False)
        self.pushButton_browse_record_rtcm.setVisible(False)
        self.red_light.setVisible(False)
        self.green_light.setVisible(False)
        self.red_light_record.setVisible(False)
        self.green_light_record.setVisible(False)
        self.label_sampling.setVisible(False)
        self.label_samplingfreq.setVisible(False)
        self.lineEdit_samplingfreq.setVisible(False)
        self.lineEdit_samplingfreq_2.setVisible(False)
        self.radioButton_Rx_1.setVisible(False)
        self.radioButton_Rx_2.setVisible(False)
        self.comboBox_comport_rtcm.currentIndexChanged.connect(self.on_rtcm_dropdown)
        self.comboBox_comport.currentIndexChanged.connect(self.on_comport_dropdown)
        self.comboBox.currentIndexChanged.connect(self.on_selection_change)
        self.comboBox_2.currentIndexChanged.connect(self.on_selection_change_2)
    
    def comboBox_comport_popup(self):
        global current_port
        print("Hi")
        current_port = self.comport
        self.update_com_ports()
        if present:
            self.comboBox_comport.setCurrentText(current_port)
        else:
            self.comboBox_comport.setCurrentText(current_port)
        QComboBox.showPopup(self.comboBox_comport)  # Call the original showPopup method

    def comboBox_comport_rtcm_popup(self):
        global current_port_rtcm
        print("Hi")
        current_port_rtcm = self.comport_rtcm
        self.update_com_ports_rtcm()
        if present:
            self.comboBox_comport_rtcm.setCurrentText(current_port_rtcm)
        else:
            self.comboBox_comport_rtcm.setCurrentText(current_port_rtcm)
        QComboBox.showPopup(self.comboBox_comport_rtcm)  # Call the original showPopup method
    
    def size_after_minus_x(self, size_in_bytes, adc_bits, sf, seconds_to_subtract, size_to_subtract_mb,channels=1):
        try:
            adc_bits = int(adc_bits)
            sf = float(sf)
            channels = int(channels)
            if sf == 0 or channels < 1:
                return None
            
            Bytes_perSample_single = (adc_bits * 2) / 8
            Bytes_perSample = Bytes_perSample_single * channels
            
            sampling_frequency_in_hz = sf * 1e6
            
            # current duration
            duration = size_in_bytes / (sampling_frequency_in_hz * Bytes_perSample)
            
            # new duration after subtracting `seconds_to_subtract`
            new_duration = max(0, duration - seconds_to_subtract)
            
            if new_duration == 0:
                return 0  # explicitly return 0 if no time left
            
            # calculate new size
            new_size_in_bytes = new_duration * sampling_frequency_in_hz * Bytes_perSample
            
            # Getting into the GPIO
            print(f"Size before subtracting {size_to_subtract_mb} MB: {new_size_in_bytes} bytes")
            size_to_subtract_bytes = size_to_subtract_mb * 1024 * 1024
            final_size_in_bytes = max(0, new_size_in_bytes - size_to_subtract_bytes)
            print(f"Size after subtracting {size_to_subtract_mb} MB: {final_size_in_bytes} bytes")
            
            return final_size_in_bytes
            
        except (ValueError, ZeroDivisionError):
            return None
        
    def get_max_duration_theorotical(self):
        global available_memory, ser, main_func_called, SSD_free_space

        if recording_started:
            return

        main_func_called = False
        if not interface_is_online(self.comport):
            return

        print(fs_system)
        self.label_SSD_capacity.setVisible(True)
        self.label_available_Duration.setVisible(True)

        available_memory = SSD_free_space
        if SSD_free_space is None:
            self.label_SSD_capacity.setText("Free SSD: Not found")
            self.label_available_Duration.setText("Max Duration: Not found")
            print("Free SSD: Not found")
            return

        size_in_bytes_1 = convert_size(int(SSD_free_space))

        if SSD_free_space is not None:
            self.label_SSD_capacity.setText(f"Free SSD: {size_in_bytes_1}")
        else:
            self.label_SSD_capacity.setText("Free SSD: Not found")

        if not SSD_free_space:
            self.label_available_Duration.setText("Max Duration: Not found")
            return

        def calculate_duration(adc_bits, sf):
            global duration_available_for_recording
            try:
                adc_bits = int(adc_bits)
                sf = float(sf)
                if sf == 0:
                    return None
                Bytes_perSample = (adc_bits * 2) / 8
                sampling_frequency_in_mega = sf * 1e6
                duration = SSD_free_space / (sampling_frequency_in_mega * Bytes_perSample)
                duration_available_for_recording = second_to_hhmmss(math.floor(duration))
                return duration_available_for_recording
            except (ValueError, ZeroDivisionError):
                return None

        if self.radioButton_single.isChecked():
            if rx1_checked:
                if self.selected_adc_bits1 and self.samplingfreq_1:
                    duration = calculate_duration(self.selected_adc_bits1, self.samplingfreq_1)
                    if duration:
                        self.label_available_Duration.setText(f"Max Duration: {duration}")
                    else:
                        self.label_available_Duration.setText("Max Duration: ")
                else:
                    self.label_available_Duration.setText("Max Duration: ")

            elif rx2_checked:
                if self.selected_adc_bits2 and self.samplingfreq_2:
                    if str(self.selected_adc_bits2) != "Select" and str(self.samplingfreq_2) != "":
                        if int(self.selected_adc_bits2) not in [4, 8, 16]:
                            self.label_available_Duration.setText("Max Duration: ")
                            return
                        duration = calculate_duration(self.selected_adc_bits2, self.samplingfreq_2)
                        if duration:
                            self.label_available_Duration.setText(f"Max Duration: {duration}")
                        else:
                            self.label_available_Duration.setText("Max Duration: ")
                    else:
                        self.label_available_Duration.setText("Max Duration: ")
                else:
                    self.label_available_Duration.setText("Max Duration: ")

        elif self.radioButton_double.isChecked():
            if all([self.selected_adc_bits1, self.samplingfreq_1, self.selected_adc_bits2, self.samplingfreq_2]):
                sf1 = self.lineEdit_samplingfreq.text()
                try:
                    sf1 = float(sf1)
                    if sf1 == 0:
                        return
                    Bytes_perSample = (int(self.selected_adc_bits1) * 2) / 8
                    duration = SSD_free_space / (sf1 * 1e6 * Bytes_perSample)
                    duration /= 2
                    duration = second_to_hhmmss(math.floor(duration))
                    self.label_available_Duration.setText(f"Max Duration: {duration}")
                except (ValueError, ZeroDivisionError):
                    self.label_available_Duration.setText("Max Duration: ")
            else:
                self.label_available_Duration.setText("Max Duration: ")

    
    def get_max_duration(self):
        global available_memory, ser, main_func_called, SSD_free_space

        if recording_started:
            return

        main_func_called = False
        bs = read_lines()
        if not interface_is_online(self.comport):
            return

        print(fs_system)
        self.label_SSD_capacity.setVisible(True)
        self.label_available_Duration.setVisible(True)

        size_in_bytes = get_memory_available(fs_system)
        print(size_in_bytes)

        if size_in_bytes is None:
            SSD_free_space = None
            self.label_SSD_capacity.setText("Free SSD: Not found")
            self.label_available_Duration.setText("Max Duration: Not found")
            return
    
        if Commands_file_user:
            with open(file_path_to_read_response, 'a') as file:
                file.write(f'{get_current_datetime()} :Size in bytes\n')
                file.write(f'{get_current_datetime()}   {size_in_bytes}\n\n')

        available_memory = size_in_bytes
        if (HW_USB_in_use):
            size_in_bytes = size_in_bytes-HW_USB_Size
        size_in_bytes_1 = convert_size(size_in_bytes)

        if size_in_bytes is not None:
            SSD_free_space = size_in_bytes
            self.label_SSD_capacity.setText(f"Free SSD: {size_in_bytes_1}")
        else:
            self.label_SSD_capacity.setText("Free SSD: Not found")
            SSD_free_space = None

        if not size_in_bytes:
            self.label_available_Duration.setText("Max Duration: Not found")
            return

        def calculate_duration(adc_bits, sf):
            global duration_available_for_recording
            try:
                adc_bits = int(adc_bits)
                sf = float(sf)
                if sf == 0:
                    return None
                Bytes_perSample = (adc_bits * 2) / 8
                sampling_frequency_in_mega = sf * 1e6
                duration = size_in_bytes / (sampling_frequency_in_mega * Bytes_perSample)
                duration_available_for_recording = second_to_hhmmss(math.floor(duration))
                return duration_available_for_recording
            except (ValueError, ZeroDivisionError):
                return None

        if self.radioButton_single.isChecked():
            if rx1_checked:
                if self.selected_adc_bits1 and self.samplingfreq_1:
                    duration = calculate_duration(self.selected_adc_bits1, self.samplingfreq_1)
                    if duration:
                        self.label_available_Duration.setText(f"Max Duration: {duration}")
                    else:
                        self.label_available_Duration.setText("Max Duration: ")
                else:
                    self.label_available_Duration.setText("Max Duration: ")

            elif rx2_checked:
                if self.selected_adc_bits2 and self.samplingfreq_2:
                    if str(self.selected_adc_bits2) != "Select" and str(self.samplingfreq_2) != "":
                        if int(self.selected_adc_bits2) not in [4, 8, 16]:
                            self.label_available_Duration.setText("Max Duration: ")
                            return
                        duration = calculate_duration(self.selected_adc_bits2, self.samplingfreq_2)
                        if duration:
                            self.label_available_Duration.setText(f"Max Duration: {duration}")
                        else:
                            self.label_available_Duration.setText("Max Duration: ")
                    else:
                        self.label_available_Duration.setText("Max Duration: ")
                else:
                    self.label_available_Duration.setText("Max Duration: ")

        elif self.radioButton_double.isChecked():
            if all([self.selected_adc_bits1, self.samplingfreq_1, self.selected_adc_bits2, self.samplingfreq_2]):
                sf1 = self.lineEdit_samplingfreq.text()
                try:
                    sf1 = float(sf1)
                    if sf1 == 0:
                        return
                    Bytes_perSample = (int(self.selected_adc_bits1) * 2) / 8
                    duration = size_in_bytes / (sf1 * 1e6 * Bytes_perSample)
                    duration /= 2
                    duration = second_to_hhmmss(math.floor(duration))
                    self.label_available_Duration.setText(f"Max Duration: {duration}")
                except (ValueError, ZeroDivisionError):
                    self.label_available_Duration.setText("Max Duration: ")
            else:
                self.label_available_Duration.setText("Max Duration: ")


    def show_tx_1(self):
        self.lineEdit_Gain_Tx.setEnabled(True)
        self.lineEdit_Gain_Tx_2.setEnabled(False)
        self.lineEdit_Gain_Tx.setText(default_gain_tx)
        self.lineEdit_Gain_Tx_2.setText("")
        self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
    def show_tx_2(self):
        self.lineEdit_Gain_Tx.setEnabled(False)
        self.lineEdit_Gain_Tx_2.setEnabled(True)
        self.lineEdit_Gain_Tx_2.setText(default_gain_tx)
        self.lineEdit_Gain_Tx.setText("")
        self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """) 
    def show_popup(self):
      global rx1_checked, rx2_checked
      if self.radioButton_Rx_1.isChecked():
            rx1_checked = True
            rx2_checked = False
            self.lineEdit_gain_2.setText("")
            self.lineEdit_gain_1.setText(default_gain_rx)
            self.lineEdit_3.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.lineEdit_gain_1.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.lineEdit_bandwidth.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #2E5;
                                            }
                                        """)
            self.lineEdit_samplingfreq.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #2E5;
                                            }
                                        """)
            self.comboBox.setStyleSheet("""
                    QComboBox {
                        background-color: #2C3E50;
                        color: #FFFFFF;
                        border: 2px solid #1ABC9C;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QComboBox::drop-down {
                        width: 30px;  # Adjust the width of the drop-down arrow area
                        border-left: 2px solid #1ABC9C;
                        background-color: #2C3E50;
                    }
                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox::down-arrow:!editable {
                        color: #FFFFFF;  # Set the color of the "v"
                        text-align: center;
                        content: "v";  # Use "v" as the dropdown arrow
                    }
                    QComboBox::hover {
                        background-color: #3A7;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2E2E2E;  # Match dropdown background with main background
                        color: #FFFFFF;  # White text color
                        border: 2px solid #1ABC9C;
                        selection-background-color: #3A7;  # Color for selected item
                    }
                """)
            self.lineEdit_4.clear()
            #self.comboBox_2.clear()
            self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_bandwidth_2.clear()
            self.lineEdit_samplingfreq_2.clear()

            self.lineEdit_4.setEnabled(False)
            self.lineEdit_3.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(False)
            self.lineEdit_gain_1.setEnabled(True)
            self.lineEdit_gain_2.setEnabled(False)
            self.lineEdit_bandwidth.setEnabled(True)
            self.lineEdit_bandwidth_2.setEnabled(False)
            self.lineEdit_samplingfreq.setEnabled(True)
            self.lineEdit_samplingfreq_2.setEnabled(False)
            self.lineEdit_gain_1.setEnabled(True)
            self.lineEdit_gain_2.setEnabled(False)
            self.lineEdit_4.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.lineEdit_gain_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.lineEdit_bandwidth_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.lineEdit_samplingfreq_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
            self.comboBox_2.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)

    def show_popup_2(self):
      global rx1_checked, rx2_checked
      if self.radioButton_Rx_2.isChecked(): 
        rx1_checked = False
        rx2_checked = True
        self.lineEdit_gain_1.setText("")
        self.lineEdit_gain_2.setText(default_gain_rx)

        self.lineEdit_4.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_gain_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_bandwidth_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_samplingfreq_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.comboBox_2.setStyleSheet("""
                QComboBox {
                    background-color: #2C3E50;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #2C3E50;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)

        self.lineEdit_3.clear()
          #self.comboBox.clear()
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_bandwidth.clear()
        self.lineEdit_samplingfreq.clear()

        self.lineEdit_4.setEnabled(True)
        self.lineEdit_3.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(True)
        self.lineEdit_gain_1.setEnabled(False)
        self.lineEdit_gain_2.setEnabled(True)
        self.lineEdit_bandwidth.setEnabled(False)
        self.lineEdit_bandwidth_2.setEnabled(True)
        self.lineEdit_samplingfreq.setEnabled(False)
        self.lineEdit_samplingfreq_2.setEnabled(True)
        self.lineEdit_gain_1.setEnabled(False)
        self.lineEdit_gain_2.setEnabled(True)
        self.lineEdit_3.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_gain_1.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_bandwidth.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_samplingfreq.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.comboBox.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)

    def on_comport_dropdown(self, index):
        item = self.comboBox_comport.currentText()
        if item == WIFI_INTERFACE_OPTION:
            self.lineEdit_hostname.setVisible(True)
            self.label_ssid.setVisible(True)
            self.lineEdit_password.setVisible(False)
            self.label_hostname.setVisible(True)
        else:
            self.lineEdit_hostname.setVisible(False)
            self.label_ssid.setVisible(False)
            self.lineEdit_password.setVisible(False)
            self.label_hostname.setVisible(False)

    def on_rtcm_dropdown(self, index):
        item = self.comboBox_comport_rtcm.currentText()
        if item == "HW USB":
            self.lineEdit_deviceid.setVisible(True)
            self.label_deviceid.setVisible(True)
            self.lineEdit_busno.setVisible(True)
            self.label_busno.setVisible(True)
            self.pushButton_usb_info.setVisible(True)
        else:
            self.lineEdit_deviceid.setVisible(False)
            self.label_deviceid.setVisible(False)
            self.lineEdit_busno.setVisible(False)
            self.label_busno.setVisible(False)
            self.pushButton_usb_info.setVisible(False)

    def on_selection_change(self, index):
            self.get_max_duration_theorotical()
            global comport_1_checked, comport_2_checked 
            print("hi")
            selected_item = self.comboBox.currentText()
            if not comport_2_checked:
                if self.radioButton_double.isChecked():
                    if selected_item:
                        comport_1_checked = True
                        self.comboBox_2.setCurrentText(selected_item)
                        print("hi-1")
                        if (selected_item) == "4":
                            print("hi-11")
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Maximum Values!")
                            msg_box_11.setText(f"Maximum Sampling Frequency: {round((61.44)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9 * 61.44) / 2, 2)}MHz")
                            msg_box_11.exec()
                            comport_1_checked = False
                            return
                        if (selected_item) == "8":
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Maximum Values!")
                            msg_box_11.setText(f"Maximum Sampling Frequency: {round((48)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9*48)/2, 2)}MHz")
                            msg_box_11.exec()
                            comport_1_checked = False
                            return
                        if (selected_item) == "16":
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Maximum Values!")
                            msg_box_11.setText(f"Maximum Sampling Frequency: {round((24)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9*24)/2, 2)}MHz")
                            msg_box_11.exec()
                            comport_1_checked = False
                            return
                    

            if self.radioButton_single.isChecked():
                print("hi-2")
                if selected_item:
                    if (selected_item) == "4":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 61.44MHz\nMaximum Bandwidth: {round((0.9 * 61.44), 2)}MHz")
                        msg_box_11.exec()
                        return
                    if (selected_item) == "8":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 48MHz\nMaximum Bandwidth: {round((0.9 * 48), 2)}MHz")
                        msg_box_11.exec()
                        return
                    if (selected_item) == "16":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 24MHz\nMaximum Bandwidth: {round((0.9 * 24), 2)}MHz")
                        msg_box_11.exec()
                        return
                
    def on_selection_change_2(self, index):
            self.get_max_duration_theorotical()
            global comport_1_checked, comport_2_checked
            print("hi2")
            selected_item = self.comboBox_2.currentText()

            if not comport_1_checked:
                if self.radioButton_double.isChecked():
                    comport_2_checked = True
                    self.comboBox.setCurrentText(selected_item)
                    if comport_2_checked:
                        if selected_item:
                            if (selected_item) == "4":
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Maximum Values!")
                                msg_box_11.setText(f"Maximum Sampling Frequency: {round((61.44)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9 * 61.44) / 2, 2)}MHz")
                                msg_box_11.exec()
                                comport_2_checked = False
                                return
                            if (selected_item) == "8":
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Maximum Values!")
                                msg_box_11.setText(f"Maximum Sampling Frequency: {round((48)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9*48)/2, 2)}MHz")
                                msg_box_11.exec()
                                comport_2_checked = False
                                return
                            if (selected_item) == "16":
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Maximum Values!")
                                msg_box_11.setText(f"Maximum Sampling Frequency: {round((24)/2, 2)}MHz\nMaximum Bandwidth: {round((0.9*24)/2, 2)}MHz")
                                msg_box_11.exec()
                                comport_2_checked = False
                                return


            if self.radioButton_single.isChecked():
                if selected_item:
                    if (selected_item) == "4":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 61.44MHz\nMaximum Bandwidth: {round(0.9*61.44, 2)}MHz")
                        msg_box_11.exec()
                        return
                    if (selected_item) == "8":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 48MHz\nMaximum Bandwidth: {round(0.9*48, 2)}MHz")
                        msg_box_11.exec()
                        return
                    if (selected_item) == "16":
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Maximum Values!")
                        msg_box_11.setText(f"Maximum Sampling Frequency: 24MHz\nMaximum Bandwidth: {round(0.9*24, 2)}MHz")
                        msg_box_11.exec()
                        return

    def filter_rtcm_messages(self):
        try:
            with open(rtcm_create_file, 'wb') as file_rtcm:
                last_stamp = time.time()
                
                # Write initial timestamp
                timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-3] + "]\n"
                file_rtcm.write(timestamp.encode())
                file_rtcm.flush()
                
                print(f"Started recording RTCM data with timestamps to {rtcm_create_file}")
                
                while self.running:
                    current_time = time.time()
                    
                    # Write timestamp every second
                    if current_time - last_stamp >= 1.0:
                        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")[:-3] + "]\n"
                        file_rtcm.write(timestamp.encode())
                        file_rtcm.flush()
                        last_stamp = current_time
                    
                    try:
                        # Read directly from serial port
                        if ser_rtcm.in_waiting > 0:
                            raw_data = ser_rtcm.read(ser_rtcm.in_waiting)
                            if raw_data:
                                # Write raw RTCM data to file
                                file_rtcm.write(raw_data)
                                file_rtcm.flush()
                        else:
                            # Small sleep when no data
                            time.sleep(0.01)
                            
                    except Exception as e:
                        time.sleep(0.1)
                                    
        except Exception as e:
            print(f"Error in RTCM recording: {e}")
        finally:
            self.running = False
            print("RTCM recording stopped.")

        
    def start_reading(self):
        global _variable
        if not self.running:
            print("hii")
            self.running = True
            _variable = True
            self.thread = threading.Thread(target=self.filter_rtcm_messages, daemon=True)
            self.thread.start()

    def stop_reading(self):
        global _variable
        self.running = False
        _variable = False
        if self.port and self.port.is_open:
            self.port.close()

    def stop_sending(self):
        self.is_sending = False
        if ser_rtcm and ser_rtcm.isOpen():
            ser_rtcm.close()

    def send_data(self):
        """
        Send exactly int(duration * rate) blocks.
        - Each block = bytes between two timestamp headers in the .rtcm file.
        - Loops (wraps) over intervals if the file provides fewer than needed.
        - Uses absolute pacing so wall-clock ~= duration.
        """
        global ser_rtcm, rtcm_file_path, timeout_time, startoffset_auto, duration_auto
        print("\n=== STARTING DATA TRANSMISSION ===")
        # Close any pre-existing serial
        try:
            if ser_rtcm and ser_rtcm.isOpen():
                ser_rtcm.close()
        except Exception:
            pass

        # UI params
        rate = float(self.lineEdit_rate.text())
        time_delay = 1.0 / rate if rate > 0 else 0.0
        start_offset = int(startoffset_auto)
        run_duration = int(duration_auto)

        print(f"time_delay: {time_delay}, start_offset: {start_offset}, run_duration: {run_duration}")
        print(f"Starting data transmission…")
        print(f"RTCM file path: {rtcm_file_path}")

        try:
            file_size = os.path.getsize(rtcm_file_path)
            print(f"File size: {file_size} bytes")

            with open(rtcm_file_path, 'rb') as fbin:
                buf = fbin.read()

            # Robust timestamp regex: allows ' ' or 'T' between date and time, microseconds 1..6 digits
            ts_re = re.compile(
                rb"\[(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})\.(\d{1,6})\]",
                re.MULTILINE,
            )
            matches = list(ts_re.finditer(buf))
            print(f"Found {len(matches)} timestamps in file.")
            if len(matches) < 2:
                print("❌ Not enough timestamp headers (need at least 2 to form one interval).")
                self.is_sending = False
                return

            # Build intervals between consecutive headers
            intervals = []
            for i in range(len(matches) - 1):
                head = matches[i]
                nxt  = matches[i + 1]
                start_payload = head.end()
                end_payload   = nxt.start()
                if end_payload > start_payload:
                    header_us = self._ts_groups_to_us_bytes(head.groups())
                    intervals.append((start_payload, end_payload, header_us))

            if not intervals:
                print("❌ No non-empty intervals found between timestamps.")
                self.is_sending = False
                return

            # Apply start_offset (seconds) relative to first header
            first_header_us = self._ts_groups_to_us_bytes(matches[0].groups())
            start_offset_us = start_offset * 1_000_000
            filtered = [(a, b, t) for (a, b, t) in intervals if (t - first_header_us) >= start_offset_us]
            if not filtered:
                print("⚠️ No intervals at/after the requested start offset.")
                self.is_sending = False
                return

            # How many blocks to send (exact)
            blocks_to_send = int(run_duration * rate)
            if blocks_to_send <= 0:
                print("⚠️ Computed 0 blocks to send; exiting.")
                self.is_sending = False
                return

            # Open serial and transmit with absolute pacing + looping
            with serial.Serial(self.comport_rtcm, self.baudrate_rtcm, timeout=timeout_time) as ser:
                transmission_start = time.time()
                bytes_sent = 0
                block_count = 0

                n_intervals = len(filtered)
                print(f"Usable intervals after offset: {n_intervals}. Target blocks: {blocks_to_send}")

                for k in range(blocks_to_send):
                    if not self.is_sending:
                        break

                    # Loop over intervals if needed
                    idx = k % n_intervals
                    start_payload, end_payload, header_us = filtered[idx]
                    payload = buf[start_payload:end_payload]

                    # Send block
                    send_command(payload)
                    ser.flush()

                    block_count += 1
                    bytes_sent += len(payload)
                    print(f"📦 Sent block {block_count}/{blocks_to_send} "
                        f"({len(payload)} bytes, timestamp_us={header_us})")

                    # Absolute pacing to avoid drift: schedule next send at start + (k+1)/rate
                    if k < blocks_to_send - 1 and rate > 0:
                        next_deadline = transmission_start + (k + 1) / rate
                        remaining = next_deadline - time.time()
                        if remaining > 0:
                            time.sleep(remaining)

                elapsed = time.time() - transmission_start
                print("\n=== TRANSMISSION COMPLETED ===")
                print(f"Blocks sent: {block_count}")
                print(f"Total bytes sent: {bytes_sent}")
                print(f"Elapsed: {elapsed:.2f}s  (target ≈ {blocks_to_send / max(rate,1):.2f}s)")
                if elapsed > 0:
                    print(f"Avg throughput: {bytes_sent/elapsed:.2f} B/s")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

        self.is_sending = False



    def _ts_groups_to_us_bytes(self, m_groups):
        """
        Convert timestamp regex groups (bytes) → epoch microseconds UTC.
        """
        from datetime import datetime, timezone
        try:
            Y, Mo, D, hh, mm, ss, us = (int(g) for g in m_groups)
        except Exception:
            Y, Mo, D, hh, mm, ss, us = (0, 0, 0, 0, 0, 0, 0)
        if us > 999999:
            us = int(str(us)[:6])
        dt = datetime(Y, Mo, D, hh, mm, ss, us, tzinfo=timezone.utc)
        return int(dt.timestamp() * 1_000_000)





    
        
    def update_file_name(self, text):
        self.file_name = text.strip()

    def get_comport(self, index):
        global comport
        self.comport = self.comboBox_comport.itemText(index)
        comport = self.comport
        self.update_wifi_interface_state()

    def get_baudrate(self, index):
        self.baudrate = self.comboBox_baudrate.itemText(index)

    def get_comport_rtcm(self, index):
        self.comport_rtcm = self.comboBox_comport_rtcm.itemText(index)

    def get_baudrate_rtcm(self, index):
        self.baudrate_rtcm = self.comboBox_baudrate_rtcm.itemText(index)

    def get_ref_freq(self, index):
        self.reference_frequency_raw = self.comboBox_ref_freq.itemText(index)
        if self.reference_frequency_raw == "AD9361 (single CH)":
            self.reference_frequency = "0"
        else:
            self.reference_frequency = str(str(self.reference_frequency_raw).split("MHz")[0].strip())
        print(self.reference_frequency)

    def get_file_name(self, text):
        self.file_name_replay = text.strip()

    def get_file_name_rtcm(self, text):
        self.file_name_replay_rtcm = text.strip()

    def get_folder_name(self, text):
        self.folder_name_record = text.strip()
    
    def get_folder_name_rtcm(self, text):
        self.folder_name_record_rtcm = text.strip()

    def update_bandwidth(self, text):
        self.bandwidth = text.strip()
    
    def update_bandwidth_2(self, text):
        self.bandwidth_2 = text.strip()

    def update_fs_system(self, text):
        self.fs_system_GUI = text.strip()

    def upate_center_frequency1(self, text):
        self.selected_center_frequency1 = text.strip()
        if self.radioButton_double.isChecked() and self.reference_frequency == "0":
            self.lineEdit_4.setText(self.selected_center_frequency1)

    def upate_center_frequency2(self, text):
        self.selected_center_frequency2 = text.strip()
        if self.radioButton_double.isChecked() and self.reference_frequency == "0":
            self.lineEdit_3.setText(self.selected_center_frequency2)

    def get_duration(self, text):
        self.duration_value = text.strip()

    def update_adc_bits1(self, index):
        self.selected_adc_bits1 = self.comboBox.itemText(index)

    def update_adc_bits2(self, index):
        self.selected_adc_bits2 = self.comboBox_2.itemText(index)
    
    def update_number_of_files(self, index):
        self.number_of_files = self.comboBox_number_of_files.itemText(index)

    def handle_radio_button_rfmdmode(self, checked):
        print("rfmd mode selected")
        if checked:
            self.comboBox_ref_freq.setEnabled(False)
            self.update_ref_freq()
            self.comboBox_ref_freq.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
            
        else: 
            self.comboBox_ref_freq.setEnabled(True)
            self.comboBox_ref_freq.setStyleSheet("""
                                        QComboBox {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QComboBox::drop-down {
                                            width: 30px;  # Adjust the width of the drop-down arrow area
                                            border-left: 2px solid #1ABC9C;
                                            background-color: #2C3E50;
                                        }
                                        QComboBox::down-arrow {
                                            width: 12px;
                                            height: 12px;
                                        }
                                        QComboBox::down-arrow:!editable {
                                            color: #FFFFFF;  # Set the color of the "v"
                                            text-align: center;
                                            content: "v";  # Use "v" as the dropdown arrow
                                        }
                                        QComboBox::hover {
                                            background-color: #3A7;
                                        }
                                        QComboBox QAbstractItemView {
                                            background-color: #2E2E2E;  # Match dropdown background with main background
                                            color: #FFFFFF;  # White text color
                                            border: 2px solid #1ABC9C;
                                            selection-background-color: #3A7;  # Color for selected item
                                        }
                                    """)
            

    def handle_radio_button_rtcm(self, checked):
        global rtcm_checked
        if checked:
            rtcm_checked = True
            self.comboBox_baudrate_rtcm.setEnabled(True)
            self.comboBox_comport_rtcm.setEnabled(True)
            self.comboBox_baudrate_rtcm.setStyleSheet("""
                    QComboBox {
                        background-color: #2C3E50;
                        color: #FFFFFF;
                        border: 2px solid #1ABC9C;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QComboBox::drop-down {
                        width: 30px;  # Adjust the width of the drop-down arrow area
                        border-left: 2px solid #1ABC9C;
                        background-color: #2C3E50;
                    }
                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox::down-arrow:!editable {
                        color: #FFFFFF;  # Set the color of the "v"
                        text-align: center;
                        content: "v";  # Use "v" as the dropdown arrow
                    }
                    QComboBox::hover {
                        background-color: #3A7;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2E2E2E;  # Match dropdown background with main background
                        color: #FFFFFF;  # White text color
                        border: 2px solid #1ABC9C;
                        selection-background-color: #3A7;  # Color for selected item
                    }
                """)
            self.comboBox_comport_rtcm.setStyleSheet("""
                    QComboBox {
                        background-color: #2C3E50;
                        color: #FFFFFF;
                        border: 2px solid #1ABC9C;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QComboBox::drop-down {
                        width: 30px;  # Adjust the width of the drop-down arrow area
                        border-left: 2px solid #1ABC9C;
                        background-color: #2C3E50;
                    }
                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox::down-arrow:!editable {
                        color: #FFFFFF;  # Set the color of the "v"
                        text-align: center;
                        content: "v";  # Use "v" as the dropdown arrow
                    }
                    QComboBox::hover {
                        background-color: #3A7;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2E2E2E;  # Match dropdown background with main background
                        color: #FFFFFF;  # White text color
                        border: 2px solid #1ABC9C;
                        selection-background-color: #3A7;  # Color for selected item
                    }
                """)
            
            print("Radio button is selected")
        else:
            self.comboBox_comport_rtcm.setCurrentIndex(0)
            self.comboBox_baudrate_rtcm.setCurrentIndex(0)
            rtcm_checked = False
            self.comboBox_baudrate_rtcm.setEnabled(False)
            self.comboBox_comport_rtcm.setEnabled(False)
            self.lineEdit_replay_rtcm.clear()
            self.lineEdit_replay_rtcm.setPlaceholderText("Please select the file")
            self.comboBox_comport_rtcm.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
            self.comboBox_baudrate_rtcm.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)

    def handle_radio_button_ad9361(self, checked):
        global ad9361_checked
        if checked:
            ad9361_checked = True
            self.comboBox_comport.setEnabled(True)
            self.update_wifi_interface_state()
            self.comboBox_baudrate.setStyleSheet("""
                    QComboBox {
                        background-color: #2C3E50;
                        color: #FFFFFF;
                        border: 2px solid #1ABC9C;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QComboBox::drop-down {
                        width: 30px;  # Adjust the width of the drop-down arrow area
                        border-left: 2px solid #1ABC9C;
                        background-color: #2C3E50;
                    }
                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox::down-arrow:!editable {
                        color: #FFFFFF;  # Set the color of the "v"
                        text-align: center;
                        content: "v";  # Use "v" as the dropdown arrow
                    }
                    QComboBox::hover {
                        background-color: #3A7;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2E2E2E;  # Match dropdown background with main background
                        color: #FFFFFF;  # White text color
                        border: 2px solid #1ABC9C;
                        selection-background-color: #3A7;  # Color for selected item
                    }
                """)
            self.comboBox_comport.setStyleSheet("""
                    QComboBox {
                        background-color: #2C3E50;
                        color: #FFFFFF;
                        border: 2px solid #1ABC9C;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QComboBox::drop-down {
                        width: 30px;  # Adjust the width of the drop-down arrow area
                        border-left: 2px solid #1ABC9C;
                        background-color: #2C3E50;
                    }
                    QComboBox::down-arrow {
                        width: 12px;
                        height: 12px;
                    }
                    QComboBox::down-arrow:!editable {
                        color: #FFFFFF;  # Set the color of the "v"
                        text-align: center;
                        content: "v";  # Use "v" as the dropdown arrow
                    }
                    QComboBox::hover {
                        background-color: #3A7;
                    }
                    QComboBox QAbstractItemView {
                        background-color: #2E2E2E;  # Match dropdown background with main background
                        color: #FFFFFF;  # White text color
                        border: 2px solid #1ABC9C;
                        selection-background-color: #3A7;  # Color for selected item
                    }
                """)
            
            print("Radio button is selected")
        else:
            ad9361_checked = False
            self.comboBox_baudrate.setEnabled(False)
            self.comboBox_comport.setEnabled(False)
            self.comboBox_comport.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
            self.comboBox_baudrate.setStyleSheet("""
                QComboBox {
                    background-color: #4A6375;
                    color: #FFFFFF;
                    border: 2px solid #1ABC9C;
                    border-radius: 5px;
                    padding: 5px;
                }
                QComboBox::drop-down {
                    width: 30px;  # Adjust the width of the drop-down arrow area
                    border-left: 2px solid #1ABC9C;
                    background-color: #4A6375;
                }
                QComboBox::down-arrow {
                    width: 12px;
                    height: 12px;
                }
                QComboBox::down-arrow:!editable {
                    color: #FFFFFF;  # Set the color of the "v"
                    text-align: center;
                    content: "v";  # Use "v" as the dropdown arrow
                }
                QComboBox::hover {
                    background-color: #3A7;
                }
                QComboBox QAbstractItemView {
                    background-color: #2E2E2E;  # Match dropdown background with main background
                    color: #FFFFFF;  # White text color
                    border: 2px solid #1ABC9C;
                    selection-background-color: #3A7;  # Color for selected item
                }
            """)
    ######################################################################################################################
    def ensure_interface_disconnection(self):
        global ser, interface_in_use
        ensure_interface_disconnection_handle(ser, interface_in_use)

    def ensure_interface_connection(self, timeout_value=timeout_time, show_disconnection_dialog=False, destroy_root=False):
        global ser, root, ssh_url, ssh_password, interface_in_use
        if interface_in_use == 0:
            ser = connect_to_interface(ser, self.comport, self.baudrate, timeout_value)
            if ser is not None:
                return True
            if show_disconnection_dialog:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Warning")
                msg.setText("COM port got disconnected!")
                msg.exec()
                if destroy_root:
                    root.destroy()
                self.open_after_disconnection()
            else:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Error!")
                msg_box_2.setText("You cannot open this COM Port!")
                msg_box_2.exec()
            return False
        else:
            if self.comport == WIFI_INTERFACE_OPTION:
                print("Router WiFi")
                ssh_url = f"{ssh_username}@{self.lineEdit_hostname.text().strip()}.local"
            elif self.comport == WIFI_INTERFACE_OPTION_2:
                print("Board WiFi")
                ssh_url = ssh_fixed_url
            else:
                print("Unknown WiFi interface")
                return False

            ser, error_message = connect_to_wifi_interface(ser, ssh_url, ssh_password, timeout_value)
            if ser is not None:
                print("WiFi SSH connection established successfully.")
                return True

            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText(f"Unable to connect over WiFi SSH: {error_message}")
            msg_box_2.exec()
            return False

    def interface_check(self):
        global interface_in_use
        interface_in_use = interface_check_handle(self.comport, WIFI_INTERFACE_OPTION, WIFI_INTERFACE_OPTION_2)

    def open_usb_info(self):
        global flag_raised, ser, usb_button_flag, newoutput, interface_in_use
        self.comport = self.comboBox_comport.currentText()
        self.baudrate = self.comboBox_baudrate.currentText()
        print(self.comport)
        self.interface_check()
        if not self.ensure_interface_connection(timeout_time):
            return
        send_command(b'\x03')
        send_command(bytearray('clear\n', 'ascii'))
        with open(file_path, 'a') as file:
            file.write(f'\n{get_current_datetime()}   \x03\n')
            file.write(f'{get_current_datetime()}   clear\n')
        lines = self.read_Response_END() 
        print(lines)
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active: 
            
            send_command(bytearray(f'lsusb ; (echo END) > /dev/null\n', 'ascii'))
            if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   lsblk ; (echo END) > /dev/null\n')
            lines = self.read_Response_END()  # Call the function
            if lines is None:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                    msg_box_11.exec()
                    self.ensure_interface_disconnection()
                    return  # Stop execution
            print(lines)
            output = ''.join([line.decode('utf-8') for line in lines[1:-2]])
            
            def raise_flag():
                global flag_raised
                flag_raised = False
            newoutput = output.split("\n")

            if not gui_opened and not flag_raised:
                    flag_raised = True
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("USB Information")
                    msg_box_11.setText(f"{output}")
                    # Connect the finished signal to raise the flag
                    msg_box_11.finished.connect(raise_flag)
                    msg_box_11.exec()
        else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Comport got disconnected")
                    msg_box_11.exec()
                    #self.open_after_disconnection()
                    return 
        self.ensure_interface_disconnection()
        usb_button_flag = True

    def open_replay_window(self):
        if gui_opened:
            return
        global ser, config_button, fs_system, replay_tab, record_tab
        if not recording_started and not browse_folder and not browse_files and not config_browse_file and not delete_gui:
            
            if (self.baudrate != None and
                self.comport != None):
                if not submitted:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Submit!")
                    msg_box_11.setText("Please Submit the selected parameters")
                    msg_box_11.exec()
                    return
                #####################################################################
                if not self.ensure_interface_connection(timeout_time):
                    self.open_after_disconnection()
                    return
                #######################################################################
                fs_system_len = fs_system.split("/")
                if not fs_system == "/dev/" and len(fs_system_len)>=3:
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   *----Opened Replay window----*\n')
                    #############################################################################
                    """if ser.isOpen():
                        self.ensure_interface_disconnection()
                        #time.sleep(1)
                    # ####################################################
                    ser = serial.Serial(self.comport, self.baudrate, timeout=0.3)"""
                    #####################################################################################
                    if self.radioButton_double.isChecked():
                         self.label_Gain_Tx.setVisible(False)
                         self.label_Gain_Tx_2.setVisible(False)
                         self.label_Gain_Tx_2ch.setVisible(True)
                         self.label_Gain_Tx_2_2ch.setVisible(True)
                         self.lineEdit_Gain_Tx.setEnabled(True)
                         if self.radioButton_gpiomode.isChecked():
                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                         
                         self.lineEdit_Gain_Tx_2.setEnabled(True)
                         self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                    if self.radioButton_single.isChecked():
                         self.label_Gain_Tx.setVisible(True)
                         self.label_Gain_Tx_2.setVisible(True)
                         self.label_Gain_Tx.setEnabled(True)
                         self.label_Gain_Tx_2.setEnabled(True)
                         self.label_Gain_Tx_2ch.setVisible(False)
                         self.label_Gain_Tx_2_2ch.setVisible(False)
                         if self.label_Gain_Tx.isChecked():
                              self.lineEdit_Gain_Tx.setEnabled(True)
                              if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                              self.lineEdit_Gain_Tx_2.setEnabled(False)
                              self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                              self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         if self.label_Gain_Tx_2.isChecked():
                              self.lineEdit_Gain_Tx.setEnabled(False)
                              if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                              self.lineEdit_Gain_Tx_2.setEnabled(True)
                              self.lineEdit_Gain_Tx.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                              self.lineEdit_Gain_Tx_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                              

                    record_tab = False
                    replay_tab = True
                    config_button = False
                    self.comboBox_number_of_files.setVisible(False)
                    self.pushButton_refresh_config_maxduration.setVisible(False)
                    self.label_MHz_BW.setVisible(False)
                    self.label_MHz_LO.setVisible(False)
                    self.label_MHz_SF.setVisible(False)
                    self.label_files_select.setVisible(False)
                    self.label_current_file.setVisible(False)
                    self.label_SSD_capacity.setVisible(False)
                    self.label_available_Duration.setVisible(False)
                    self.button_reboot.setVisible(False)
                    self.button_shutdown.setVisible(False)
                    if show_path_btn_active_replay:
                        self.show_path_btn_replay.setVisible(True)
                    if hide_path_btn_active_replay:
                        self.hide_path_btn_replay.setVisible(True)
                    if show_path_btn_active_replay_rtcm:
                        self.show_path_btn_replay_rtcm.setVisible(True)
                    if hide_path_btn_active_replay_rtcm:
                        self.hide_path_btn_replay_rtcm.setVisible(True)
                    self.show_path_btn.setVisible(False)
                    self.hide_path_btn.setVisible(False)
                    self.show_path_btn_rtcm.setVisible(False)
                    self.hide_path_btn_rtcm.setVisible(False)
                    self.table_widget.setVisible(False)
                    self.label_fs_system.setVisible(False)
                    self.label_fs_system_display.setVisible(False)
                    self.lineEdit_fs_system.setVisible(False)
                    self.line_fs_system.setVisible(False)
                    self.fs_system_edit_btn.setVisible(False)
                    self.fs_system_submit_btn.setVisible(False)
                    #self.pushButton_select_file.setVisible(False)
                    self.label_config.setVisible(False)
                    self.pushButton_browse_config.setVisible(False)
                    self.pushButton_refresh_config.setVisible(False)
                    self.label_sampling.setVisible(False)
                    #self.green_satellite.setVisible(False)
                    self.label_samplingfreq.setVisible(False)
                    self.lineEdit_samplingfreq.setVisible(False)
                    self.lineEdit_samplingfreq_2.setVisible(False)
                    self.red_light_record.setVisible(False)
                    self.green_light_record.setVisible(False)
                    self.line_record.setVisible(False)
                    self.line_vertical.setVisible(False)
                    self.line_vertical_2.setVisible(False)
                    self.label_browse_record.setVisible(False)
                    self.label_browse_record_rtcm.setVisible(False)
                    self.radioButton_GPIO_Record.setVisible(False)
                    self.lineEdit_browse_record.setVisible(False)
                    self.lineEdit_browse_record_rtcm.setVisible(False)
                    self.pushButton_browse_record.setVisible(False)
                    self.pushButton_browse_record_rtcm.setVisible(False)
                    self.red_light.setVisible(True)
                    self.radioButton_double.setVisible(False)
                    self.radioButton_single.setVisible(False)
                    self.label_radio.setVisible(False)
                    self.lineEdit_hostname.setVisible(False)
                    self.label_ssid.setVisible(False)
                    self.lineEdit_password.setVisible(False)
                    self.label_hostname.setVisible(False)
                    self.label_gpiomode.setVisible(False)
                    self.radioButton_gpiomode.setVisible(False)
                    self.radioButton_rfmdmode.setVisible(False)
                    self.label_connectivity.setVisible(False)
                    self.current_window = "replay"
                    self.pushButton_login.setEnabled(True)
                    self.pushButton.setVisible(False)
                    self.pushButton_2.setVisible(True)
                    self.pushButton_3.setVisible(False)
                    self.pushButton_4.setVisible(True)
                    self.pushButton_5.setVisible(True)
                    self.lineEdit.setVisible(False)
                    self.lineEdit_2.setVisible(False)
                    self.lineEdit_3.setVisible(False)
                    self.lineEdit_4.setVisible(False)
                    self.lineEdit_6.setVisible(False)
                    self.label.setVisible(False)
                    self.label_10.setVisible(False)
                    self.label_2.setVisible(False)
                    self.label_3.setVisible(False)
                    self.label_4.setVisible(False)
                    self.label_5.setVisible(False)
                    self.label_8.setVisible(False)
                    self.label_9.setVisible(False)
                    self.comboBox.setVisible(False)
                    self.comboBox_2.setVisible(False)
                    self.pushButton_6.setVisible(True)
                    self.pushButton_7.setVisible(True)
                    self.lineEdit_7.setVisible(True)
                    self.lineEdit_8.setVisible(True)
                    self.label_11.setVisible(True)
                    self.label_12.setVisible(True)
                    self.radioButton_GPIO_Replay.setVisible(True)
                    if self.radioButton_rfmdmode.isChecked():
                        self.radioButton_GPIO_Record.setDisabled(True)
                        self.radioButton_GPIO_Record.setChecked(False)
                        self.radioButton_GPIO_Replay.setDisabled(True)
                        self.radioButton_GPIO_Replay.setChecked(False)
                    else:
                        self.radioButton_GPIO_Record.setDisabled(False)
                        self.radioButton_GPIO_Replay.setDisabled(False)
                    self.pushButton_8.setVisible(True)
                    self.lineEdit9.setVisible(True)
                    self.lineEdit_replay_rtcm.setVisible(True)
                    self.pushButton_browse_replay_rtcm.setVisible(True)
                    self.label_files_rtcm.setVisible(True)
                    self.lineEdit9.setReadOnly(True)
                    self.label_13.setVisible(True)
                    self.label_about_2.setVisible(False)
                    self.label_about_3.setVisible(False)
                    self.label_bandwidth.setVisible(False)
                    self.label_gain.setVisible(False)
                    self.lineEdit_bandwidth.setVisible(False)
                    self.radioButton_autoplay.setVisible(True)
                    #self.label_Gain_Tx.setVisible(True)
                    self.lineEdit_Gain_Tx.setVisible(True)
                    self.lineEdit_rate.setVisible(True)
                    #self.label_Gain_Tx_2.setVisible(True)
                    self.lineEdit_Gain_Tx_2.setVisible(True)
                    self.label_Gain_Tx_3ch.setVisible(True)
                    self.line_vertical_Replay.setVisible(True)
                    self.label_rate.setVisible(True)
                    self.lineEdit_gain_1.setVisible(False)
                    self.lineEdit_gain_2.setVisible(False)
                    
                    self.lineEdit_bandwidth_2.setVisible(False)
                    self.label_SD_image_system_download_2.setVisible(False)
                    self.label_SD_image_system_download.setVisible(False)
                    self.pushButton_submit.setVisible(False)
                    self.comboBox_baudrate.setVisible(False)
                    self.comboBox_comport.setVisible(False)
                    self.label_ref_freq.setVisible(False)
                    self.comboBox_ref_freq.setVisible(False)
                    self.label_connected.setVisible(False)
                    self.label_connected_rtcm.setVisible(False)
                    self.button_reconnect.setVisible(False)
                    self.comboBox_baudrate_rtcm.setVisible(False)
                    self.radioButton_ad9361.setVisible(False)
                    self.radioButton_rtcm.setVisible(False)
                    self.lineEdit_deviceid.setVisible(False)
                    self.label_deviceid.setVisible(False)
                    self.lineEdit_busno.setVisible(False)
                    self.label_busno.setVisible(False)
                    self.pushButton_usb_info.setVisible(False)
                    self.comboBox_comport_rtcm.setVisible(False)
                    self.line_2.setVisible(False)
                    self.lineEdit_replay.setVisible(True)
                    self.label_replay.setVisible(True)
                    self.radioButton_Rx_1.setVisible(False)
                    self.radioButton_Rx_2.setVisible(False)
                    self.pushButton_4.setStyleSheet("QPushButton{"
                                            "background-color: #1ABC9C;"
                                            "color: white;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_5.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_2.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_login.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_select_file.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"
                                              "}")  # Change color when pressed if desired
                    if only_ad9361:
                         self.lineEdit_replay_rtcm.setEnabled(False)
                         self.pushButton_browse_replay_rtcm.setEnabled(True)
                         self.show_path_btn_replay_rtcm.setEnabled(True)
                         self.hide_path_btn_replay_rtcm.setEnabled(True)
                         self.lineEdit9.setEnabled(True)
                         self.pushButton_8.setEnabled(True)
                         self.show_path_btn.setEnabled(True)
                         self.hide_path_btn.setEnabled(True)
                         self.lineEdit_rate.setEnabled(False)
                         self.lineEdit_rate.setStyleSheet("""
                                                QLineEdit {
                                                    background-color:  #4A6375;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                         self.lineEdit_replay_rtcm.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         self.lineEdit9.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                    elif only_rtcm:
                         self.lineEdit_replay_rtcm.setEnabled(True)
                         self.pushButton_browse_replay_rtcm.setEnabled(True)
                         self.show_path_btn_replay_rtcm.setEnabled(True)
                         self.hide_path_btn_replay_rtcm.setEnabled(True)
                         self.lineEdit9.setEnabled(False)
                         self.pushButton_8.setEnabled(False)
                         self.show_path_btn.setEnabled(False)
                         self.hide_path_btn.setEnabled(False)
                         self.lineEdit_rate.setEnabled(True)
                         self.lineEdit_rate.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                         self.lineEdit9.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         self.lineEdit_replay_rtcm.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                    if checked_both_without_HWUSB or HW_USB_in_use:
                        self.lineEdit_replay_rtcm.setEnabled(True)
                        self.pushButton_browse_replay_rtcm.setEnabled(True)
                        self.show_path_btn_replay_rtcm.setEnabled(True)
                        self.hide_path_btn_replay_rtcm.setEnabled(True)
                        self.lineEdit9.setEnabled(True)
                        self.pushButton_8.setEnabled(True)
                        self.lineEdit_rate.setEnabled(True)
                        self.lineEdit_rate.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                        self.show_path_btn.setEnabled(True)
                        self.hide_path_btn.setEnabled(True)
                        self.lineEdit_replay_rtcm.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                        self.lineEdit9.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                    self.pushButton_invisible.setVisible(False)
                    self.pushButton_pdf.setVisible(False)
                    self.vericalline_fs_system.setVisible(False)
                    self.label_SD_image_system.setVisible(False)
                    self.label_SD_image_display.setVisible(False)
                else:
                    msg_box_9 = QMessageBox()
                    msg_box_9.setWindowTitle("Error!")
                    msg_box_9.setText("Please Submit a valid label for nvme SSD")
                    msg_box_9.exec()                             
            else:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Missing Data")
                msg_box_2.setText("Please select the Com port")
                msg_box_2.exec()
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Recording is ON!")
            msg_box_2.setText("You cannot switch to Replay while Recording is ON!")
            msg_box_2.exec()

    def main_function(self):
        global main_func_called
        main_func_called = True
             
        if gui_opened:
            return
        if not replay_started and not browse_files and not browse_folder and not config_browse_file and not delete_gui:
            global ser, config_button, record_tab, replay_tab, boot
            if ((self.baudrate != None) and
                (self.comport != None)):
                if not submitted:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Submit!")
                    msg_box_11.setText("Please Submit the selected parameters")
                    msg_box_11.exec()
                    return
                fs_system_len = fs_system.split("/")
                if not fs_system == "/dev/" and len(fs_system_len)>=3:
                    thread_1 = threading.Thread(target=self.open_record_window)
                    thread_2 = threading.Thread(target=self.get_max_duration_theorotical)
                    # Start threads
                    thread_1.start()
                    thread_2.start()

                    """size_in_bytes_1 = convert_size(SSD_free_space) 
                    self.label_SSD_capacity.setText(f"Free SSD: {SSD_free_space}")
                    self.open_record_window()"""
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText("Please Enter a valid label for nvme SSD in files tab")
                    msg_box_11.exec()
                    return
            else:
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Missing Data")
                msg_box_9.setText("Please select the Com port")
                msg_box_9.exec()
        else:
            if replay_started:
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Replay is ON!")
                msg_box_9.setText("You cannot switch to Recording while Replay is ON!")
                msg_box_9.exec()
    #################################################################################################################
    def check_selected_files_availability(self):
                print("hi")
                """svg_renderer = QSvgRenderer("Refreshing_on_progress.svg")  # Replace with your SVG image path
                # Create a QPixmap and render the SVG onto it
                pixmap = QPixmap(45, 45)  # Set the size of the icon
                pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                # Use QPainter to render the SVG on the QPixmap
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
                # Set the rendered SVG as the icon for the QPushButton
                icon = QIcon(pixmap)
                self.pushButton_refresh_config.setIcon(icon)
                self.pushButton_refresh_config.setIconSize(QSize(30, 30))  # Set icon size"""

                lines = read_lines()
                comport_is_active = interface_is_online(self.comport)
         
                if comport_is_active:   
                    send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                    lines = read_lines()
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return
                comport_is_active = interface_is_online(self.comport)
          
                if comport_is_active:               
                    send_command(bytearray(f'cat "{filename_txt}" ; (echo END) > /dev/null\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cat "{filename_txt}" ; (echo END) > /dev/null\n')
                    lines = self.read_Response_END()  # Call the function
                    if lines is None:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        msg_box_11.exec()
                        return  # Stop execution
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return
                if len(lines) >= 3:
                    if not filename_txt in str(lines[0]):
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! 'HW_files' folder is not found\nIn the directory {read_selected_file_path}")
                        msg_box_11.exec() 
                        return
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops!, Please check the connections\nIs the AD9361 Hardware connected?")
                    msg_box_11.exec() 
                    return
                ######################################################################################
                lines = lines[1:-2]
                print(lines)
                try:
                    decoded_lines = [line.decode() for line in lines]
                except UnicodeDecodeError as e:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Recevied messages are not decoded")
                        msg_box_11.exec() 
                        return
                    
                print(decoded_lines)
                file_names = decoded_lines
                count = 0
                directories_files = {}
                self.variable_names = []
                if decoded_lines == []:
                    self.variable_names = []
                
                elif not "No such file or directory" in (decoded_lines[-1]):
                    if comport_is_active:
                                send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                    else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return

                    for line in decoded_lines:
                        if "selected_files:" in line:
                            print(line)
                            extracted_line = "/"+"/".join(line.split("/")[1:-1]).split("\\")[0].strip()
                            print(extracted_line)
                            extracted_file_name = line.split("/")[-1].split("\\")[0].strip()+".bin"
                            print(extracted_file_name)
                            count += 1
                            directories_files[count] = extracted_line, extracted_file_name

                    # Build the command dynamically
                    command_parts = []
                    print(directories_files)
                    for _, (directory, filename) in directories_files.items():
                        command_parts.append(
                            f'cd "{directory}" && [ -f "{filename}" ] && echo "{directory}/{filename}:- Found" || echo "{directory}/{filename}:- Not Found"'
                        )

                    ################################################################################################
                    # Join all commands with a semicolon
                    command_file_read = "; ".join(command_parts) + " ; (echo END) > /dev/null\n"
                    #print(command_file_read)
                    send_command(bytearray(command_file_read, 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}  {command_file_read}')
                    lines = self.read_Response_END()  # Call the function
                    print(lines)
                    if lines is None:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        msg_box_11.exec()
                        return  # Stop execution
                    decoded_lines = [line.decode() for line in lines]
                    for line in decoded_lines:
                        print(line)
                        message = str(line.split(":-")[-1]).strip()
                        print(message)
                        if message == "Not Found":
                            line_to_edit = line.split(":-")[0].split(".bin")[0].strip()
                           
                            line_to_edit = filename_txt_string_editor(line_to_edit)
                           
                            comport_is_active = interface_is_online(self.comport)

                            if comport_is_active:
                                send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                                        
                            if comport_is_active:
                                send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt}\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt}\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                                        
                        if message == "Found":
                            print(line)
                            self.variable_names.append(line.split(":-")[0].split("/")[-1].strip().split(".bin")[0].strip())
                    ################################################################################################
                elif "No such file or directory" in (decoded_lines[-1]):
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Info")
                    msg_box_11.setText(f"The file {filename_txt} not found\n\nA new {filename_txt} file is created\n\nDirectory:{directory}")
                    msg_box_11.exec()
                    comport_is_active = interface_is_online(self.comport)
                 
                    if comport_is_active: 
                        send_command(bytearray(f'cd "{directory}"\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   cd "{directory}"\n')
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"COM port got disconnected!")
                        msg_box_11.exec()
                        self.open_after_disconnection()
                        return
                    comport_is_active = interface_is_online(self.comport)
                
                    if comport_is_active: 
                        send_command(bytearray(f'touch "{filename_txt}"\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   touch "{filename_txt}"\n')
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"COM port got disconnected!")
                        msg_box_11.exec()
                        self.open_after_disconnection()
                        return
                    read_lines()
                    self.variable_names = []
        
                self.populate_table()
                svg_renderer = QSvgRenderer("Refresh.svg")  # Replace with your SVG image path
                # Create a QPixmap and render the SVG onto it
                pixmap = QPixmap(45, 45)  # Set the size of the icon
                pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                # Use QPainter to render the SVG on the QPixmap
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
                # Set the rendered SVG as the icon for the QPushButton
                icon = QIcon(pixmap)
                self.pushButton_refresh_config.setIcon(icon)
                self.pushButton_refresh_config.setIconSize(QSize(30, 30))  # Set icon size
    #################################################################################################################
    def open_after_disconnection(self):
            global comport_connected, submitted, config_button, ser_rtcm, check_comport, ser
            comport_connected = False
            if ser.isOpen():
                self.ensure_interface_disconnection()
            if checked_both_without_HWUSB:
                if ser_rtcm.isOpen():
                    ser_rtcm.close()
            submitted = False
            if self.worker.running:
                self.worker.stop()  # Tell the thread to stop
                self.worker.wait()
                self.worker.running = False
            config_button = False
            if Commands_file_user:
                with open(file_path, 'a') as file:
                    file.write(f'\n{get_current_datetime()}   *----Opened Home tab after disconnection----*\n')
            self.show_path_btn_replay.setVisible(False)
            self.update_com_ports_rtcm()
            self.update_com_ports()
            check_comport = True
            self.show_path_btn_replay_rtcm.setVisible(False)
            self.hide_path_btn_replay_rtcm.setVisible(False)
            self.comboBox_number_of_files.setVisible(False)
            self.pushButton_invisible.setVisible(False)
            self.pushButton_pdf.setVisible(False)
            self.vericalline_fs_system.setVisible(False)
            self.label_SD_image_system.setVisible(False)
            self.label_SD_image_display.setVisible(False)
            self.label_MHz_BW.setVisible(False)
            self.label_MHz_LO.setVisible(False)
            self.vericalline_fs_system.setVisible(False)
            self.label_SD_image_system.setVisible(False)
            self.label_SD_image_display.setVisible(False)
            self.label_MHz_SF.setVisible(False)
            self.label_files_select.setVisible(False)
            self.label_current_file.setVisible(False)
            self.label_SSD_capacity.setVisible(False)
            self.label_available_Duration.setVisible(False)
            self.hide_path_btn_replay.setVisible(False)
            self.table_widget.setVisible(False)
            self.show_path_btn.setVisible(False)
            self.hide_path_btn.setVisible(False)
            self.show_path_btn_rtcm.setVisible(False)
            self.hide_path_btn_rtcm.setVisible(False)
            self.label_fs_system.setVisible(False)
            self.label_fs_system_display.setVisible(False)
            self.lineEdit_fs_system.setVisible(False)
            self.line_fs_system.setVisible(False)
            self.fs_system_edit_btn.setVisible(False)
            self.fs_system_submit_btn.setVisible(False)
            #self.pushButton_select_file.setVisible(False)
            self.label_config.setVisible(False)
            self.pushButton_browse_config.setVisible(False)
            self.pushButton_refresh_config.setVisible(False)
            #self.green_satellite.setVisible(False) 
            self.radioButton_Rx_1.setVisible(False)
            self.radioButton_Rx_2.setVisible(False)  
            self.label_sampling.setVisible(False)
            self.radioButton_autoplay.setVisible(False)
            self.label_Gain_Tx.setVisible(False)
            self.label_Gain_Tx_2ch.setVisible(False)
            self.label_Gain_Tx_2_2ch.setVisible(False) 
            self.label_Gain_Tx_2.setVisible(False)
            self.lineEdit_Gain_Tx_2.setVisible(False)
            self.label_Gain_Tx_3ch.setVisible(False)
            self.line_vertical_Replay.setVisible(False)
            self.lineEdit_Gain_Tx.setVisible(False)
            self.lineEdit_rate.setVisible(False)
            self.label_rate.setVisible(False)
            self.label_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq_2.setVisible(False)
            self.red_light_record.setVisible(False)
            self.green_light_record.setVisible(False)
            self.green_light.setVisible(False)
            self.red_light.setVisible(False)
            self.line_record.setVisible(False)
            self.line_vertical.setVisible(False)
            self.line_vertical_2.setVisible(False)
            self.label_browse_record.setVisible(False)
            self.label_browse_record_rtcm.setVisible(False)
            self.radioButton_GPIO_Record.setVisible(False)
            self.lineEdit_browse_record.setVisible(False)
            self.lineEdit_browse_record_rtcm.setVisible(False)
            self.pushButton_browse_record.setVisible(False)
            self.pushButton_browse_record_rtcm.setVisible(False)
            self.pushButton_login.setEnabled(False)
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(True)
            self.pushButton_3.setVisible(False)
            self.pushButton_4.setVisible(True)
            self.pushButton_5.setVisible(True)
            self.lineEdit.setVisible(False)
            self.comboBox_comport.setVisible(True)
            self.label_ref_freq.setVisible(False)
            self.comboBox_ref_freq.setVisible(False)
            self.comboBox_baudrate.setVisible(True)
            self.pushButton_submit.setVisible(True)
            self.label_connectivity.setVisible(True)
            self.radioButton_double.setVisible(True)
            self.radioButton_single.setVisible(True)
            self.label_radio.setVisible(True)
            item = self.comboBox_comport.currentText()
            if item == WIFI_INTERFACE_OPTION:
                self.lineEdit_hostname.setVisible(True)
                self.label_ssid.setVisible(True)
                self.lineEdit_password.setVisible(False)
                self.label_hostname.setVisible(True)
            else:
                self.lineEdit_hostname.setVisible(False)
                self.label_ssid.setVisible(False)
                self.lineEdit_password.setVisible(False)
                self.label_hostname.setVisible(False)
            self.label_gpiomode.setVisible(False)
            self.radioButton_gpiomode.setVisible(False)
            self.radioButton_rfmdmode.setVisible(False)
            self.comboBox_baudrate_rtcm.setVisible(True)
            self.radioButton_ad9361.setVisible(True)
            self.radioButton_rtcm.setVisible(True)
            if self.comboBox_comport_rtcm.currentText() == "HW USB":
                self.lineEdit_deviceid.setVisible(True)
                self.label_deviceid.setVisible(True)
                self.lineEdit_busno.setVisible(True)
                self.label_busno.setVisible(True)
                self.pushButton_usb_info.setVisible(True)
            else:
                self.lineEdit_deviceid.setVisible(False)
                self.label_deviceid.setVisible(False)
                self.lineEdit_busno.setVisible(False)
                self.label_busno.setVisible(False)
                self.pushButton_usb_info.setVisible(False)
            self.comboBox_comport_rtcm.setVisible(True)
            self.label_connected.setVisible(False)
            self.label_connected_rtcm.setVisible(False)
            self.button_reconnect.setVisible(False)
            self.button_reboot.setVisible(False)
            self.button_shutdown.setVisible(False)
            self.lineEdit_2.setVisible(False)
            self.lineEdit_3.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_6.setVisible(False)
            self.label.setVisible(False)
            self.label_10.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.label_8.setVisible(False)
            self.label_9.setVisible(False)
            self.comboBox.setVisible(False)
            self.comboBox_2.setVisible(False)
            self.label_bandwidth.setVisible(False)
            self.label_gain.setVisible(False)
            self.lineEdit_bandwidth.setVisible(False)
            self.lineEdit_gain_1.setVisible(False)
            self.lineEdit_gain_2.setVisible(False)
            self.lineEdit_bandwidth_2.setVisible(False)
            self.lineEdit_replay.setVisible(False)
            self.label_replay.setVisible(False)
            self.pushButton_refresh_config_maxduration.setVisible(False)
            self.pushButton_refresh_config.setVisible(False)   

            self.pushButton_6.setVisible(False)
            self.pushButton_7.setVisible(False)
            self.lineEdit_7.setVisible(False)
            self.lineEdit_8.setVisible(False)
            self.label_11.setVisible(False)
            self.label_12.setVisible(False)
            self.radioButton_GPIO_Replay.setVisible(False)
            self.pushButton_8.setVisible(False)
            self.lineEdit9.setVisible(False)
            self.lineEdit_replay_rtcm.setVisible(False)
            self.pushButton_browse_replay_rtcm.setVisible(False)
            self.label_files_rtcm.setVisible(False)
            self.label_13.setVisible(False)
            self.label_about_2.setVisible(False)
            self.label_about_3.setVisible(False)
            self.line_2.setVisible(False)
            self.pushButton_4.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_2.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_login.setStyleSheet("QPushButton{"
                                         "background-color: #1ABC9C;"
                                         "color: white;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_5.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_select_file.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_4.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_refresh_config_maxduration.setVisible(False)
            self.pushButton_refresh_config.setVisible(False)            
            """comport_thread = threading.Thread(target=self.check_comport_Regularly)
            comport_thread.start()"""
            """self.get_comport()
            self.get_comport_rtcm()
            if self.comport_rtcm == "":
                self.comboBox_comport_rtcm.addItem("Select Port") 
            if self.comport == "":
                self.comboBox_comport.addItem("Select Port")"""
            

    #################################################################################################################
    def open_record_window(self):
        print(self.reference_frequency)
        if gui_opened:
            return
        fs_system_len = fs_system.split("/")
        if not replay_started and not browse_files and not browse_folder and not config_browse_file and not delete_gui:
            global ser, config_button, record_tab, replay_tab, boot
            if ((self.baudrate != None) and
                (self.comport != None)):
                if not submitted:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Submit!")
                    msg_box_11.setText("Please Submit the selected parameters")
                    msg_box_11.exec()
                    return
                #####################################################################
                if not self.ensure_interface_connection(timeout_time):
                    self.open_after_disconnection()
                    return
                #######################################################################
                if not fs_system == "/dev/" and len(fs_system_len)>=3:
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   *----Opened Record window----*\n')
                    ###########################################################################
                    #####################################################################################
                    
                    if boot:
                        boot = False
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active:
                            send_command(b'\x03')
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   \x03')
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active:
                            send_command(bytearray('clear\n', 'ascii'))
                            if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   clear\n')
                            bs = read_lines()
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    ####################################################################################
                    """if ser.isOpen:
                        self.ensure_interface_disconnection()
                    ser = serial.Serial(self.comport, self.baudrate, timeout=timeout_time)"""
                    ####################################################################################
                    record_tab = True
                    replay_tab = False
                    config_button = False
                    self.comboBox_number_of_files.setVisible(True)
                    self.pushButton_refresh_config_maxduration.setVisible(True)
                    self.label_MHz_BW.setVisible(True)
                    self.label_MHz_LO.setVisible(True)
                    self.label_MHz_SF.setVisible(True)
                    self.label_files_select.setVisible(True)
                    self.label_current_file.setVisible(True)
                    self.show_path_btn_replay.setVisible(False)
                    self.hide_path_btn_replay.setVisible(False)
                    self.show_path_btn_replay_rtcm.setVisible(False)
                    self.hide_path_btn_replay_rtcm.setVisible(False)
                    if show_path_btn_active:
                        self.show_path_btn.setVisible(True)
                    if hide_path_btn_active:
                        self.hide_path_btn.setVisible(True)
                    if show_path_btn_active_rtcm:
                         self.show_path_btn_rtcm.setVisible(True)
                    if hide_path_btn_active_rtcm:
                         self.hide_path_btn_rtcm.setVisible(True)
                    #self.pushButton_select_file.setVisible(False)
                    
                    self.label_fs_system.setVisible(False)
                    self.label_SD_image_system_download_2.setVisible(False)
                    self.label_SD_image_system_download.setVisible(False)
                    self.label_fs_system_display.setVisible(False)
                    self.lineEdit_fs_system.setVisible(False)
                    self.line_fs_system.setVisible(False)
                    self.fs_system_edit_btn.setVisible(False)
                    self.fs_system_submit_btn.setVisible(False)
                    self.table_widget.setVisible(False)
                    self.label_config.setVisible(False)
                    self.pushButton_browse_config.setVisible(False)
                    self.pushButton_refresh_config.setVisible(False)
                    self.label_sampling.setVisible(False)
                    #self.green_satellite.setVisible(False)
                    self.label_samplingfreq.setVisible(True)
                    self.lineEdit_samplingfreq.setVisible(True)
                    self.lineEdit_samplingfreq_2.setVisible(True)
                    self.line_record.setVisible(True)
                    self.line_vertical.setVisible(True)
                    self.line_vertical_2.setVisible(True)
                    self.red_light_record.setVisible(True)
                    self.green_light_record.setVisible(False)
                    self.label_browse_record.setVisible(True)
                    self.label_browse_record_rtcm.setVisible(True)
                    self.radioButton_GPIO_Record.setVisible(True)
                    if self.radioButton_rfmdmode.isChecked():
                        self.radioButton_GPIO_Record.setDisabled(True)
                        self.radioButton_GPIO_Record.setChecked(False)
                        self.radioButton_GPIO_Replay.setDisabled(True)
                        self.radioButton_GPIO_Replay.setChecked(False)
                    else:
                        self.radioButton_GPIO_Record.setDisabled(False)
                        self.radioButton_GPIO_Replay.setDisabled(False)
                    self.lineEdit_browse_record.setVisible(True)
                    self.lineEdit_browse_record_rtcm.setVisible(True)
                    self.pushButton_browse_record.setVisible(True)
                    self.pushButton_browse_record_rtcm.setVisible(True)
                    self.green_light.setVisible(False)
                    self.pushButton_invisible.setVisible(False)
                    self.pushButton_pdf.setVisible(False)
                    self.vericalline_fs_system.setVisible(False)
                    self.label_SD_image_system.setVisible(False)
                    self.label_SD_image_display.setVisible(False)
                    self.red_light.setVisible(False)
                    self.radioButton_Rx_1.setVisible(True)
                    self.radioButton_Rx_2.setVisible(True)
                    self.lineEdit_4.setVisible(True)
                    self.lineEdit_bandwidth_2.setVisible(True)
                    self.comboBox_2.setVisible(True)
                    self.lineEdit_samplingfreq_2.setVisible(True)
                    if self.radioButton_single.isChecked():
                        if self.radioButton_Rx_1.isChecked(): 
                            self.lineEdit_4.setEnabled(False)
                            self.lineEdit_bandwidth_2.setEnabled(False)
                            self.comboBox_2.setEnabled(False)
                           
                            self.lineEdit_gain_2.setEnabled(False)
                            #self.lineEdit_gain_2.setText("")
                            self.lineEdit_samplingfreq_2.setEnabled(False)
                            self.lineEdit_3.setEnabled(True)
                            self.lineEdit_bandwidth.setEnabled(True)
                            self.comboBox.setEnabled(True)
                            self.lineEdit_gain_1.setEnabled(True)
                            #self.lineEdit_gain_2.setText("")
                            self.lineEdit_samplingfreq.setEnabled(True)
                            self.lineEdit_4.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #4A6375;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                            self.lineEdit_bandwidth_2.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.lineEdit_samplingfreq_2.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.lineEdit_gain_2.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.comboBox_2.setStyleSheet("""
                                QComboBox {
                                    background-color: #4A6375;
                                    color: #FFFFFF;
                                    border: 2px solid #1ABC9C;
                                    border-radius: 5px;
                                    padding: 5px;
                                }
                                QComboBox::drop-down {
                                    width: 30px;  # Adjust the width of the drop-down arrow area
                                    border-left: 2px solid #1ABC9C;
                                    background-color: #4A6375;
                                }
                                QComboBox::down-arrow {
                                    width: 12px;
                                    height: 12px;
                                }
                                QComboBox::down-arrow:!editable {
                                    color: #FFFFFF;  # Set the color of the "v"
                                    text-align: center;
                                    content: "v";  # Use "v" as the dropdown arrow
                                }
                                QComboBox::hover {
                                    background-color: #3A7;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: #2E2E2E;  # Match dropdown background with main background
                                    color: #FFFFFF;  # White text color
                                    border: 2px solid #1ABC9C;
                                    selection-background-color: #3A7;  # Color for selected item
                                }
                            """)
                            self.lineEdit_3.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                            self.lineEdit_bandwidth.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.lineEdit_samplingfreq.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.lineEdit_gain_1.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.comboBox.setStyleSheet("""
                                    QComboBox {
                                        background-color: #2C3E50;
                                        color: #FFFFFF;
                                        border: 2px solid #1ABC9C;
                                        border-radius: 5px;
                                        padding: 5px;
                                    }
                                    QComboBox::drop-down {
                                        width: 30px;  # Adjust the width of the drop-down arrow area
                                        border-left: 2px solid #1ABC9C;
                                        background-color: #2C3E50;
                                    }
                                    QComboBox::down-arrow {
                                        width: 12px;
                                        height: 12px;
                                    }
                                    QComboBox::down-arrow:!editable {
                                        color: #FFFFFF;  # Set the color of the "v"
                                        text-align: center;
                                        content: "v";  # Use "v" as the dropdown arrow
                                    }
                                    QComboBox::hover {
                                        background-color: #3A7;
                                    }
                                    QComboBox QAbstractItemView {
                                        background-color: #2E2E2E;  # Match dropdown background with main background
                                        color: #FFFFFF;  # White text color
                                        border: 2px solid #1ABC9C;
                                        selection-background-color: #3A7;  # Color for selected item
                                    }
                                """)
                        if self.radioButton_Rx_2.isChecked():
                            #self.lineEdit_gain_1.setText("")
                            self.lineEdit_4.setEnabled(True)
                            self.lineEdit_bandwidth_2.setEnabled(True)
                            self.comboBox_2.setEnabled(True)
                            self.lineEdit_gain_1.setEnabled(False)
                            self.lineEdit_gain_2.setEnabled(True)
                            self.lineEdit_samplingfreq_2.setEnabled(True)
                            self.lineEdit_3.setEnabled(False)
                            self.lineEdit_bandwidth.setEnabled(False)
                            self.comboBox.setEnabled(False)
                            self.lineEdit_gain_1.setEnabled(False)
                            #self.lineEdit_gain_2.setText("")
                            self.lineEdit_samplingfreq.setEnabled(False)
                            self.lineEdit_3.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #4A6375;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                            self.lineEdit_bandwidth.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.lineEdit_samplingfreq.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.lineEdit_gain_1.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #4A6375;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                            self.comboBox.setStyleSheet("""
                                QComboBox {
                                    background-color: #4A6375;
                                    color: #FFFFFF;
                                    border: 2px solid #1ABC9C;
                                    border-radius: 5px;
                                    padding: 5px;
                                }
                                QComboBox::drop-down {
                                    width: 30px;  # Adjust the width of the drop-down arrow area
                                    border-left: 2px solid #1ABC9C;
                                    background-color: #4A6375;
                                }
                                QComboBox::down-arrow {
                                    width: 12px;
                                    height: 12px;
                                }
                                QComboBox::down-arrow:!editable {
                                    color: #FFFFFF;  # Set the color of the "v"
                                    text-align: center;
                                    content: "v";  # Use "v" as the dropdown arrow
                                }
                                QComboBox::hover {
                                    background-color: #3A7;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: #2E2E2E;  # Match dropdown background with main background
                                    color: #FFFFFF;  # White text color
                                    border: 2px solid #1ABC9C;
                                    selection-background-color: #3A7;  # Color for selected item
                                }
                            """)
                            self.lineEdit_4.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                            self.lineEdit_bandwidth_2.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.lineEdit_gain_2.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.lineEdit_samplingfreq_2.setStyleSheet("""
                                                            QLineEdit {
                                                                background-color: #2C3E50;
                                                                color: #FFFFFF;
                                                                border: 2px solid #1ABC9C;
                                                                border-radius: 5px;
                                                                padding: 5px;
                                                            }
                                                            QLineEdit:focus {
                                                                border: 2px solid #2E5;
                                                            }
                                                        """)
                            self.comboBox_2.setStyleSheet("""
                                    QComboBox {
                                        background-color: #2C3E50;
                                        color: #FFFFFF;
                                        border: 2px solid #1ABC9C;
                                        border-radius: 5px;
                                        padding: 5px;
                                    }
                                    QComboBox::drop-down {
                                        width: 30px;  # Adjust the width of the drop-down arrow area
                                        border-left: 2px solid #1ABC9C;
                                        background-color: #2C3E50;
                                    }
                                    QComboBox::down-arrow {
                                        width: 12px;
                                        height: 12px;
                                    }
                                    QComboBox::down-arrow:!editable {
                                        color: #FFFFFF;  # Set the color of the "v"
                                        text-align: center;
                                        content: "v";  # Use "v" as the dropdown arrow
                                    }
                                    QComboBox::hover {
                                        background-color: #3A7;
                                    }
                                    QComboBox QAbstractItemView {
                                        background-color: #2E2E2E;  # Match dropdown background with main background
                                        color: #FFFFFF;  # White text color
                                        border: 2px solid #1ABC9C;
                                        selection-background-color: #3A7;  # Color for selected item
                                    }
                                """)
                    elif self.radioButton_double.isChecked():
                        self.radioButton_Rx_1.setVisible(False)
                        self.radioButton_Rx_2.setVisible(False)
                        self.lineEdit_4.setVisible(True)
                        self.lineEdit_bandwidth_2.setVisible(True)
                        self.comboBox_2.setVisible(True)
                        self.label_4.setVisible(True)
                        self.lineEdit_4.setEnabled(True)
                        self.lineEdit_bandwidth_2.setEnabled(True)
                        self.comboBox_2.setEnabled(True)
                        self.lineEdit_gain_1.setEnabled(True)
                        self.lineEdit_gain_2.setEnabled(True)
                        self.lineEdit_samplingfreq_2.setEnabled(True)
                   
                        self.lineEdit_3.setEnabled(True)
                        self.lineEdit_bandwidth.setEnabled(True)
                        self.comboBox.setEnabled(True)
                        self.lineEdit_gain_1.setEnabled(True)
                        self.lineEdit_gain_2.setEnabled(True)
                        self.lineEdit_samplingfreq.setEnabled(True)
                        self.label_4.setEnabled(False)
                        self.lineEdit_gain_2.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                        self.lineEdit_gain_1.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                        self.lineEdit_4.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #2E5;
                                            }
                                        """)
                        self.lineEdit_bandwidth_2.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #2C3E50;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                        self.lineEdit_samplingfreq_2.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #2C3E50;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                        self.comboBox_2.setStyleSheet("""
                                QComboBox {
                                    background-color: #2C3E50;
                                    color: #FFFFFF;
                                    border: 2px solid #1ABC9C;
                                    border-radius: 5px;
                                    padding: 5px;
                                }
                                QComboBox::drop-down {
                                    width: 30px;  # Adjust the width of the drop-down arrow area
                                    border-left: 2px solid #1ABC9C;
                                    background-color: #2C3E50;
                                }
                                QComboBox::down-arrow {
                                    width: 12px;
                                    height: 12px;
                                }
                                QComboBox::down-arrow:!editable {
                                    color: #FFFFFF;  # Set the color of the "v"
                                    text-align: center;
                                    content: "v";  # Use "v" as the dropdown arrow
                                }
                                QComboBox::hover {
                                    background-color: #3A7;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: #2E2E2E;  # Match dropdown background with main background
                                    color: #FFFFFF;  # White text color
                                    border: 2px solid #1ABC9C;
                                    selection-background-color: #3A7;  # Color for selected item
                                }
                            """)
                        self.lineEdit_3.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #2C3E50;
                                                color: #FFFFFF;
                                                border: 2px solid #1ABC9C;
                                                border-radius: 5px;
                                                padding: 5px;
                                            }
                                            QLineEdit:focus {
                                                border: 2px solid #2E5;
                                            }
                                        """)
                        self.lineEdit_bandwidth.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #2C3E50;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                        self.lineEdit_samplingfreq.setStyleSheet("""
                                                        QLineEdit {
                                                            background-color: #2C3E50;
                                                            color: #FFFFFF;
                                                            border: 2px solid #1ABC9C;
                                                            border-radius: 5px;
                                                            padding: 5px;
                                                        }
                                                        QLineEdit:focus {
                                                            border: 2px solid #2E5;
                                                        }
                                                    """)
                        self.comboBox.setStyleSheet("""
                                QComboBox {
                                    background-color: #2C3E50;
                                    color: #FFFFFF;
                                    border: 2px solid #1ABC9C;
                                    border-radius: 5px;
                                    padding: 5px;
                                }
                                QComboBox::drop-down {
                                    width: 30px;  # Adjust the width of the drop-down arrow area
                                    border-left: 2px solid #1ABC9C;
                                    background-color: #2C3E50;
                                }
                                QComboBox::down-arrow {
                                    width: 12px;
                                    height: 12px;
                                }
                                QComboBox::down-arrow:!editable {
                                    color: #FFFFFF;  # Set the color of the "v"
                                    text-align: center;
                                    content: "v";  # Use "v" as the dropdown arrow
                                }
                                QComboBox::hover {
                                    background-color: #3A7;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: #2E2E2E;  # Match dropdown background with main background
                                    color: #FFFFFF;  # White text color
                                    border: 2px solid #1ABC9C;
                                    selection-background-color: #3A7;  # Color for selected item
                                }
                            """)
                    self.radioButton_double.setVisible(False)
                    self.radioButton_single.setVisible(False)
                    self.label_radio.setVisible(False)
                    self.lineEdit_hostname.setVisible(False)
                    self.lineEdit_password.setVisible(False)
                    self.label_ssid.setVisible(False)
                    self.label_hostname.setVisible(False)
                    self.label_gpiomode.setVisible(False)
                    self.radioButton_gpiomode.setVisible(False)
                    self.radioButton_rfmdmode.setVisible(False)
                    self.radioButton_autoplay.setVisible(False)
                    self.label_Gain_Tx.setVisible(False)
                    self.label_Gain_Tx_2ch.setVisible(False)
                    self.label_Gain_Tx_2_2ch.setVisible(False) 
                    self.label_Gain_Tx_2.setVisible(False)
                    self.lineEdit_Gain_Tx_2.setVisible(False)
                    self.label_Gain_Tx_3ch.setVisible(False)
                    self.line_vertical_Replay.setVisible(False)
                    self.lineEdit_Gain_Tx.setVisible(False)
                    self.lineEdit_rate.setVisible(False)
                    self.label_rate.setVisible(False)
                    self.label_connectivity.setVisible(False)
                    self.pushButton_4.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_2.setStyleSheet("QPushButton{"
                                            "background-color: #1ABC9C;"
                                            "color: white;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_5.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_login.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton_select_file.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                    self.pushButton.setVisible(True)
                    self.pushButton_2.setVisible(True)
                    self.pushButton_login.setEnabled(True)
                    self.pushButton_3.setVisible(True)
                    self.pushButton_4.setVisible(True)
                    self.pushButton_5.setVisible(True)
                    self.lineEdit.setVisible(True)
                    self.lineEdit_2.setVisible(True)
                    self.lineEdit_3.setVisible(True)
                    
                    self.lineEdit_6.setVisible(True)
                    self.label.setVisible(True)
                    self.label_10.setVisible(True)
                    self.label_2.setVisible(True)
                    self.label_3.setVisible(True)
                    self.label_5.setVisible(True)
                    self.label_8.setVisible(True)
                    self.label_9.setVisible(False)
                    self.comboBox.setVisible(True)
                    self.label_bandwidth.setVisible(True)
                    self.label_gain.setVisible(True)
                    self.lineEdit_bandwidth.setVisible(True)
                    self.lineEdit_replay.setVisible(False)
                    self.lineEdit_gain_1.setVisible(True)
                    self.lineEdit_gain_2.setVisible(True)
                    self.label_replay.setVisible(False)
                    self.label_connected.setVisible(False)
                    self.label_connected_rtcm.setVisible(False)
                    self.button_reconnect.setVisible(False)
                    self.button_reboot.setVisible(False)
                    self.button_shutdown.setVisible(False)

                    self.pushButton_6.setVisible(False)
                    self.pushButton_7.setVisible(False)
                    self.lineEdit_7.setVisible(False)
                    self.lineEdit_8.setVisible(False)
                    self.label_11.setVisible(False)
                    self.label_12.setVisible(False)
                    self.radioButton_GPIO_Replay.setVisible(False)
                    self.pushButton_8.setVisible(False)
                    self.lineEdit9.setVisible(False)
                    self.lineEdit_replay_rtcm.setVisible(False)
                    self.pushButton_browse_replay_rtcm.setVisible(False)
                    self.label_files_rtcm.setVisible(False)
                    self.label_13.setVisible(False)
                    self.label_about_2.setVisible(False)
                    self.label_about_3.setVisible(False)
                    self.pushButton_submit.setVisible(False)
                    self.comboBox_baudrate.setVisible(False)
                    self.comboBox_comport.setVisible(False)
                    self.label_ref_freq.setVisible(False)
                    self.comboBox_ref_freq.setVisible(False)
                    self.comboBox_baudrate_rtcm.setVisible(False)
                    self.radioButton_ad9361.setVisible(False)
                    self.radioButton_rtcm.setVisible(False)
                    self.lineEdit_deviceid.setVisible(False)
                    self.label_deviceid.setVisible(False)
                    self.lineEdit_busno.setVisible(False)
                    self.label_busno.setVisible(False)
                    self.pushButton_usb_info.setVisible(False)
                    self.comboBox_comport_rtcm.setVisible(False)
                    self.line_2.setVisible(True)
                    if only_ad9361:
                         self.lineEdit_browse_record_rtcm.clear()
                         self.lineEdit_browse_record_rtcm.setEnabled(False)
                         self.pushButton_browse_record_rtcm.setEnabled(True)
                         self.show_path_btn_rtcm.setEnabled(True)
                         self.hide_path_btn_rtcm.setEnabled(False)
                         self.lineEdit_browse_record.setEnabled(True)
                         self.pushButton_browse_record.setEnabled(True)
                         self.show_path_btn.setEnabled(True)
                         self.hide_path_btn.setEnabled(True)
                         self.lineEdit_browse_record_rtcm.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         self.lineEdit_browse_record.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                    elif only_rtcm:
                         self.lineEdit_browse_record_rtcm.setEnabled(True)
                         self.pushButton_browse_record_rtcm.setEnabled(True)
                         self.show_path_btn_rtcm.setEnabled(True)
                         self.hide_path_btn_rtcm.setEnabled(True)
                         self.lineEdit_browse_record.setEnabled(False)
                         self.pushButton_browse_record.setEnabled(False)
                         self.show_path_btn.setEnabled(False)
                         self.hide_path_btn.setEnabled(False)
                         self.lineEdit_browse_record_rtcm.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                         self.lineEdit_browse_record.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
                    if checked_both_without_HWUSB or HW_USB_in_use:
                        print("\n\n\n\n\n\njiiiiiiiiiiiiiiiiiiiiiiii")
                        self.lineEdit_browse_record_rtcm.setEnabled(True)
                        self.pushButton_browse_record_rtcm.setEnabled(True)
                        self.show_path_btn_rtcm.setEnabled(True)
                        self.hide_path_btn_rtcm.setEnabled(True)
                        self.lineEdit_browse_record.setEnabled(True)
                        self.pushButton_browse_record.setEnabled(True)
                        self.show_path_btn.setEnabled(True)
                        self.hide_path_btn.setEnabled(True)
                        self.lineEdit_browse_record_rtcm.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                        self.lineEdit_browse_record.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
                else:
                    msg_box_9 = QMessageBox()
                    msg_box_9.setWindowTitle("Error!")
                    msg_box_9.setText("Please Submit a valid label for nvme SSD")
                    msg_box_9.exec() 
            else:
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Missing Data")
                msg_box_9.setText("Please select the Com port")
                msg_box_9.exec()
        else:
            if replay_started:
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Replay is ON!")
                msg_box_9.setText("You cannot switch to Recording while Replay is ON!")
                msg_box_9.exec()

    def get_recording_progress(self, text):
        self.progressrecording = text.strip()

    def get_replay_progress(self, text):
        self.progressreplay = text.strip()

    def get_samplingfreq_2(self, text):
        self.samplingfreq_2 = text.strip()
        self.get_max_duration_theorotical()
        if self.radioButton_double.isChecked():
            self.lineEdit_samplingfreq.setText(self.samplingfreq_2)

    def get_samplingfreq(self, text):
        self.samplingfreq_1 = text.strip()
        self.get_max_duration_theorotical()
        if self.radioButton_double.isChecked():
            self.lineEdit_samplingfreq_2.setText(self.samplingfreq_1)

    def get_start_time(self, text):
        self.start_time_value = text.strip()

    def get_stop_time(self, text):
        self.stop_time_value = text.strip()   

    def get_Rate(self, text):
        self.rate = text.strip()

    def read_decoded_line(self):
        global ser
        if interface_in_use == 0:
            return read_serial_decoded_line(ser)
        else:
            return read_wifi_decoded_line(ser)
		
    def rtcm_record_command(self, filepath):
        filepath = filepath
        if device_id == "" and bus_no == "":
            command = f"/home/root/adc4bits/libiio/build/examples/RTCMrx {self.baudrate_rtcm} >{filepath}.rtcm&"
        else:
            command = f"/home/root/adc4bits/libiio/build/examples/RTCMrx {self.baudrate_rtcm} {bus_no} {device_id} >{filepath}.rtcm&"
        with open(file_path, 'a') as file:
            file.write(f"\n{get_current_datetime()}   {command}")
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active:
            send_command(bytearray(command,'ascii'))
            with open(file_path, 'a') as file:
                file.write(f'\n{get_current_datetime()}   {command}\n')


    def rtcm_replay_command(self, filepath, autoreplay, startoffset_HW_rtcm, runduration_HW_rtcm):
        filepath = filepath
        if device_id == "" and bus_no == "":
            command = f"/home/root/adc4bits/libiio/build/examples/RTCMtx {self.baudrate_rtcm} {filepath} {autoreplay} {startoffset_HW_rtcm} {runduration_HW_rtcm}&"
        else:
            command = f"/home/root/adc4bits/libiio/build/examples/RTCMtx {self.baudrate_rtcm} {filepath} {autoreplay} {startoffset_HW_rtcm} {runduration_HW_rtcm} {bus_no} {device_id}&"
        with open(file_path, 'a') as file:
            file.write(f"\n{get_current_datetime()}   {command}")
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active:
            send_command(bytearray(command,'ascii'))
            with open(file_path, 'a') as file:
                file.write(f'\n{get_current_datetime()}   {command}\n')
        
    def start_timer_replay(self):
        global replay_started, replay_terminated, read_Replay_response, ser, start_time_valid, stop_time_valid, nolog_high, log_duration, check_flag, replayed_time, replay_terminated, read_Replay_response
        global path_auto, filename_auto, duration_auto, startoffset_auto
        def check_replaying():
            global replay_terminated, replay_started
            while True:
                if read_Replay_response:
                    line = self.read_decoded_line()
                    print(line)
                    if "Terminated before the full duration!" in line:
                        replay_terminated = True
                        break
                else:
                    break

        read_Replay_response = True
        replay_terminated = False
        
        if nolog_high:
            log_duration = rx1_duration
        else:
            if self.radioButton_double.isChecked():
                log_duration = log_duration
            if log_duration == "Not found":
                log_duration = log_duration_2
            print(f"log_duration: {log_duration}")
            log_duration = validate_time(str(log_duration))
            
        ###############################################
        if not replay_started:
            ##############################################
            if checked_both_without_HWUSB:
                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                if not comport_2_rtcm:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                    msg_box_2.exec()
                    self.open_after_disconnection()
                    return
            if refile:
                if self.start_time_value == "":
                    self.start_time_value = None
                    print(self.start_time_value)
                if self.stop_time_value == "":
                    self.stop_time_value = None
            
            print(self.start_time_value)
            print(self.stop_time_value)

            self.lineEdit_replay.clear()
            if (self.file_name_replay is None):
                #print("Condition met!")
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Missing Data")
                msg_box_2.setText("Please enter the required data before recording")
                msg_box_2.exec()
                return
            if (self.file_name_replay == ""):
                #print("Condition met!")
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Missing Data")
                msg_box_2.setText("Please enter the required data before recording")
                msg_box_2.exec()
                return
            
            if self.label_Gain_Tx_2.isChecked() or self.radioButton_double.isChecked():
                tx_gain_2 = self.lineEdit_Gain_Tx_2.text()
                if tx_gain_2 == "":
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText("Please enter the required data before recording")
                    msg_box_2.exec() 
                    return
                try:
                    tx_gain_2 = float(tx_gain_2)
                except ValueError:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error")
                    msg_box_2.setText("Please enter a valid Gain!")
                    msg_box_2.exec()
                    return 
                if tx_gain_2 > 0 or tx_gain_2 < -89.75:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error!")
                    msg_box_2.setText("Gain should be between 0dB and -89.75dB")
                    msg_box_2.exec() 
                    return  
                if self.label_Gain_Tx_2.isChecked():
                    tx_gain = self.lineEdit_Gain_Tx_2.text()
                elif self.radioButton_double.isChecked():
                    tx_gain = self.lineEdit_Gain_Tx.text()

            if self.label_Gain_Tx.isChecked() or self.radioButton_double.isChecked():
                tx_gain = self.lineEdit_Gain_Tx.text()
                if tx_gain == "":
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText("Please enter the required data before recording")
                    msg_box_2.exec() 
                    return
                try:
                    tx_gain = float(tx_gain)
                except ValueError:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error")
                    msg_box_2.setText("Please enter a valid Gain!")
                    msg_box_2.exec()
                    return 
                if tx_gain > 0 or tx_gain < -89.75:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error!")
                    msg_box_2.setText("Gain should be between 0dB and -89.75dB")
                    msg_box_2.exec() 
                    return  
                if self.label_Gain_Tx.isChecked():
                    tx_gain_2 = self.lineEdit_Gain_Tx.text()
                elif self.radioButton_double.isChecked():
                    tx_gain_2 = self.lineEdit_Gain_Tx_2.text()
            ###########################################################################
            if checked_both_without_HWUSB or HW_USB_in_use:
                if self.file_name_replay_rtcm is None:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText("Please enter the required data before replaying")
                    msg_box_2.exec()  
                    return
                try:
                    self.rate = self.lineEdit_rate.text()
                    self.rate = float(self.rate)
                    print(self.rate)
                except ValueError:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error")
                    msg_box_2.setText("Please enter a valid Rate")
                    msg_box_2.exec()
                    return
                ############################################################
                real_File_name = str(self.file_name_replay).split("/")
                if len(real_File_name) >=2:
                    real_File_name = real_File_name[-1]
                else:
                    real_File_name = real_File_name[0]
                ##############################################################
                if not real_File_name == rtcm_file_name:
                    msg_box_compare = QMessageBox()
                    msg_box_compare.setWindowTitle("Warning")
                    #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                    msg_box_compare.setInformativeText("Filenames are not same, do you want to continue?")
                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                    reply_3 = msg_box_compare.exec()
                    if reply_3 == QMessageBox.StandardButton.Yes:
                        check_flag = True
                        pass
                    else:
                        check_flag = False
                        return   
            print(self.start_time_value)
            print(self.stop_time_value)     
            ################################################################################
            if self.start_time_value is not None:
                start_time_valid = validate_time(self.start_time_value)
                if start_time_valid == None:
                    msg_box_error = QMessageBox()
                    msg_box_error.setWindowTitle("Invalid Format")
                    msg_box_error.setText("Start time value is in a wrong format")
                    msg_box_error.exec()
                    return
                
            if self.stop_time_value is not None:
                stop_time_valid = validate_time(self.stop_time_value)
                if stop_time_valid == None:
                    msg_box_error = QMessageBox()
                    msg_box_error.setWindowTitle("Invalid Format")
                    msg_box_error.setText("Stop time value is in a wrong format")
                    msg_box_error.exec()
                    return
                
            if self.start_time_value is None:
                start_time_valid = "00:00:00"
                print(start_time_valid)
            if self.stop_time_value is None:
                if self.start_time_value is None:
                    stop_time_valid = str(log_duration)
                else:
                    stop_time_valid = subtract_two_times(start_time_valid, str(log_duration))

            if not self.timer_started_1:
                if (start_time_valid) is not None:
                    # Parse the start time value and set it as the initial elapsed time
                    start_time = QTime.fromString(start_time_valid, "HH:mm:ss")
                    self.elapsed_time = start_time
                    self.start_time_1 = QTime.currentTime()
                    #print("Entered start time is:", self.start_time_value)
                    if (start_time_valid > str(log_duration)):
                        msg_box_start_time_reply = QMessageBox()
                        msg_box_start_time_reply.setWindowTitle("Confirmation")
                        msg_box_start_time_reply.setText(f"Start time is greater than the duration({log_duration})")
                        msg_box_start_time_reply.setIcon(QMessageBox.Icon.Information)
                        #Execute the message box
                        reply = msg_box_start_time_reply.exec()
                        return
                
                print(start_time_valid)
                print(stop_time_valid)
                result = add_two_times(start_time_valid, stop_time_valid)
                print(result)
                print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                #print(result)
                if (stop_time_valid is not None):
                    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                    if (result > str(log_duration)):
                        print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                        msg_box_stop_time_reply = QMessageBox()
                        msg_box_stop_time_reply.setWindowTitle("Confirmation")
                        msg_box_stop_time_reply.setText(f"Stop time is greater than the duration({log_duration}), Do you like to replay till available duration?")
                        msg_box_stop_time_reply.setIcon(QMessageBox.Icon.Question)
                        msg_box_stop_time_reply.addButton(QMessageBox.StandardButton.Yes)
                        msg_box_stop_time_reply.addButton(QMessageBox.StandardButton.No)
                        msg_box_stop_time_reply.setDefaultButton(QMessageBox.StandardButton.No) 
                        #Execute the message box
                        reply = msg_box_stop_time_reply.exec()

                        if reply == QMessageBox.StandardButton.Yes:
                            self.lineEdit_7.setEnabled(False)
                            self.lineEdit_8.setEnabled(False)
                            self.radioButton_autoplay.setEnabled(False)
                            ######################## Auto-Replay ##################
                            if self.radioButton_autoplay.isChecked():
                                self.autoreplay = 1
                            else:
                                self.autoreplay = 0
                            ########################################################
                            real_File_name = str(self.file_name_replay).split("/")
                            if len(real_File_name) >=2:
                                real_File_name = real_File_name[-1]
                            else:
                                real_File_name = real_File_name[0]
                            ##########################################################
                            replay_started = True
                            self.label_Gain_Tx.setEnabled(False)
                            self.label_Gain_Tx_2.setEnabled(False)
                            self.lineEdit_Gain_Tx.setEnabled(False)
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(False) and self.radioButton_GPIO_Record.setEnabled(False)
                            self.lineEdit_Gain_Tx_2.setEnabled(False)
                            if start_time_valid == "00:00:00":
                                self.lineEdit_7.setText(log_duration)
                                stop_time_valid = log_duration

                            else:
                                time = subtract_two_times(start_time_valid, log_duration)
                                self.lineEdit_7.setText(time)
                                stop_time_valid = time

                            self.lineEdit_8.setText(start_time_valid)
                            self.green_light.setVisible(True)
                            self.pushButton_invisible.setVisible(False)
                            self.pushButton_pdf.setVisible(False)

                            self.red_light.setVisible(False)
                            
                            #print("Selected yes")
                            #ser = serial.Serial(self.comport, self.baudrate, timeout=2)
                            #./main <mode> <start_offset> <run_duration> <file_path>
                            start_time_in_sec = time_to_seconds(start_time_valid)
                            duration_in_sec = time_to_seconds(log_duration)
                            print(real_File_name)
                            
                            if self.label_Gain_Tx.isChecked():
                                mode = 1
                            if self.label_Gain_Tx_2.isChecked():
                                mode = 5
                            if self.radioButton_double.isChecked():
                                mode = 3
                            if nolog_high:
                                if single_channel_rx1_replay:
                                    rx1_bw_obtained = rx1_bw
                                    rx2_bw_obtained = rx1_bw
                                    rx1_sf_obtained = rx1_sf
                                    rx2_sf_obtained = rx1_sf
                                    rx1_cf_obtained = rx1_cf
                                    rx2_cf_obtained = rx1_cf
                                    rx1_adc_obtained = rx1_adc
                                    rx2_adc_obtained = rx1_adc
                                    rx_duration_obtained = time_to_seconds(rx1_duration)
                                elif single_channel_rx2_replay:
                                    rx1_bw_obtained = rx2_bw
                                    rx2_bw_obtained = rx2_bw
                                    rx1_sf_obtained = rx2_sf
                                    rx2_sf_obtained = rx2_sf
                                    rx1_cf_obtained = rx2_cf
                                    rx2_cf_obtained = rx2_cf
                                    rx1_adc_obtained = rx2_adc
                                    rx2_adc_obtained = rx2_adc
                                    rx_duration_obtained = time_to_seconds(rx2_duration)
                                elif Dual_channel_replay:
                                    rx1_bw_obtained = rx1_bw
                                    rx2_bw_obtained = rx2_bw
                                    rx1_sf_obtained = rx1_sf
                                    rx2_sf_obtained = rx2_sf
                                    rx1_cf_obtained = rx1_cf
                                    rx2_cf_obtained = rx2_cf
                                    rx1_adc_obtained = rx1_adc
                                    rx2_adc_obtained = rx2_adc
                                    rx_duration_obtained = time_to_seconds(rx1_duration)

                            if not nolog_high:
                                final_string_replay = (
                                    f"{executable_tx} "                                # executable_tx
                                    f"{mode} "           # Var1
                                    f"{start_time_in_sec} "           # Var1
                                    f"{duration_in_sec} "           # Var2
                                    f'"{Lg_path}"'                                    # Var3
                                    f'"{real_File_name}.bin" ' 
                                    f"{tx_gain} "                    
                                    f"{tx_gain_2} "                    
                                    f"{self.autoreplay} "
                                    f"{self.reference_frequency} "     
                                    f'| tee -i "{Lg_path}{real_File_name}.txlog" \n'                   
                                )
                            else:
                                final_string_replay = (
                                    f"{executable_tx} "                                # executable_tx
                                    f"{mode} "           # Var1
                                    f"{start_time_in_sec} "           # Var1
                                    f"{duration_in_sec} "           # Var2
                                    f'"{Lg_path}"'                                    # Var3
                                    f'"{real_File_name}.bin" ' 
                                    f"{tx_gain} "                    
                                    f"{tx_gain_2} "                    
                                    f"{self.autoreplay} "
                                    f"{self.reference_frequency} "
                                    f"{rx1_bw_obtained}e6 "
                                    f"{rx2_bw_obtained}e6 "
                                    f"{rx1_sf_obtained}e6 "
                                    f"{rx2_sf_obtained}e6 "
                                    f"{rx1_cf_obtained}e6 "
                                    f"{rx2_cf_obtained}e6 "
                                    f"{rx1_adc_obtained} "
                                    f"{rx2_adc_obtained} "
                                    f"{rx_duration_obtained} "
                                    f'| tee -i "{Lg_path}{real_File_name}.txlog" \n'                    
                                )
                                #print("the command is ",final_string_replay)
                            if checked_both_without_HWUSB:
                                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                                if not comport_2_rtcm:
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Missing Data")
                                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                                    msg_box_2.exec()
                                    self.open_after_disconnection()
                                    return
                                
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                path_auto = Lg_path
                                filename_auto = f"{real_File_name}.gpio"
                                duration_auto = duration_in_sec
                                startoffset_auto = start_time_in_sec
                                #self.GPIO_record_replay(Lg_path, f"{real_File_name}.gpio", duration_in_sec, start_time_in_sec)
                                result = self.GPIO_record_replay(Lg_path, f"{real_File_name}.gpio", duration_in_sec, start_time_in_sec)
                                if result == 0:
                                    print("No response from GPIO check (lines were None)")
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Time out")
                                    msg_box_2.setText(f"response not received within the time limit!")
                                    msg_box_2.exec()
                                    return
                                elif result == 1:
                                    print("File exists — starting replay...")
                                    pass
                                elif result == 2:
                                    msg_box_compare = QMessageBox()
                                    msg_box_compare.setWindowTitle("Warning")
                                    msg_box_compare.setText(f"\"{real_File_name}.gpio\" file not found!")
                                    msg_box_compare.setInformativeText("Are you sure you want to continue?")
                                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                    reply_ = msg_box_compare.exec()
                                    if reply_ == QMessageBox.StandardButton.Yes: 
                                        #send_command(bytearray(f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR replay {path_auto}{filename_auto} {int(duration_auto)+1} {startoffset_auto}&\n", 'ascii'))        
                                        pass
                                    else:
                                        replayed_time = False
                                        self.lineEdit_7.setEnabled(True)
                                        self.lineEdit_8.setEnabled(True)
                                        self.radioButton_autoplay.setEnabled(True)
                                        replay_started = False
                                        self.timer_started_1 = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                        if self.radioButton_double.isChecked():
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                        if self.radioButton_single.isChecked():
                                            if self.label_Gain_Tx.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                                            if self.label_Gain_Tx_2.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(False)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                                        self.green_light.setVisible(False)
                                        self.pushButton_invisible.setVisible(False)
                                        self.pushButton_pdf.setVisible(False)
                                        self.red_light.setVisible(True)
                                        return
                                    print("File not found — cannot start replay")
                                else:
                                    print("Unexpected result:", result)

                            if HW_USB_in_use:
                                file_command = f"{rtcm_file_path}"
                                self.rtcm_replay_command(file_command, self.autoreplay, start_time_in_sec, duration_in_sec)

                            if comport_is_active: 
                                send_command(bytearray(final_string_replay,'ascii'))
                                self.worker.running = True  # Ensure the thread runs when started
                                self.worker.start()
                                replaying_thread = threading.Thread(target=check_replaying)
                                replaying_thread.start()
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   {final_string_replay}")
                                lines = read_line()
                                #print(lines)
                                decoded_lines = [line.decode('UTF-8') for line in lines]
                                print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

                                #print(decoded_lines)
                            else:
                                replayed_time = False
                                self.lineEdit_7.setEnabled(True)
                                self.lineEdit_8.setEnabled(True)
                                self.radioButton_autoplay.setEnabled(True)
                                replay_started = False
                                self.timer_started_1 = False
                                self.worker.stop()  # Tell the thread to stop
                                self.worker.wait()
                                self.worker.running = False
                                if self.radioButton_gpiomode.isChecked():
                                    self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                if self.radioButton_double.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                if self.radioButton_single.isChecked():
                                    if self.label_Gain_Tx.isChecked():
                                        self.lineEdit_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx_2.setEnabled(True)
                                        self.lineEdit_Gain_Tx_2.setEnabled(False)
                                    if self.label_Gain_Tx_2.isChecked():
                                        self.lineEdit_Gain_Tx.setEnabled(False)
                                        self.label_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx_2.setEnabled(True)
                                        self.lineEdit_Gain_Tx_2.setEnabled(True)
                                self.green_light.setVisible(False)
                                self.pushButton_invisible.setVisible(False)
                                self.pushButton_pdf.setVisible(False)
                                self.red_light.setVisible(True)
                                self.stop_GPIO_record_replay()
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not replay")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            for line in decoded_lines:
                                #print(line)
                                if "Replayed time:" in line:
                                    replayed_time = True
                                if "Destroying" in line:
                                    if not replayed_time:
                                        read_Replay_response = False
                                        self.timer_started_1 = False
                                        replayed_time = False
                                        self.lineEdit_7.setEnabled(True)
                                        self.lineEdit_8.setEnabled(True)
                                        self.radioButton_autoplay.setEnabled(True)
                                        replay_started = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                        if self.radioButton_double.isChecked():
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                        if self.radioButton_single.isChecked():
                                            if self.label_Gain_Tx.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                                            if self.label_Gain_Tx_2.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(False)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                                        self.green_light.setVisible(False)
                                        self.pushButton_invisible.setVisible(False)
                                        self.pushButton_pdf.setVisible(False)
                                        self.red_light.setVisible(True)
                                        self.stop_GPIO_record_replay()
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"Error occured! Replay not started!")
                                        msg_box_11.exec()     
                                        return
                            ########################################
                            self.timer_1.start(1000)  # Start the timer with 1 second interval
                            self.timer_started_1 = True
                            replayed_time = False
                            ########################################
                        elif reply == QMessageBox.StandardButton.No:
                            #print("Selected No")
                            #Don't start the timer, remain in the same state
                            return
                    else:
                        if not check_flag:
                            msg_box_stop_time_reply_1 = QMessageBox()
                            msg_box_stop_time_reply_1.setWindowTitle("Confirmation")
                            msg_box_stop_time_reply_1.setText(f"Do you want to start the replay?")
                            msg_box_stop_time_reply_1.setIcon(QMessageBox.Icon.Question)
                            msg_box_stop_time_reply_1.addButton(QMessageBox.StandardButton.Yes)
                            msg_box_stop_time_reply_1.addButton(QMessageBox.StandardButton.No)
                            msg_box_stop_time_reply_1.setDefaultButton(QMessageBox.StandardButton.No) 
                            #Execute the message box
                            reply_2 = msg_box_stop_time_reply_1.exec()

                            if reply_2 == QMessageBox.StandardButton.Yes:
                                 check_flag = True
                                 pass
                            else:
                                 return
                        if check_flag:
                            check_flag = False
                            self.lineEdit_7.setEnabled(False)
                            self.lineEdit_8.setEnabled(False)
                            self.radioButton_autoplay.setEnabled(False)

                            if not self.ensure_interface_connection(timeout_time):
                                self.open_after_disconnection()
                                return

                            ######################## Auto-Replay ##################
                            if self.radioButton_autoplay.isChecked():
                                self.autoreplay = 1
                            else:
                                self.autoreplay = 0
                            ########################################################
                            if nolog_high:
                                log_duration = rx1_duration
                            else:
                                 log_duration = log_duration

                            real_File_name = str(self.file_name_replay).split("/")
                            print(real_File_name)
                            if len(real_File_name) >=2:
                                real_File_name = real_File_name[-1]
                            else:
                                real_File_name = real_File_name[0]    
                                
                            replay_started = True
                            self.label_Gain_Tx.setEnabled(False)
                            self.label_Gain_Tx_2.setEnabled(False)
                            self.lineEdit_Gain_Tx.setEnabled(False)
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(False) and self.radioButton_GPIO_Record.setEnabled(False)
                            self.lineEdit_Gain_Tx_2.setEnabled(False)
                            if start_time_valid == "00:00:00":
                                if stop_time_valid == "":
                                    self.lineEdit_7.setText(log_duration)
                                    stop_time_valid = log_duration
                                else:
                                    self.lineEdit_7.setText(stop_time_valid)
                            else:
                                if stop_time_valid == "":
                                    time = subtract_two_times(start_time_valid, log_duration)
                                    self.lineEdit_7.setText(time)
                                    stop_time_valid = time
                                else:
                                    self.lineEdit_7.setText(stop_time_valid)

                            self.lineEdit_8.setText(start_time_valid)
                            self.green_light.setVisible(True)
                            self.pushButton_invisible.setVisible(False)
                            self.pushButton_pdf.setVisible(False)
                            self.red_light.setVisible(False)
                            # Start the timer here automatically
                            #self.timer_1.start(1000)  # Start the timer with 1 second interval
                            #self.timer_started_1 = True
                            #ser = serial.Serial(self.comport, self.baudrate, timeout=2)
                            start_time_in_sec = time_to_seconds(start_time_valid)
                            duration_in_sec = time_to_seconds(stop_time_valid)
                            
                            if self.label_Gain_Tx.isChecked():
                                mode = 1
                            if self.label_Gain_Tx_2.isChecked():
                                mode = 5
                            if self.radioButton_double.isChecked():
                                mode = 3

                            if nolog_high:
                                if single_channel_rx1_replay:
                                    rx1_bw_obtained = rx1_bw
                                    rx2_bw_obtained = rx1_bw
                                    rx1_sf_obtained = rx1_sf
                                    rx2_sf_obtained = rx1_sf
                                    rx1_cf_obtained = rx1_cf
                                    rx2_cf_obtained = rx1_cf
                                    rx1_adc_obtained = rx1_adc
                                    rx2_adc_obtained = rx1_adc
                                    rx_duration_obtained = time_to_seconds(rx1_duration)
                                elif single_channel_rx2_replay:
                                    rx1_bw_obtained = rx2_bw
                                    rx2_bw_obtained = rx2_bw
                                    rx1_sf_obtained = rx2_sf
                                    rx2_sf_obtained = rx2_sf
                                    rx1_cf_obtained = rx2_cf
                                    rx2_cf_obtained = rx2_cf
                                    rx1_adc_obtained = rx2_adc
                                    rx2_adc_obtained = rx2_adc
                                    rx_duration_obtained = time_to_seconds(rx2_duration)
                                elif Dual_channel_replay:
                                    rx1_bw_obtained = rx1_bw
                                    rx2_bw_obtained = rx2_bw
                                    rx1_sf_obtained = rx1_sf
                                    rx2_sf_obtained = rx2_sf
                                    rx1_cf_obtained = rx1_cf
                                    rx2_cf_obtained = rx2_cf
                                    rx1_adc_obtained = rx1_adc
                                    rx2_adc_obtained = rx2_adc
                                    rx_duration_obtained = time_to_seconds(rx1_duration)
                            
                            if not nolog_high:
                                final_string_replay = (
                                    f"{executable_tx} "                                # executable_tx
                                    f"{mode} "           # Var1
                                    f"{start_time_in_sec} "           # Var1
                                    f"{duration_in_sec} "           # Var2
                                    f'"{Lg_path}"'                                    # Var3
                                    f'"{real_File_name}.bin" '  
                                    f"{tx_gain} "                    
                                    f"{tx_gain_2} "                    
                                    f"{self.autoreplay} "
                                    f"{self.reference_frequency} "     
                                    f'| tee -i "{Lg_path}{real_File_name}.txlog" \n'                   
                                )
                            else:
                                final_string_replay = (
                                    f"{executable_tx} "                                # executable_tx
                                    f"{mode} "           # Var1
                                    f"{start_time_in_sec} "           # Var1
                                    f"{duration_in_sec} "           # Var2
                                    f'"{Lg_path}"'                                    # Var3
                                    f'"{real_File_name}.bin" '
                                    f"{tx_gain} "                    
                                    f"{tx_gain_2} "                    
                                    f"{self.autoreplay} "
                                    f"{self.reference_frequency} "
                                    f"{rx1_bw_obtained}e6 "
                                    f"{rx2_bw_obtained}e6 "
                                    f"{rx1_sf_obtained}e6 "
                                    f"{rx2_sf_obtained}e6 "
                                    f"{rx1_cf_obtained}e6 "
                                    f"{rx2_cf_obtained}e6 "
                                    f"{rx1_adc_obtained} "
                                    f"{rx2_adc_obtained} "
                                    f"{rx_duration_obtained} "
                                    f'| tee -i "{Lg_path}{real_File_name}.txlog" \n'                    
                                )   
                            if checked_both_without_HWUSB:
                                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                                if not comport_2_rtcm:
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Missing Data")
                                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                                    msg_box_2.exec()
                                    self.open_after_disconnection()
                                    return
                                
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                path_auto = Lg_path
                                filename_auto = f"{real_File_name}.gpio"
                                duration_auto = duration_in_sec
                                startoffset_auto = start_time_in_sec
                                #self.GPIO_record_replay(Lg_path, f"{real_File_name}.gpio", duration_in_sec, start_time_in_sec)
                                result = self.GPIO_record_replay(Lg_path, f"{real_File_name}.gpio", duration_in_sec, start_time_in_sec)
                                if result == 0:
                                    print("No response from GPIO check (lines were None)")
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Time out")
                                    msg_box_2.setText(f"response not received within the time limit!")
                                    msg_box_2.exec()
                                    return
                                elif result == 1:
                                    print("File exists — starting replay...")
                                    pass
                                elif result == 2:
                                    msg_box_compare = QMessageBox()
                                    msg_box_compare.setWindowTitle("Warning")
                                    msg_box_compare.setText(f"\"{real_File_name}.gpio\" file not found!")
                                    msg_box_compare.setInformativeText("Are you sure you want to continue?")
                                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                    reply_ = msg_box_compare.exec()
                                    if reply_ == QMessageBox.StandardButton.Yes: 
                                        #send_command(bytearray(f"sudo /home/root/adc4bits/libiio/build/examples/GPIO_RR replay {path_auto}{filename_auto} {int(duration_auto)+1} {startoffset_auto}&\n", 'ascii'))                
                                        pass
                                    else:
                                        replayed_time = False
                                        self.lineEdit_7.setEnabled(True)
                                        self.lineEdit_8.setEnabled(True)
                                        self.radioButton_autoplay.setEnabled(True)
                                        replay_started = False
                                        self.timer_started_1 = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                        if self.radioButton_double.isChecked():
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                        if self.radioButton_single.isChecked():
                                            if self.label_Gain_Tx.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                                            if self.label_Gain_Tx_2.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(False)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                                        self.green_light.setVisible(False)
                                        self.pushButton_invisible.setVisible(False)
                                        self.pushButton_pdf.setVisible(False)
                                        self.red_light.setVisible(True)
                                        return
                                    print("File not found — cannot start replay")
                                else:
                                    print("Unexpected result:", result)
                            if HW_USB_in_use:
                                file_command = f"{rtcm_file_path}"
                                self.rtcm_replay_command(file_command, self.autoreplay, start_time_in_sec, duration_in_sec)
                            if comport_is_active:              
                                #print("the command is ",final_string_replay)
                                path_auto = Lg_path
                                filename_auto = f"{real_File_name}.gpio"
                                duration_auto = duration_in_sec
                                startoffset_auto = start_time_in_sec
                                #self.GPIO_record_replay(Lg_path, f"{real_File_name}.gpio", duration_in_sec, start_time_in_sec)
                                #self.GPIO_record_replay(Lg_path, f"{real_File_name}.bin", 120)
                                send_command(bytearray(final_string_replay,'ascii'))
                                self.worker.running = True  # Ensure the thread runs when started
                                self.worker.start()
                                replaying_thread = threading.Thread(target=check_replaying)
                                replaying_thread.start()
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   {final_string_replay}")
                                lines = read_line()
                                #print(lines)
                                decoded_lines = [line.decode('UTF-8') for line in lines]
                            else:
                                replayed_time = False
                                self.lineEdit_7.setEnabled(True)
                                self.lineEdit_8.setEnabled(True)
                                self.radioButton_autoplay.setEnabled(True)
                                replay_started = False
                                self.timer_started_1 = False
                                self.worker.stop()  # Tell the thread to stop
                                self.worker.wait()
                                self.worker.running = False
                                if self.radioButton_gpiomode.isChecked():
                                    self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                if self.radioButton_double.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                if self.radioButton_single.isChecked():
                                    if self.label_Gain_Tx.isChecked():
                                        self.lineEdit_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx_2.setEnabled(True)
                                        self.lineEdit_Gain_Tx_2.setEnabled(False)
                                    if self.label_Gain_Tx_2.isChecked():
                                        self.lineEdit_Gain_Tx.setEnabled(False)
                                        self.label_Gain_Tx.setEnabled(True)
                                        self.label_Gain_Tx_2.setEnabled(True)
                                        self.lineEdit_Gain_Tx_2.setEnabled(True)
                                self.green_light.setVisible(False)
                                self.pushButton_invisible.setVisible(False)
                                self.pushButton_pdf.setVisible(False)
                                self.red_light.setVisible(True)
                                self.stop_GPIO_record_replay()
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not replay")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            for line in decoded_lines:
                                if "Replayed time:" in line:
                                    replayed_time = True
                                if "Destroying" in line:
                                    if not replayed_time:
                                        #print("hiii")
                                        read_Replay_response = False
                                        replayed_time = False
                                        self.lineEdit_7.setEnabled(True)
                                        self.lineEdit_8.setEnabled(True)
                                        self.radioButton_autoplay.setEnabled(True)
                                        replay_started = False
                                        self.timer_started_1 = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                                        if self.radioButton_double.isChecked():
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                            self.lineEdit_Gain_Tx.setEnabled(True)
                                        if self.radioButton_single.isChecked():
                                            if self.label_Gain_Tx.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                                            if self.label_Gain_Tx_2.isChecked():
                                                self.lineEdit_Gain_Tx.setEnabled(False)
                                                self.label_Gain_Tx.setEnabled(True)
                                                self.label_Gain_Tx_2.setEnabled(True)
                                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                                        self.green_light.setVisible(False)
                                        self.pushButton_invisible.setVisible(False)
                                        self.pushButton_pdf.setVisible(False)
                                        self.red_light.setVisible(True)
                                        self.stop_GPIO_record_replay()
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"Error occured! Replay not started!")
                                        msg_box_11.exec()     
                                        return
                            ########################################
                            self.timer_1.start(1000)  # Start the timer with 1 second interval
                            self.timer_started_1 = True
                            replayed_time = False
                            ########################################
            else:
                return
            
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error")
            msg_box_2.setText("You are already Replaying!")
            msg_box_2.exec()
            return
        
    def read_Response_END(self):
        return read_response_end_interface_handle(
            ser,
            interface_in_use,
            file_path_to_read_response,
            get_current_datetime,
        )

    def connectivity_done(self):
        print(self.reference_frequency)
        global ser, bus_no, device_id, usb_button_flag, interface_in_use
        global nvmelabel_lebel_txt, check_comport, SSD_free_space, selected_files_paths, HW_USB_in_use, checked_both_without_HWUSB
        global executable_rx, executable_tx, active_comport_used, active_com_port_used_for_rtcm, comport_connected, ser, submitted, fs_system, submit_btn_clicked, Edit_btn_clicked, nvme_label_found, checked_both, only_ad9361, only_rtcm, ser_rtcm
        if self.comport is None or self.baudrate is None:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Missing Data")
            msg_box_2.setText("Please select required details")
            msg_box_2.exec()
            return
        
        with open(file_path, 'a') as file:
            file.write("\n\n" + " Calling connectivity_done function ".center(50, "*") + "\n\n")
        self.lineEdit_browse_record_rtcm.clear()
        self.lineEdit_replay_rtcm.clear()
        active_comport_used = self.comport
        if self.radioButton_Rx_1.isChecked():
            self.lineEdit_gain_2.setText("")
            self.lineEdit_gain_1.setText(default_gain_rx)
        if self.radioButton_Rx_2.isChecked():
            self.lineEdit_gain_1.setText("")
            self.lineEdit_gain_2.setText(default_gain_rx)
        if self.radioButton_double.isChecked():
            self.lineEdit_gain_2.setText(default_gain_rx)
            self.lineEdit_gain_1.setText(default_gain_rx)
            self.lineEdit_Gain_Tx.setText(default_gain_tx)
            self.lineEdit_Gain_Tx_2.setText(default_gain_tx)
        if self.radioButton_single.isChecked():
            self.lineEdit_Gain_Tx.setText(default_gain_tx)
            self.lineEdit_Gain_Tx_2.setText("")
        if ad9361_checked and not rtcm_checked:
            only_ad9361 = True
            checked_both_without_HWUSB = False
            HW_USB_in_use = False
            only_rtcm = False
        if rtcm_checked and not ad9361_checked:
            only_rtcm = True
            only_ad9361 = False
            checked_both_without_HWUSB = False
            HW_USB_in_use = False
        if ad9361_checked and rtcm_checked:
            information = self.comboBox_comport_rtcm.currentText()
            if information == "HW USB":
                print(information)
                checked_both_without_HWUSB = False
                HW_USB_in_use = True
            else: 
                checked_both_without_HWUSB = True
                HW_USB_in_use = False
            print(checked_both_without_HWUSB)
           
            if self.comport_rtcm is None or self.baudrate_rtcm is None:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Missing Data")
                msg_box_2.setText("Please select required details")
                msg_box_2.exec()
                
                return
            if self.comport == self.comport_rtcm:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Error!")
                msg_box_2.setText("You cannot have same COM Ports!")
                msg_box_2.exec()
                return
            only_ad9361 = False
            only_rtcm = False
            active_com_port_used_for_rtcm = self.comport_rtcm
            print(f"active_com_port_used_for_rtcm: {active_com_port_used_for_rtcm}")
        selected_submit = True
        self.interface_check()
        if selected_submit:
            ##############################################################
            if not self.ensure_interface_connection(timeout_time):
                return
            #####################################################
            if checked_both_without_HWUSB:
                try:
                    ser_rtcm = serial.Serial(self.comport_rtcm, self.baudrate_rtcm, timeout=timeout_time)
                except serial.SerialException as e:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error!")
                    msg_box_2.setText(f"You cannot open the {self.comport_rtcm}!")
                    msg_box_2.exec()
                    self.ensure_interface_disconnection()
                    return
            

            if HW_USB_in_use:
                if not usb_button_flag:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Attention!")
                    msg_box_2.setText(f"Please verify the HW USB info by clicking on the HW USB info btn!")
                    msg_box_2.exec()
                    self.ensure_interface_disconnection()
                    return
                device_id = self.lineEdit_deviceid.text().strip()
                bus_no = self.lineEdit_busno.text().strip()
                print(device_id)
                print(bus_no)
                if device_id == "" and bus_no == "":
                    pass
                else:
                    try:
                        device_id = int(device_id)
                        bus_no = int(bus_no)
                        matched = False
                        for line in newoutput:
                            if "Bus" in line and "Device" in line:
                                # split and extract bus/device
                                parts = line.split(":")[0].split()
                                bus = int(parts[1])
                                device = int(parts[3])  # "Device" comes before the number

                                # check match
                                if bus == bus_no and device == device_id:
                                    print(f"✅ Match found: {line}")
                                    matched = True
                                    break
                        if not matched:
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Error!")
                            msg_box_2.setText(f"No matching Bus and Device found in the USB info!")
                            msg_box_2.exec()
                            self.ensure_interface_disconnection()
                            return
                    except:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Error!")
                        msg_box_2.setText(f"Device ID and bus number should be an integer!")
                        msg_box_2.exec()
                        self.ensure_interface_disconnection()
                        return
                print(device_id)
                print(bus_no)
            ######################################################
            #send_command(bytearray(f'cd /home/root/\n', 'ascii'))
            send_command(b'\x03')
            with open(file_path, 'a') as file:
                file.write(f'\n{get_current_datetime()}   b"\\x03"\n')
            #send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/command_set01.sh\n', 'ascii'))
            comport_is_active = interface_is_online(self.comport)
            if comport_is_active: 
                send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/command_set01.sh ; /home/root/adc4bits/libiio/command_set01.sh ; (echo END) > /dev/null\n', 'ascii'))
                if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/command_set01.sh ; /home/root/adc4bits/libiio/command_set01.sh ; (echo END) > /dev/null\n')
                lines = self.read_Response_END()
                print(lines) 
                try:
                    decoded_lines = [line.decode() for line in lines]
                except:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Could not decode the response from the device!\nPlease check the connection and try again.")
                    msg_box_11.exec()
                    self.ensure_interface_disconnection()
                    return
                #for line in decoded_lines:
                if "No such" in decoded_lines[-3]:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"adc4bits folder not found in the current directory!\nPlease place the adc4bits folder and libiio folder inside adc4bits folder.\n")
                        msg_box_11.exec()
                        self.ensure_interface_disconnection()
                        return
                       
                if Commands_file_user:
                            with open(file_path_to_read_response, 'a') as file:
                                file.write(f'{get_current_datetime()} :Response after checking the file directory')
                                file.write(f'\n{get_current_datetime()}   {lines}\n\n')
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Comport got disconnected")
                msg_box_11.exec()
                #self.open_after_disconnection()
                return  
            libiio_folder_found = False
            for line in decoded_lines:
                if "fs_system value:" in line:
                    fs_system = line.split(":")[-1].strip().replace("'","")
                elif "✅ Available space" in line:
                    SSD_free_space = float(line.split(":")[-1].strip().split(" ")[0])
                    if HW_USB_in_use:
                        SSD_free_space = SSD_free_space - HW_USB_Size
                elif "libiio folder found" in line:
                    libiio_folder_found = True
            
            self.variable_names = []
            selected_files_paths = []
            start_marker = "Final contents of selected_files.txt:"
            stop_marker = "Script execution time:"
            start_printing = False

            for line in decoded_lines:
                if start_marker in line:
                    start_printing = True
                elif stop_marker in line:
                    break
                if start_printing:
                    if "selected_files:" in line:
                        valid_file_name_initial = line.split(":")[-1].strip()
                        valid_file_name = (valid_file_name_initial.split("/")[-1].strip())
                        selected_files_paths.append(valid_file_name_initial)
                        self.variable_names.append(valid_file_name)

            if not libiio_folder_found:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Please note!")
                msg_box_11.setText(f"Libiio folder not found in the current directory \"/home/root/adc4bits/\"!\nPlease place the libiio folder else recorded files will not be stored\n")
                msg_box_11.exec()

            
            if not fs_system == "/dev/":
                Edit_btn_clicked = True
                self.lineEdit_fs_system.setText(fs_system)
                self.fs_system_submit_btn.setVisible(False)
                #self.fs_system_edit_btn.setVisible(True)
                self.lineEdit_fs_system.setEnabled(False)
                self.lineEdit_fs_system.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #4A6375;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
            else:
                submit_btn_clicked = True
                #self.fs_system_submit_btn.setVisible(True)
                self.fs_system_edit_btn.setVisible(False)
                self.lineEdit_fs_system.setEnabled(True)
                self.lineEdit_fs_system.setStyleSheet("""
                                                QLineEdit {
                                                    background-color: #2C3E50;
                                                    color: #FFFFFF;
                                                    border: 2px solid #1ABC9C;
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QLineEdit:focus {
                                                    border: 2px solid #2E5;
                                                }
                                            """)
            comport_connected = True
            submitted = True
            if self.radioButton_single.isChecked():
                self.lineEdit_bandwidth_2.clear()
                self.lineEdit_gain_2.clear()
                self.lineEdit_samplingfreq_2.clear()
                self.lineEdit_4.clear()
                self.comboBox_2.setCurrentIndex(0)
            self.lineEdit_fs_system.setText(fs_system)
            #################################################################################################################################################
            self.frame.setVisible(True)
            self.lineEdit9.clear()
            self.lineEdit9.setPlaceholderText("Please select the file")
            self.label_SSD_capacity.setVisible(False)
            self.label_available_Duration.setVisible(False)
            self.radioButton_double.setVisible(False)
            self.radioButton_single.setVisible(False)
            self.label_radio.setVisible(False)
            self.lineEdit_hostname.setVisible(False)
            self.lineEdit_password.setVisible(False)
            self.label_ssid.setVisible(False)
            self.label_hostname.setVisible(False)
            self.label_gpiomode.setVisible(False)
            self.radioButton_gpiomode.setVisible(False)
            self.radioButton_rfmdmode.setVisible(False)
            # Define label_connected as an instance attribute
            self.label_connected_rtcm = QtWidgets.QLabel(self.frame)
            self.label_connected_rtcm.setGeometry(QtCore.QRect(135, 135, 500, 50))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.label_connected_rtcm.setFont(font)
            self.label_connected_rtcm.setObjectName("label_connected")
            self.label_connected_rtcm.setText(f"Connected to {self.comport_rtcm} with a Baudrate {self.baudrate_rtcm} for RTCM")
            # Set text color to green
            #self.label_connected.setStyleSheet("color: green;")
            # Make sure the label is visible
            self.label_connected_rtcm.setVisible(True)
            self.label_connected_rtcm.update()

            self.label_connected = QtWidgets.QLabel(self.frame)
            self.label_connected.setGeometry(QtCore.QRect(135, 180, 500, 50))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.label_connected.setFont(font)
            self.label_connected.setObjectName("label_connected")
            self.label_connected.setText(f"Connected to {self.comport} with a Baudrate {self.baudrate} for AD9361")
            # Set text color to green
            #self.label_connected.setStyleSheet("color: green;")
            # Make sure the label is visible
            self.label_connected.setVisible(True)
            self.label_connected.update()
            ##################################################################################################
            self.button_reboot = QtWidgets.QPushButton(self.frame)
            self.button_reboot.setGeometry(QtCore.QRect(250, 250, 81, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.button_reboot.setFont(font) 
            self.button_reboot.setText("Reboot")
            self.button_reboot.setStyleSheet("QPushButton{"
                                         "background-color:#1ABC9C;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #3A7;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #2E5;"  # Change color when pressed if desired
                                         "}"
                                         )
            self.button_shutdown = QtWidgets.QPushButton(self.frame)
            self.button_shutdown.setGeometry(QtCore.QRect(350, 250, 95, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.button_shutdown.setFont(font) 
            self.button_shutdown.setText("Shut down")
            self.button_shutdown.setStyleSheet("QPushButton{"
                                         "background-color:#1ABC9C;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #3A7;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #2E5;"  # Change color when pressed if desired
                                         "}"
                                         )
            #Create Reconnect button
            self.button_reconnect = QtWidgets.QPushButton(self.frame)
            self.button_reconnect.setGeometry(QtCore.QRect(300, 305, 100, 31))
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            self.button_reconnect.setFont(font) 
            self.button_reconnect.setText("Disconnect")
            self.button_reconnect.setStyleSheet("QPushButton{"
                                         "background-color:red;"
                                         "color:white;"
                                         "border-radius:15;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: black;"  # Change color on hover if desired
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: gray;"  # Change color when pressed if desired
                                         "}"
                                         )
            self.button_reconnect.setVisible(True)
            self.button_reboot.setVisible(True)
            self.button_shutdown.setVisible(True)
            if (checked_both_without_HWUSB or HW_USB_in_use):
                self.label_connected_rtcm.setVisible(True)
            else:
                self.label_connected_rtcm.setVisible(False)
            self.button_reconnect.clicked.connect(self.reconnect)
            self.button_reboot.clicked.connect(self.reboot)
            self.button_shutdown.clicked.connect(self.shutdown)
            ##############################################################################################################
            self.label_connectivity.setVisible(False)
            self.pushButton_submit.setVisible(False)
            self.comboBox_baudrate.setVisible(False)
            self.comboBox_comport.setVisible(False)
            self.label_ref_freq.setVisible(False)
            self.comboBox_ref_freq.setVisible(False)
            self.comboBox_baudrate_rtcm.setVisible(False)
            self.radioButton_ad9361.setVisible(False)
            self.radioButton_rtcm.setVisible(False)
            self.lineEdit_deviceid.setVisible(False)
            self.label_deviceid.setVisible(False)
            self.lineEdit_busno.setVisible(False)
            self.label_busno.setVisible(False)
            self.pushButton_usb_info.setVisible(False)
            self.comboBox_comport_rtcm.setVisible(False)
            self.pushButton_4.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.radioButton_Rx_1.setVisible(False)
            self.radioButton_Rx_2.setVisible(False)
            if self.radioButton_rfmdmode.isChecked():
                print("RFMD mode selected")
                comport_is_active = interface_is_online(self.comport)
                if comport_is_active:
                    send_command(bytearray("devmem 0xB0000000 w 8\n",'ascii'))
                    send_command(bytearray("/home/root/adc4bits/libiio/build/utils/iio_reg ad9361-phy 0x0A 0x10\n",'ascii'))
                    with open(file_path, 'a') as file:
                        file.write(f"{get_current_datetime()}   devmem 0xB0000000 w 8\n")
                        file.write(f"{get_current_datetime()}   /home/root/adc4bits/libiio/build/utils/iio_reg ad9361-phy 0x0A 0x10\n")
            else:
                print("RFMD mode not selected")
                comport_is_active = interface_is_online(self.comport)
                if comport_is_active:
                    send_command(bytearray("devmem 0xB0000000 w 0\n",'ascii'))
                    send_command(bytearray("/home/root/adc4bits/libiio/build/utils/iio_reg ad9361-phy 0x0A 0xa\n",'ascii'))
                    with open(file_path, 'a') as file:
                        file.write(f"{get_current_datetime()}   devmem 0xB0000000 w 0\n")
                        file.write(f"{get_current_datetime()}   /home/root/adc4bits/libiio/build/utils/iio_reg ad9361-phy 0x0A 0xa\n")
            with open(file_path, 'a') as file:
                file.write("\n\n" + "closing connectivity_done function".center(50, "-") + "\n\n")

            
        check_comport = False
    ##############################################################################################
    def shutdown(self):
        global comport_connected, ser, gui_opened, root_gui, boot
        if gui_opened:
            return      
        msg_box_3 = QMessageBox()
        msg_box_3.setWindowTitle("Confirmation")
        msg_box_3.setText("Are you sure you want to shutdown?")
        msg_box_3.setIcon(QMessageBox.Icon.Question)
        msg_box_3.addButton(QMessageBox.StandardButton.Yes)
        msg_box_3.addButton(QMessageBox.StandardButton.No)
        msg_box_3.setDefaultButton(QMessageBox.StandardButton.No) 
        # Execute the message box
        selected_reboot = msg_box_3.exec()
        if selected_reboot == QMessageBox.StandardButton.Yes:
            comport_is_active = interface_is_online(self.comport)
            if comport_is_active: 
                send_command(bytearray(shutdown_command,'ascii'))   
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f"\n{get_current_datetime()}   {shutdown_command}") 
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"COM port got disconnected!, could not shutdown!")
                msg_box_11.exec()
                self.open_after_disconnection()
                return
            ########################################################################################
            gui_opened = True
            boot = True
            import tkinter as tk
            def countdown(count):
                if count > 0:
                    label_timer.config(text=f"{count} s")
                    root_gui.after(1000, countdown, count - 1)  # Update every second
                else:
                    root_gui.destroy()  # Close the GUI when countdown reaches 0

            # Create the main window
            root_gui = tk.Tk()
            root_gui.title("Shutting down")
            root_gui.geometry("300x150")
            root_gui.attributes("-toolwindow", 1)
            root_gui.attributes("-fullscreen", 0)
            # Remove window decorations (minimize, maximize, close buttons)

            # Create a label for "Rebooting" text
            label_rebooting = tk.Label(root_gui, text="Shutting down...", font=("Helvetica", 16, "bold"))
            label_rebooting.pack(pady=20)

            # Create a label for countdown timer
            label_timer = tk.Label(root_gui, text="", font=("Helvetica", 14))
            label_timer.pack()
            root_gui.protocol("WM_DELETE_WINDOW", lambda: None)
            # Start countdown from 30 seconds
            countdown(10)
            # Run the Tkinter event loop
            root_gui.mainloop()
            gui_opened = False
            self.open_after_disconnection()
            ##################################################################################################
    ###############################################################################################
    def reboot(self):
        global comport_connected, ser, gui_opened, root_gui, boot
        if gui_opened:
            return
        
        msg_box_3 = QMessageBox()
        msg_box_3.setWindowTitle("Confirmation")
        msg_box_3.setText("Are you sure you want to reboot?")
        msg_box_3.setIcon(QMessageBox.Icon.Question)
        msg_box_3.addButton(QMessageBox.StandardButton.Yes)
        msg_box_3.addButton(QMessageBox.StandardButton.No)
        msg_box_3.setDefaultButton(QMessageBox.StandardButton.No) 
        # Execute the message box
        selected_reboot = msg_box_3.exec()
        if selected_reboot == QMessageBox.StandardButton.Yes:
            comport_is_active = interface_is_online(self.comport)
            if comport_is_active: 
                send_command(bytearray(reboot_command,'ascii'))   
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f"\n{get_current_datetime()}   {reboot_command}")
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"COM port got disconnected!, could not reboot the system!")
                msg_box_11.exec()
                self.open_after_disconnection()
                return
            ########################################################################################
            gui_opened = True
            boot = True
            import tkinter as tk
            def countdown(count):
                if count > 0:
                    label_timer.config(text=f"{count} s")
                    root_gui.after(1000, countdown, count - 1)  # Update every second
                else:                 
                    root_gui.destroy()  # Close the GUI when countdown reaches 0
                    
            # Create the main window
            root_gui = tk.Tk()
            root_gui.title("Rebooting")
            root_gui.geometry("300x150")
            root_gui.attributes("-toolwindow", 1)
            root_gui.attributes("-fullscreen", 0)
            # Remove window decorations (minimize, maximize, close buttons)

            # Create a label for "Rebooting" text
            label_rebooting = tk.Label(root_gui, text="Rebooting...", font=("Helvetica", 16, "bold"))
            label_rebooting.pack(pady=20)

            # Create a label for countdown timer
            label_timer = tk.Label(root_gui, text="", font=("Helvetica", 14))
            label_timer.pack()
            root_gui.protocol("WM_DELETE_WINDOW", lambda: None)
            # Start countdown from 30 seconds
            countdown(30)
            # Run the Tkinter event loop
            root_gui.mainloop()
            gui_opened = False
            ##################################################################################################
    ######################################################################################################
        
    def reconnect(self):
        if gui_opened:
            return
        global comport_connected,ser, submitted, ser_rtcm, check_comport
        msg_box_3 = QMessageBox()
        msg_box_3.setWindowTitle("Confirmation")
        msg_box_3.setText("Are you sure you want to Disconnect?")
        msg_box_3.setIcon(QMessageBox.Icon.Question)
        msg_box_3.addButton(QMessageBox.StandardButton.Yes)
        msg_box_3.addButton(QMessageBox.StandardButton.No)
        msg_box_3.setDefaultButton(QMessageBox.StandardButton.No) 
        selected_reconnect = msg_box_3.exec()
        if selected_reconnect == QMessageBox.StandardButton.Yes:
            #self.check_comport_Regularly()
            self.update_com_ports()
            self.update_com_ports_rtcm()
            comport_is_active = interface_is_online(self.comport)
            if comport_is_active: 
                send_command(bytearray(f'nice --20 /home/root/adc4bits/libiio/build/examples/switches\n', 'ascii'))
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f'nice --20 /home/root/adc4bits/libiio/build/examples/switches\n')
            comport_connected = False
            if ser.isOpen():
                self.ensure_interface_disconnection()
                print("closed!")
            if checked_both_without_HWUSB:
                if ser_rtcm.isOpen():
                    ser_rtcm.close()
            submitted = False
            print(executable_rx)
            print(executable_tx)
            check_comport = True
            #self.green_satellite.setVisible(False)
            self.radioButton_double.setVisible(True)
            self.radioButton_single.setVisible(True)
            self.label_radio.setVisible(True)
            item = self.comboBox_comport.currentText()
            if item == WIFI_INTERFACE_OPTION:
                self.lineEdit_hostname.setVisible(True)
                self.label_ssid.setVisible(True)
                self.lineEdit_password.setVisible(False)
                self.label_hostname.setVisible(True)
            else:
                self.lineEdit_hostname.setVisible(False)
                self.label_ssid.setVisible(False)
                self.lineEdit_password.setVisible(False)
                self.label_hostname.setVisible(False)
            self.label_gpiomode.setVisible(False)
            self.radioButton_gpiomode.setVisible(False)
            self.radioButton_rfmdmode.setVisible(False)
            self.pushButton_submit.setVisible(True)
            self.comboBox_baudrate.setVisible(True)
            self.comboBox_comport.setVisible(True)
            self.label_ref_freq.setVisible(False)
            self.comboBox_ref_freq.setVisible(False)
            self.comboBox_baudrate_rtcm.setVisible(True)
            self.radioButton_ad9361.setVisible(True)
            self.radioButton_rtcm.setVisible(True)
            if self.comboBox_comport_rtcm.currentText() == "HW USB":
                self.lineEdit_deviceid.setVisible(True)
                self.label_deviceid.setVisible(True)
                self.lineEdit_busno.setVisible(True)
                self.label_busno.setVisible(True)
                self.pushButton_usb_info.setVisible(True)
            else:
                self.lineEdit_deviceid.setVisible(False)
                self.label_deviceid.setVisible(False)
                self.lineEdit_busno.setVisible(False)
                self.label_busno.setVisible(False)
                self.pushButton_usb_info.setVisible(False)
            self.comboBox_comport_rtcm.setVisible(True)
            self.pushButton_5.setEnabled(True)
            self.label_connectivity.setVisible(True)
            self.button_reconnect.setVisible(False)
            self.button_shutdown.setVisible(False)
            self.button_reboot.setVisible(False)
            self.label_connected.setVisible(False)
            self.label_connected_rtcm.setVisible(False)
            self.pushButton_login.setEnabled(False)
            """self.get_comport()
            self.get_comport_rtcm()
            if self.comport_rtcm == "":
                self.comboBox_comport_rtcm.addItem("Select Port") 
            if self.comport == "":
                self.comboBox_comport.addItem("Select Port")"""
            
    def stop_timer_replay(self):
        global replay_started, count_one_replay, read_Replay_response, replay_terminated, count_seconds
        if replay_started:
            if not replay_terminated:
                msg_box_stop_replay = QMessageBox()
                msg_box_stop_replay.setWindowTitle("Confirmation")
                msg_box_stop_replay.setText("Do you want to stop the Replay?")
                msg_box_stop_replay.setIcon(QMessageBox.Icon.Question)
                msg_box_stop_replay.addButton(QMessageBox.StandardButton.Yes)
                msg_box_stop_replay.addButton(QMessageBox.StandardButton.No)
                msg_box_stop_replay.setDefaultButton(QMessageBox.StandardButton.No) 
                # Execute the message box
                reply = msg_box_stop_replay.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    print("\n\n\n\n\n\n\n\n\n\nyes\n\n\n\n\n\n\n\n")
                    if self.timer_started_1:
                        print("\n\n\n\n\n\n\n\n\n\nyes1\n\n\n\n\n\n\n\n")
                        self.timer_1.stop()
                        if checked_both_without_HWUSB or HW_USB_in_use:
                            if (HW_USB_in_use):
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active: 
                                    send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                            else:
                                self.stop_sending()
                           
                        read_Replay_response = False
                        time.sleep(1)
                        count_one_replay = 0
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(b'\x03')
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   \x03')
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                       
                        self.lineEdit_7.setEnabled(True)
                        self.lineEdit_8.setEnabled(True)
                        self.radioButton_autoplay.setEnabled(True)
                        self.green_light.setVisible(False)
                        self.pushButton_invisible.setVisible(False)
                        self.pushButton_pdf.setVisible(False)
                        self.red_light.setVisible(True)
                        self.stop_GPIO_record_replay()
                        count_seconds = 0
                        #self.lineEdit_replay.setStyleSheet("background-color: white;")
                        self.timer_started_1 = False
                        replay_started = False
                        read_Replay_response = False
                        self.timer_started_1 = False
                        self.worker.stop()  # Tell the thread to stop
                        self.worker.wait()
                        self.worker.running = False
                        if self.radioButton_gpiomode.isChecked():
                            self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                        if self.radioButton_double.isChecked():
                            self.lineEdit_Gain_Tx.setEnabled(True)
                            self.lineEdit_Gain_Tx_2.setEnabled(True)
                        if self.radioButton_single.isChecked():
                            if self.label_Gain_Tx.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                            if self.label_Gain_Tx_2.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(False)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                        self.update_time_1()
                        
                        #send_command(bytearray("kill -SIGINT $(ps -uax | grep ad9361-ii | awk -F' ' '{ print $2 }')\n",'ascii'))
                        #self.ensure_interface_disconnection()
        else:
            msg_box_9 = QMessageBox()
            msg_box_9.setWindowTitle("Error!")
            msg_box_9.setText("Replay is not yet started!")
            msg_box_9.exec()

    def update_time_1(self):
        global ser, replayed_time, replay_started, disconnected_comport_while_recording_replaying, read_Replay_response, count_seconds
        if replay_terminated:
                self.timer_1.stop()
                self.lineEdit_replay.clear()
                replayed_time = False
                read_Replay_response = False
                self.lineEdit_7.setEnabled(True)
                self.lineEdit_8.setEnabled(True)
                self.radioButton_autoplay.setEnabled(True)
                replay_started = False
                read_Replay_response = False
                self.timer_started_1 = False
                self.worker.stop()  # Tell the thread to stop
                self.worker.wait()
                self.worker.running = False
                if self.radioButton_gpiomode.isChecked():
                    self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                if self.radioButton_double.isChecked():
                            self.lineEdit_Gain_Tx.setEnabled(True)
                            self.lineEdit_Gain_Tx.setEnabled(True)
                if self.radioButton_single.isChecked():
                            if self.label_Gain_Tx.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                            if self.label_Gain_Tx_2.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(False)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                #disconnected_comport_while_recording_replaying = False
                self.green_light.setVisible(False)
                self.pushButton_invisible.setVisible(False)
                self.pushButton_pdf.setVisible(False)
                self.red_light.setVisible(True)
                self.stop_GPIO_record_replay()
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if (HW_USB_in_use):
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_sending()
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Terminated!")
                msg_box_11.setText(f"Replay got terminated!")
                msg_box_11.exec()
                #self.open_after_disconnection()
                return
        #########################################################################################################################
        #########################################################################################################################
        if not replay_terminated:
            if disconnected_comport_while_recording_replaying:
                replayed_time = False
                read_Replay_response = False
                self.timer_1.stop()
                self.lineEdit_replay.clear()
                self.lineEdit_7.setEnabled(True)
                self.lineEdit_8.setEnabled(True)
                self.radioButton_autoplay.setEnabled(True)
                replay_started = False
                self.timer_started_1 = False
                self.worker.stop()  # Tell the thread to stop
                self.worker.wait()
                self.worker.running = False
                if self.radioButton_gpiomode.isChecked():
                    self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                if self.radioButton_double.isChecked():
                            self.lineEdit_Gain_Tx.setEnabled(True)
                            self.lineEdit_Gain_Tx_2.setEnabled(True)
                if self.radioButton_single.isChecked():
                            if self.label_Gain_Tx.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(False)
                            if self.label_Gain_Tx_2.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(False)
                                self.label_Gain_Tx.setEnabled(True)
                                self.label_Gain_Tx_2.setEnabled(True)
                                self.lineEdit_Gain_Tx_2.setEnabled(True)
                #disconnected_comport_while_recording_replaying = False
                self.green_light.setVisible(False)
                self.pushButton_invisible.setVisible(False)
                self.pushButton_pdf.setVisible(False)
                self.red_light.setVisible(True)
                self.stop_GPIO_record_replay()
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if (HW_USB_in_use):
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_sending()
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Com port got disconnected, Replaying stopped\nPlease reconnect!")
                msg_box_11.exec()
                self.open_after_disconnection()
                return

            #self.lineEdit_replay.setStyleSheet("background-color: white;")
            global  count_one_replay, count_seconds
            result = add_two_times(start_time_valid, stop_time_valid)
            if self.timer_started_1:
                count_one_replay += 1
                count_seconds += 1
                print(f"Count seconds: {count_seconds}")
                current_time = self.elapsed_time.toString("HH:mm:ss")
                if stop_time_valid is not None:
                    if result < str(log_duration):
                        if current_time >= result and self.autoreplay == 0:
                            self.timer_1.stop()
                            read_Replay_response = False
                            if checked_both_without_HWUSB or HW_USB_in_use:
                                if (HW_USB_in_use):
                                    comport_is_active = interface_is_online(self.comport)
                                    if comport_is_active: 
                                        send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                                else:
                                    self.stop_sending()
                            count_one_replay = 0
                            
                            self.lineEdit_7.setEnabled(True)
                            self.lineEdit_8.setEnabled(True)
                            self.radioButton_autoplay.setEnabled(True)
                            #self.lineEdit_replay.setStyleSheet("background-color: white;")
                            replay_started = False
                            count_seconds = 0
                            self.worker.stop()  # Tell the thread to stop
                            self.worker.wait()
                            self.timer_started_1 = False
                            self.worker.running = False
                            read_Replay_response = False
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                            if self.radioButton_double.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(True)
                                self.lineEdit_Gain_Tx.setEnabled(True)
                            if self.radioButton_single.isChecked():
                                if self.label_Gain_Tx.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx_2.setEnabled(True)
                                    self.lineEdit_Gain_Tx_2.setEnabled(False)
                                if self.label_Gain_Tx_2.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(False)
                                    self.label_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx_2.setEnabled(True)
                                    self.lineEdit_Gain_Tx_2.setEnabled(True)
                            self.timer_started_1 = False
                            self.green_light.setVisible(False)
                            self.pushButton_invisible.setVisible(False)
                            self.pushButton_pdf.setVisible(False)
                            self.red_light.setVisible(True)
                            self.stop_GPIO_record_replay()
                            return
                    else:
                        if current_time >= str(log_duration) and self.autoreplay == 0:
                            self.timer_1.stop()
                            read_Replay_response = False
                            if checked_both_without_HWUSB or HW_USB_in_use:
                                if (HW_USB_in_use):
                                    comport_is_active = interface_is_online(self.comport)
                                    if comport_is_active: 
                                        send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                                else:
                                    self.stop_sending()
                            count_one_replay = 0
                            count_seconds = 0
                            self.lineEdit_7.setEnabled(True)
                            self.lineEdit_8.setEnabled(True)
                            self.radioButton_autoplay.setEnabled(True)
                            self.green_light.setVisible(False)
                            self.pushButton_invisible.setVisible(False)
                            self.pushButton_pdf.setVisible(False)
                            self.red_light.setVisible(True)
                            self.timer_started_1 = False
                            #self.lineEdit_replay.setStyleSheet("background-color: white;")
                            replay_started = False
                            self.timer_started_1 = False
                            read_Replay_response = False
                            self.worker.stop()  # Tell the thread to stop
                            self.worker.wait()
                            self.worker.running = False
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Replay.setEnabled(True) and self.radioButton_GPIO_Record.setEnabled(True)
                            if self.radioButton_double.isChecked():
                                self.lineEdit_Gain_Tx.setEnabled(True)
                                self.lineEdit_Gain_Tx.setEnabled(True)
                            if self.radioButton_single.isChecked():
                                if self.label_Gain_Tx.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx_2.setEnabled(True)
                                    self.lineEdit_Gain_Tx_2.setEnabled(False)
                                if self.label_Gain_Tx_2.isChecked():
                                    self.lineEdit_Gain_Tx.setEnabled(False)
                                    self.label_Gain_Tx.setEnabled(True)
                                    self.label_Gain_Tx_2.setEnabled(True)
                                    self.lineEdit_Gain_Tx_2.setEnabled(True)
                            return
                
                if self.autoreplay == 1:
                    if checked_both_without_HWUSB:
                        print(second_to_hhmmss(count_seconds))
                        print(stop_time_valid)
                        if str(second_to_hhmmss(count_seconds)) == stop_time_valid:
                            count_seconds = 0
                            self.stop_sending() 
                            time.sleep(0.5)
                            print("restarting autoreplay")
                            #self.stop_GPIO_record_replay()
                            self.is_sending = True
                            threading.Thread(target=self.send_data, daemon=True).start()
                            self.GPIO_record_replay(path_auto, filename_auto, duration_auto, startoffset_auto, 1)
                    else:
                        if str(second_to_hhmmss(count_seconds)) == stop_time_valid:
                            count_seconds = 0
                            self.GPIO_record_replay(path_auto, filename_auto, duration_auto, startoffset_auto, 1)

                if count_one_replay == 1:
                    if checked_both_without_HWUSB:
                        self.is_sending = True
                        threading.Thread(target=self.send_data, daemon=True).start()

                self.elapsed_time = self.elapsed_time.addSecs(1)
                self.lineEdit_replay.setText(self.elapsed_time.toString("HH:mm:ss"))
                #self.lineEdit_replay.setStyleSheet("color: black; font-weight: bold;")

###############################################################################################################################################################################
    def browse_folder_Record_rtcm(self):
        global browse_folder_for_HWUSB
        global browse_file_for_HWUSB
        try:
            if self.radioButton_rtcm.isChecked():
                global browse_file_for_HWUSB
                global rtcm_folder_name, rtcm_folder_path, rtcm_file_name, rtcm_file_path, browse_folder_for_HWUSB
                if record_tab:
                    if not recording_started:
                        svg_renderer = QSvgRenderer("selected_file.svg")  # Replace with your SVG image path
                        # Create a QPixmap and render the SVG onto it
                        pixmap = QPixmap(45, 45)  # Set the size of the icon
                        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                        # Use QPainter to render the SVG on the QPixmap
                        painter = QPainter(pixmap)
                        svg_renderer.render(painter)
                        painter.end()
                        # Set the rendered SVG as the icon for the QPushButton
                        icon = QIcon(pixmap)
                        self.pushButton_browse_record_rtcm.setIcon(icon)
                        self.pushButton_browse_record_rtcm.setIconSize(QSize(30, 30))  # Set icon size
                        #self.pushButton_browse_record_rtcm.setText("Browse..")
                        if HW_USB_in_use:
                            browse_folder_for_HWUSB = True
                            self.browse_folder_Record()
                            try:
                                folder = folder_HW_USB
                            except:
                                folder = None
                            
                        else:
                            folder = QFileDialog.getExistingDirectory(None, "Select Folder")
                        if folder:
                            if folder == None:
                                return
                            print(folder)
                            rtcm_folder_path = folder
                            if not (browse_folder_for_HWUSB):
                                folder_name = os.path.basename(folder)
                            else:
                                folder_name = rtcm_folder_path.strip().split("/")[-2]
                            rtcm_folder_name = folder_name
                            self.lineEdit_browse_record_rtcm.setText(rtcm_folder_name)
                            browse_folder_for_HWUSB = False
                            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                            # Create a QPixmap and render the SVG onto it
                            pixmap = QPixmap(45, 45)  # Set the size of the icon
                            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                            # Use QPainter to render the SVG on the QPixmap
                            painter = QPainter(pixmap)
                            svg_renderer.render(painter)
                            painter.end()
                            # Set the rendered SVG as the icon for the QPushButton
                            icon = QIcon(pixmap)
                            self.pushButton_browse_record_rtcm.setIcon(icon)
                            self.pushButton_browse_record_rtcm.setIconSize(QSize(30, 30)) 
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Info!")
                        msg_box_11.setText(f"Recording is ON!")
                        msg_box_11.exec()
                        return
                if replay_tab:
                    if not replay_started:
                        # Load the SVG file using QSvgRenderer
                        svg_renderer = QSvgRenderer("selected_file.svg")  # Replace with your SVG image path
                        # Create a QPixmap and render the SVG onto it
                        pixmap = QPixmap(45, 45)  # Set the size of the icon
                        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                        # Use QPainter to render the SVG on the QPixmap
                        painter = QPainter(pixmap)
                        svg_renderer.render(painter)
                        painter.end()
                        # Set the rendered SVG as the icon for the QPushButton
                        icon = QIcon(pixmap)
                        self.pushButton_browse_replay_rtcm.setIcon(icon)
                        self.pushButton_browse_replay_rtcm.setIconSize(QSize(30, 30))  # Set icon size
                        if HW_USB_in_use:
                            browse_file_for_HWUSB = True
                            self.browse_file()
                            try:
                                file = HW_file_path
                            except:
                                file = None
                        else:
                            file, _ = QFileDialog.getOpenFileName(None, "Select File", "", "Text Files (*.rtcm)")
                        if file:
                            if file == None:
                                return
                            file_path = file
                            rtcm_file_path = file_path
                            if not browse_file_for_HWUSB:
                                file_name = os.path.basename(file)
                            else:
                                file_name = rtcm_file_path.strip().split("/")[-2]
                            rtcm_file_name = file_name.split(".rtcm")[0]
                            self.lineEdit_replay_rtcm.setText(rtcm_file_name)
                            browse_file_for_HWUSB = False
                            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                            # Create a QPixmap and render the SVG onto it
                            pixmap = QPixmap(45, 45)  # Set the size of the icon
                            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                            # Use QPainter to render the SVG on the QPixmap
                            painter = QPainter(pixmap)
                            svg_renderer.render(painter)
                            painter.end()
                            # Set the rendered SVG as the icon for the QPushButton
                            icon = QIcon(pixmap)
                            self.pushButton_browse_record_rtcm.setIcon(icon)
                            self.pushButton_browse_record_rtcm.setIconSize(QSize(30, 30)) 
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Info!")
                        msg_box_11.setText(f"Replaying is ON!")
                        msg_box_11.exec()
                        return
        except PermissionError as e:
            print("you cannot select this folder")
        finally:
            if record_tab:
                svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                # Create a QPixmap and render the SVG onto it
                pixmap = QPixmap(45, 45)  # Set the size of the icon
                pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                # Use QPainter to render the SVG on the QPixmap
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
                # Set the rendered SVG as the icon for the QPushButton
                icon = QIcon(pixmap)
                self.pushButton_browse_record_rtcm.setIcon(icon)
                self.pushButton_browse_record_rtcm.setIconSize(QSize(30, 30))  # Set icon size
                #self.pushButton_browse_record_rtcm.setText("Browse..")
                print("terminated")

            if replay_tab:
                svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                # Create a QPixmap and render the SVG onto it
                pixmap = QPixmap(45, 45)  # Set the size of the icon
                pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                # Use QPainter to render the SVG on the QPixmap
                painter = QPainter(pixmap)
                svg_renderer.render(painter)
                painter.end()
                # Set the rendered SVG as the icon for the QPushButton
                icon = QIcon(pixmap)
                self.pushButton_browse_replay_rtcm.setIcon(icon)
                self.pushButton_browse_replay_rtcm.setIconSize(QSize(30, 30))  # Set icon size
                #self.pushButton_browse_record_rtcm.setText("Browse..")
                print("terminated")
            

    def browse_folder_Record(self):
        global folder_HW_USB
        def on_secondary_close():
            global root, browse_folder
            browse_folder = False
            # Load the SVG file using QSvgRenderer
            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
            # Create a QPixmap and render the SVG onto it
            pixmap = QPixmap(45, 45)  # Set the size of the icon
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
            # Use QPainter to render the SVG on the QPixmap
            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
            # Set the rendered SVG as the icon for the QPushButton
            icon = QIcon(pixmap)
            self.pushButton_browse_record.setIcon(icon)
            self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
            self.pushButton.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_login.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_select_file.setEnabled(True)
            print("terminated")
            if root_create_popup:
                root_create.destroy()
            root.destroy()
            
        global root, browse_folder
        if not recording_started:
            if not browse_folder:
                #####################################################################
                import sys
                from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
                from PyQt6.QtSvg import QSvgRenderer
                from PyQt6.QtGui import QPixmap, QIcon, QPainter
                from PyQt6.QtCore import QSize, Qt
                self.pushButton.setEnabled(False)
                self.pushButton_3.setEnabled(False)
                if not (browse_folder_for_HWUSB):
                    svg_renderer = QSvgRenderer("selected_file.svg")
                    pixmap = QPixmap(45, 45)  # Adjust size for icon as needed
                    pixmap.fill(Qt.GlobalColor.transparent)  # Set pixmap transparency
                    painter = QPainter(pixmap)
                    svg_renderer.render(painter)
                    painter.end()
                    self.pushButton_browse_record.setIcon(QIcon(pixmap))
                    self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Adjust the size as needed
                ######################################################################
                global back_button, path, back_btn_clicked, folders_available, Lg_path, current_path, filename, ser
                import tkinter as tk
                from tkinter import ttk, simpledialog, messagebox
                import serial, time
                
                self.pushButton_login.setEnabled(False)
                self.pushButton_2.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_select_file.setEnabled(False)
                browse_folder = True
                back_btn_clicked = False
                path = f'cd\ncd {current_path}\nls -l\n'
                comport_is_active = interface_is_online(self.comport)
                
                # Send initial commands to Serial
                path = f'cd\ncd {current_path}\nls -l\n'
                comport_is_active = interface_is_online(self.comport)
                command = check_command(current_path)
                comport_is_active = interface_is_online(self.comport)
                if comport_is_active: 
                    send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n')
                # time.sleep(0.5)
                    lines = self.read_Response_END()  # Call the function
                    try:
                        lines = [line.decode('ascii').strip() for line in lines]
                    except UnicodeDecodeError as e:
                        messagebox.showwarning("Error!", "Oops! Something went wrong, Please check the connections")
                    
                    print(f"lines:{lines}")
                    if lines is None:
                        messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        # Load the SVG file using QSvgRenderer
                        svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                        # Create a QPixmap and render the SVG onto it
                        pixmap = QPixmap(45, 45)  # Set the size of the icon
                        pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                        # Use QPainter to render the SVG on the QPixmap
                        painter = QPainter(pixmap)
                        svg_renderer.render(painter)
                        painter.end()
                        # Set the rendered SVG as the icon for the QPushButton
                        icon = QIcon(pixmap)
                        self.pushButton_browse_record.setIcon(icon)
                        self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
                        self.pushButton.setEnabled(True)
                        self.pushButton_3.setEnabled(True)
                        self.pushButton_login.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_4.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.pushButton_select_file.setEnabled(True)
                        browse_folder = False
                        return  # Stop execution
                    if Commands_file_user:
                            with open(file_path_to_read_response, 'a') as file:
                                file.write(f'{get_current_datetime()} :Response after browse folder, ls-l')
                                file.write(f'\n{get_current_datetime()}   {lines}\n\n')
                else:
                    messagebox.showwarning("Warning", "COM port got disconnected!")
                    self.open_after_disconnection()
                    return
                folders_available, _ = extract_sections(lines)
                # Initialize the main window
                root = tk.Tk()
                # Set minimum size to prevent collapsing
                root.minsize(500, 500)
                # Set window to be resizable
                root.grid_columnconfigure(0, weight=1)
                root.grid_rowconfigure(0, weight=1)
                #root.geometry("500x500")
                root.resizable(True, True)

                root.title("Browse Folder")
                # Load the image using Pillow (PIL)
                icon_image = Image.open("folder_image.png")  # Replace with your image path
                icon_photo = ImageTk.PhotoImage(icon_image)
                # Set the image as the window icon
                root.iconphoto(False, icon_photo)

                #current_path = base_path
                # Create a label to display the current path
                current_path_label = tk.Label(root, text=f"Current Path:{current_path.strip()}", foreground="green")
                current_path_label.pack(pady=5)

                # Create a frame for folder and file selection
                main_frame = tk.Frame(root)
                main_frame.pack(padx=10, pady=10)

                # Create a vertical scrollbar for the listbox
                v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
                v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                # Create a horizontal scrollbar for the listbox
                h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)
                h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

                # Create a Listbox to display folders and files
                listbox = tk.Listbox(main_frame, height=10, width=40, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
                listbox.pack(pady=5)

                # Configure the scrollbars
                v_scrollbar.config(command=listbox.yview)
                h_scrollbar.config(command=listbox.xview)


                # Populate the Listbox with folder names
                for folder in folders_available:
                    listbox.insert(tk.END, folder)

                # Select the first item by default
                if folders_available:
                    listbox.select_set(0)

                # Define buttons outside functions to manage their visibility
                
                # Define back_button outside of functions
                
                # Create a frame for create and delete folder buttons
                buttons_frame = tk.Frame(root)
                buttons_frame.pack(pady=5)

                buttons_frame_2 = tk.Frame(root)
                buttons_frame_2.pack(pady=2)

                style = ttk.Style()
                style.configure("Red.TButton", background="red", foreground="red", font=("Arial", 8, "bold"))
                style_2 = ttk.Style()
                style_2.configure("Green.TButton", background="green", foreground="green", font=("Arial", 8, "bold"))
                style_3 = ttk.Style()
                style_3.configure("Orange.TButton", background="darkorange", foreground="darkorange", font=("Arial", 8, "bold"))
                # Create the button with the custom style
                create_folder_button = ttk.Button(buttons_frame, text="Create Folder", style= "Green.TButton", command=lambda: confirm_create_folder())
                delete_folder_button = ttk.Button(buttons_frame, text="Delete", style="Red.TButton", command=lambda: confirm_delete_folder())
                rename_button = ttk.Button(buttons_frame, text="Rename",style="Orange.TButton", command=lambda: confirm_rename_folder())
                create_folder_button.pack(side=tk.LEFT, padx=5)
                delete_folder_button.pack(side=tk.LEFT, padx=20)
                rename_button.pack(side=tk.LEFT, padx=5)

                open_files_button = ttk.Button(buttons_frame_2, text="Open Folder", command=lambda: open_file_selection())
                select_files_button = ttk.Button(buttons_frame_2, text="Select Folder", command=lambda: folder_selection())
                
                open_files_button.pack(side=tk.LEFT, padx=5)
                select_files_button.pack(side=tk.LEFT, padx=20)
                back_button = ttk.Button(root, text="Back", command=lambda: back_folder())
                
                # Pack the open file selection button initially
                #open_files_button.pack(pady=10)
                #select_files_button.pack(pady=10)
                buttons_frame.pack(pady=10)
                buttons_frame_2.pack(pady=10)
                
                back_button.pack(pady=10)
                # Function to update the listbox with new contents
                def update_listbox(contents):
                    listbox.delete(0, tk.END)  # Clear the current listbox content
                    for item in folders_available:
                        listbox.insert(tk.END, item)
                    # Select the first item by default
                    if folders_available:
                        listbox.select_set(0)

                def show_file_selection(folder):
                    global path, current_path, back_btn_clicked, back_button, folders_available, selected_folder, ser, browse_folder
                    selected_folder = folder

                    back_button.pack_forget()
                    if back_btn_clicked:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'pwd ; (echo END) > /dev/null\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   pwd ; (echo END) > /dev/null\n')
                        else:
                            messagebox.showwarning("Warning", "COM port got disconnected!")
                            root.destroy()
                            self.open_after_disconnection()
                            return                
                        #print(f'pwd\n')
                        # time.sleep(0.5)
                        dirct = self.read_Response_END()  # Call the function
                        if dirct is None:
                            messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                            return
                        dirctt = current_path.split("/")
                        directory = "/".join(dirctt[:-2])
                        directory = f'{directory}/'
                        #path = f'cd\ncd {directory}\nls -l\n'
                        current_path = f'{directory}' 
                        if ":" in directory:
                            directory=directory.split(":")[1]
                            #path = f'cd\ncd {directory}\nls -l\n'
                            current_path = f'{directory}' 
                            print(current_path)
                        comport_is_active = interface_is_online(self.comport)
                        print(current_path)
                        command = check_command(current_path)
                        send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n')
                        back_btn_clicked = False
                    else:
                        #path = f'cd\ncd {dirct}/{selected_folder}/\nls -l\n'
                        current_path = f"{current_path}{selected_folder}/"
                        comport_is_active = interface_is_online(self.comport)
                        command = check_command(current_path)
                        if comport_is_active: 
                            send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode dirs; (echo END) > /dev/null\n')
                        else:
                            messagebox.showwarning("Warning", "COM port got disconnected!")
                            root.destroy()
                            self.open_after_disconnection()
                            return
                        #print(f'hiicd\ncd {dirct}/{selected_folder}/\nls -l\n')
                    # time.sleep(0.5)
                    lines = self.read_Response_END()  # Call the function
                    if lines is None:
                        messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        return
                    try:
                        lines = [line.decode('ascii').strip() for line in lines]
                    except UnicodeDecodeError as e:
                        messagebox.showwarning("Error!", "Oops! Something went wrong, Please check the connections")
                        root.destroy()
                        self.open_after_disconnection()

                    folders_available, _ = extract_sections(lines)
                    back_button = ttk.Button(root, text="Back", command=lambda: back_folder())
                    back_button.pack(pady=5)
                    # Update the existing listbox with new contents
                    update_listbox(folders_available)
                    listbox.bind("<Double-1>", lambda event: open_file_selection())
                    # Update the current path label
                    current_path_label.config(text=f"Current Path: {current_path.strip()}")
                # Function to open file selection frame
                def open_file_selection():
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_item = listbox.get(selected_indices[0])
                        show_file_selection(selected_item)
                    else:
                        messagebox.showwarning("Warning", "Please select the Folder! / The Folder is empty!")

                def back_folder():
                    determine_path = current_path.split("/")
                    determine_path = "/".join(determine_path[:-1])
                    if base_path in str(determine_path):
                        global back_btn_clicked
                        back_btn_clicked = True
                        selected_indices = listbox.curselection()
                        if selected_indices:
                            selected_item = listbox.get(selected_indices[0])
                            print(f"{selected_item}\n\n")
                            show_file_selection(selected_item)
                        else:
                            selected_item = ""
                            show_file_selection(selected_item)
                    else:
                        messagebox.showwarning("Warning", "You cannot move back from here!")
###################################################################### Create folder #######################################################################################
                def confirm_create_folder():
                    global current_path, previous_path, root_create, root_create_popup
                    previous_path = current_path
                    path_check = current_path.split("/")
                    if len(path_check) == 4:
                        if path_check[3] == "":
                            messagebox.showwarning("Warning", "You cannot create a folder here!")
                            return
                        else:
                            pass
                    previous_path = str(previous_path).split("#")[0]
                    #print(previous_path)
                    result = messagebox.askyesno("Create Folder", "Are you sure you want to create a new folder?")
                    #result = messagebox.askyesno("Create Folder", "Are you sure you want to create a new folder?")
                    if result:
                        import tkinter as tk
                        from tkinter import ttk

                        def on_okay():
                            global folder_name
                            folder_name = entry.get()
                            #print(f"File name entered: {folder_name}")
                            create_folder(folder_name)
                           
                            # Add your logic here for what happens when Okay is clicked

                        def on_cancel():
                            global root_create_popup
                            root_create_popup = False
                            root_create.destroy()

                        root_create = tk.Tk()
                        root_create_popup = True
                        root_create.title("Folder Entry")
                        root_create.geometry("300x150")  # Set the size of the GUI
                        root_create.resizable(True, False)

                        # Entry for file name
                        entry_label = ttk.Label(root_create, text="Enter Folder Name:")
                        entry_label.pack(pady=5)


                        entry = ttk.Entry(root_create, width=30)
                        entry.pack(pady=5, padx=10, fill=tk.X)  # Limited within the size of the GUI
                        
                        # Buttons
                        button_frame = ttk.Frame(root_create)
                        button_frame.pack(pady=10)

                        okay_button = ttk.Button(button_frame, text="Okay", command=on_okay)
                        okay_button.pack(side=tk.LEFT, padx=5)

                        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
                        cancel_button.pack(side=tk.LEFT, padx=5)

                        root.bind('<Return>', on_okay)
                        # Ensure window appears on top and gets focus
                        root_create.lift()  # Bring the window to the top
                        root_create.attributes('-topmost', True)  # Make it temporarily the topmost window
                        root_create.after(1, lambda: root_create.attributes('-topmost', False))  # Remove topmost after focus

                        # Set focus after the window is fully initialized
                        root_create.after(100, entry.focus_force)
                        root_create.mainloop()

                # Function to confirm folder creation
                def create_folder(folder_name):
                    global file_name_starts_with_dot, browse_folder
                    print(folder_name)
                    if folder_name:
                        if folder_name not in folders_available:
                            folder_name = str(folder_name).strip()
                            #print(len(folder_name))
                            valid, message = validate_file_and_folder_name_linux(folder_name)
                            if valid:
                                if file_name_starts_with_dot:
                                    file_name_starts_with_dot = False
                                    msg_box_compare = QMessageBox()
                                    msg_box_compare.setWindowTitle("Warning")
                                    msg_box_compare.setText("File name starts with a dot (.) and will be hidden")
                                    msg_box_compare.setInformativeText("Hidden files are not visible during replay\nAre you sure you want to continue?")
                                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                    reply_3 = msg_box_compare.exec()
                                            # Check the user's choice
                                    if reply_3 == QMessageBox.StandardButton.Yes:         
                                        pass          
                                    else:
                                         root_create.destroy()                   

                                #else:
                                current_path = previous_path
                                print(folder_name)
                                print(current_path)
                                #print(f"Creating new folder: {folder_name}")  # Placeholder action
                                variable = f"{current_path}{folder_name}"
                                
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active: 
                                    send_command(bytearray(f'mkdir "{variable}" ; (echo END) > /dev/null\n', 'ascii'))
                                    if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   mkdir "{current_path}{folder_name}" ; (echo END) > /dev/null\n')
                                    lines = self.read_Response_END()  # Call the function
                                else:
                                     messagebox.showwarning("Warning", "COM port got disconnected!\nCould not create the folder")
                                     root_create.destroy()
                                     root.destroy()
                                     self.open_after_disconnection()
                                     return
                                
                                if lines is None:
                                    messagebox.showwarning("Error!", "Response not received within the timeout\n Please close the browse tab and reopen!")
                                    root_create.destroy()
                                    root.destroy()
                                    svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                                    # Create a QPixmap and render the SVG onto it
                                    pixmap = QPixmap(45, 45)  # Set the size of the icon
                                    pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                                    # Use QPainter to render the SVG on the QPixmap
                                    painter = QPainter(pixmap)
                                    svg_renderer.render(painter)
                                    painter.end()
                                    # Set the rendered SVG as the icon for the QPushButton
                                    icon = QIcon(pixmap)
                                    self.pushButton_browse_record.setIcon(icon)
                                    self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
                                    self.pushButton.setEnabled(True)
                                    self.pushButton_3.setEnabled(True)
                                    self.pushButton_login.setEnabled(True)
                                    self.pushButton_2.setEnabled(True)
                                    self.pushButton_4.setEnabled(True)
                                    self.pushButton_5.setEnabled(True)
                                    self.pushButton_select_file.setEnabled(True)
                                    browse_folder = False
                                    return  # Stop execution
                                else:
                                        folders_available.append(folder_name)
                                        listbox.insert(tk.END, folder_name)
                                        root_create.destroy()
                                                #print(current_path)
                            else:
                                messagebox.showwarning("Error", f'"{message}"')
                        else:
                            messagebox.showwarning("Folder Exists", "A folder with this name already exists.")
                    else:
                        messagebox.showwarning("No Name", "You must enter a folder name.")
#########################################################################################################################################################################################
                def confirm_rename_folder():
                    global ser
                    print(current_path)
                    listbox_items = listbox.get(0, tk.END)
                    print(listbox_items)
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_folder = listbox.get(selected_indices[0])
                        test = current_path.split("/")
                        print(len(test))
                        if len(test) <= 4:
                            messagebox.showwarning("Warning", "You cannot rename this folder!")
                            return
                        # Ask the user for the new folder name
                        new_folder_name = simpledialog.askstring("Rename Folder", "Enter the new folder name:")
                        if new_folder_name == "":
                            messagebox.showwarning("Invalid Name", "No new folder name provided.")
                            return
                        if new_folder_name in listbox_items and not new_folder_name == selected_folder:
                            messagebox.showwarning("Invalid Name", "A folder with this name already exists.")
                            return
                        if new_folder_name == selected_folder:
                            messagebox.showwarning("No changes!", "The entered name is the same as the selected folder.")
                            return
                        if new_folder_name:
                            # If a new name is provided, proceed with renaming
                            result = messagebox.askyesno("Rename Folder", f"Are you sure you want to rename the folder '{selected_folder}' to '{new_folder_name}'?")
                            if result:
                                folders_available.remove(selected_folder)
                                folders_available.append(new_folder_name)
                                listbox.delete(selected_indices[0])
                                listbox.insert(selected_indices[0], new_folder_name)

                                # Execute the rename command
                                comport_is_active = interface_is_online(self.comport)
                                print(current_path)
                                
                                
                                print(new_folder_name)
                                if comport_is_active:
                                    # Use the 'mv' command for renaming
                                    send_command(bytearray(f'mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}"\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}"\n{get_current_datetime()}   pwd\n')
                                else:
                                    messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                    root.destroy()
                                    self.open_after_disconnection()
                                    return
                               

                                # Check the file system (optional, based on your needs)
                                print(fs_system)

                                ########################################################################
                                if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True, destroy_root=True):
                                    return
                                ########################################################################
                            ########################################################################
                                lines = read_lines()
                                ###################################################################################
                                if comport_is_active:
                                        # Use the 'mv' command for renaming
                                        send_command(bytearray(f'cat "{read_selected_file_path}{filename_txt}" ; (echo END) > /dev/null\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   cat "{read_selected_file_path}{filename_txt}" ; (echo END) > /dev/null\n')
                                else:
                                        messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                        root.destroy()
                                        self.open_after_disconnection()
                                        return
                                lines = self.read_Response_END()  # Call the function
                                if lines is None:
                                    messagebox.showwarning("Error!",f"Renaming of the file is done\n\nIf the renamed file present in the {filename_txt}\nThe file name is not renamed in it,\nas response not received within timeout time\n\ncheck hardware connections!")
                                    return  # Stop execution
                                decoded_lines = [line.decode() for line in lines]
                                print(decoded_lines)
                                test_flag_2 = False
                                for line in decoded_lines:
                                        line = line.split("selected_files:")[-1].strip()
                                        print(line)
                                        print(f"{current_path}{selected_folder}")
                                        if f'{current_path}{selected_folder}' in line:
                                             line_to_edit = line
                                             print(f".......................{line}\n\n\n{current_path}{selected_folder}")
                                             print("yes")
                                             test_flag_2 = True
                                             print((line.split(f"{current_path}{selected_folder}")))
                                             line_needs_to_be_added = current_path+new_folder_name+(line.split(f"{current_path}{selected_folder}")[-1])
                                             print(line_needs_to_be_added)
                                             #break
                                if test_flag_2:
                                        print("hii")
                                        test_flag_2 = False
                                    
                                        line_to_edit = filename_txt_string_editor(line_to_edit)
                                        comport_is_active = interface_is_online(self.comport)

                                        if comport_is_active:
                                            send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                            file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return
                                        
                                        if comport_is_active:
                                            send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {line_needs_to_be_added}" >> {filename_txt}\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {line_needs_to_be_added}" >> {filename_txt}\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return    
                                #self.get_max_duration()
                    else:
                        messagebox.showwarning("Select Folder", "No folder is selected to Rename!")
                # Function to confirm folder deletion
                def confirm_delete_folder():
                        global ser
                        selected_indices = listbox.curselection()
                        if selected_indices:
                            test = current_path.split("/")
                            print(len(test))
                            if len(test) <= 4:
                                messagebox.showwarning("Warning", "You cannot delete this folder!")
                                return
                            
                            result = messagebox.askyesno("Delete Folder", f"Are you sure you want to delete the selected folder?")
                            if result:
                                #print(selected_indices)
                                selected_folder = listbox.get(selected_indices[0])
                                #print(selected_folder)
                                folders_available.remove(selected_folder)
                                listbox.delete(selected_indices[0])
                                #print(f"Deleting folder: {selected_folder}")  # Placeholder action
                                comport_is_active = interface_is_online(self.comport)
        
                                if comport_is_active: 
                                    send_command(bytearray(f'rm -r "{current_path}{selected_folder}" ; pwd\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   rm -r "{current_path}{selected_folder}" ; pwd\n')
                                else:
                                    messagebox.showwarning("Warning", "COM port got disconnected!\ncould not delete the selected folder")
                                    root.destroy()
                                    self.open_after_disconnection()
                                    return
                                print(fs_system)
                                  
                                ########################################################################
                                if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True, destroy_root=True):
                                    return
                                ########################################################################
                                self.get_max_duration()
                        else:
                            messagebox.showwarning("Select the folder", "No folder is selected to Delete!")

                def folder_selection():
                    global folder_name, Lg_path, current_path, browse_folder, selected_inside_folder, folder_HW_USB
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_inside_folder = False
                        selected_item = listbox.get(selected_indices[0])
                        print(f"selected item: {selected_item}")
                        result = messagebox.askyesno("Sure?", "Are you sure you want to save the file in this folder?")
                        if result:
                            Lg_path = f"{current_path}{selected_item}/".strip()
                            #print(Lg_path)
                            folder_name = f"{current_path}{selected_item}/".split("/")[-2]
                            #print(folder_name)
                            if not (browse_folder_for_HWUSB):
                                if show_path_btn_active:
                                    self.lineEdit_browse_record.setText(folder_name)
                                else:
                                    self.lineEdit_browse_record.setText(Lg_path)
                            else: 
                                folder_HW_USB = Lg_path
                                print(folder_HW_USB)
                            print(folder_HW_USB)
                            browse_folder = False
                            self.pushButton.setEnabled(True)
                            self.pushButton_3.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_select_file.setEnabled(True)
                            # Load the SVG file using QSvgRenderer
                            svg_renderer = QSvgRenderer("NEW_FILE.svg") 
                            # Replace with your SVG image path
                            pixmap = QPixmap(45, 45)  # Set the size of the icon
                            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                            # Use QPainter to render the SVG on the QPixmap
                            painter = QPainter(pixmap)
                            svg_renderer.render(painter)
                            painter.end()
                            # Set the rendered SVG as the icon for the QPushButton
                            icon = QIcon(pixmap)
                            self.pushButton_browse_record.setIcon(icon)
                            self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
                            #self.ensure_interface_disconnection()
                            root.destroy()
                    else:
                        result = messagebox.askyesno("Sure?", "Are you sure you want to save the file in this folder?")
                        if result:
                            selected_inside_folder = True
                            Lg_path = f"{current_path}".strip()
                            #print(Lg_path)
                            folder_name = current_path.split("/")[-2]
                            if not (browse_folder_for_HWUSB):
                                if show_path_btn_active:
                                    self.lineEdit_browse_record.setText(folder_name)
                                else:
                                    self.lineEdit_browse_record.setText(Lg_path)
                            else: 
                                folder_HW_USB = Lg_path
                                print(folder_HW_USB)
                            print(folder_HW_USB)
                            #print(folder_name)
                            """if show_path_btn_active:
                                self.lineEdit_browse_record.setText(folder_name)
                            else:
                                self.lineEdit_browse_record.setText(Lg_path)"""
                            browse_folder = False
                            # Load the SVG file using QSvgRenderer
                            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                            # Create a QPixmap and render the SVG onto it
                            pixmap = QPixmap(45, 45)  # Set the size of the icon
                            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                            # Use QPainter to render the SVG on the QPixmap
                            painter = QPainter(pixmap)
                            svg_renderer.render(painter)
                            painter.end()
                            # Set the rendered SVG as the icon for the QPushButton
                            icon = QIcon(pixmap)
                            self.pushButton_browse_record.setIcon(icon)
                            self.pushButton_browse_record.setIconSize(QSize(30, 30))  # Set icon size
                            self.pushButton.setEnabled(True)
                            self.pushButton_3.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_select_file.setEnabled(True)
                            #self.ensure_interface_disconnection()
                            root.destroy()
                # Bind double-click event to the Listbox
                listbox.bind("<Double-1>", lambda event: open_file_selection())
                root.protocol("WM_DELETE_WINDOW", on_secondary_close)
                # Start the Tkinter event loop
                root.mainloop()
        else:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Error!")
                msg_box_2.setText("Recording is ON!")
                msg_box_2.exec()

##################################################################################################################################
    def rebuild_image(self):
        self.label_SD_image_system_download_2.setVisible(False)
        self.label_SD_image_system_download.setVisible(True)
        #self.pushButton_refresh_config.setEnabled(False)
        self.fs_system_edit_btn.setEnabled(False)
        self.fs_system_submit_btn.setEnabled(False)
        self.label_fs_system_display.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_login.setEnabled(False)
        self.pushButton_browse_config.setEnabled(False)
        self.label_SD_image_display.setEnabled(False)
        
        QApplication.processEvents()  # Force UI update

        if interface_is_online(self.comport):   
            send_command(bytearray(f'cd /home/root/adc4bits/libiio/build/ && cmake ../ -DWITH_EXAMPLES=ON -DWITH_ZSTD=OFF && make clean && make -j4\n', 'ascii'))

            if Commands_file_user:
                with open(file_path, 'a') as file:
                    file.write(f'\n{get_current_datetime()}   cd /home/root/adc4bits/libiio/build/ && cmake ../ -DWITH_EXAMPLES=ON -DWITH_ZSTD=OFF && make clean && make -j4\n')

            def check_download_progress():
                global breakloop, download
                breakloop = False
                download = "0%"
                lines = read_lines()
                decoded_lines = [line.decode() for line in lines]
                for line in decoded_lines:
                    if "[" and "]" in line:
                        download = line.split("[")[1].split("]")[0].strip()
                        print(download)
                    if "[100%]" in line:
                        breakloop = True
                        print("done.........................")
                        break

                if breakloop:
                    breakloop = False
                    finalize_update()
                else:
                    self.label_SD_image_system_download.setText(f"Building in progress...({download})")
                    QTimer.singleShot(2000, check_download_progress)  # Check again after 2 seconds

            def finalize_update():
                self.label_SD_image_system_download_2.setVisible(True)
                self.label_SD_image_system_download.setVisible(False)
                self.pushButton_refresh_config.setEnabled(True)
                self.fs_system_edit_btn.setEnabled(True)
                self.fs_system_submit_btn.setEnabled(True)
                self.label_fs_system_display.setEnabled(True)
                self.pushButton_5.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_login.setEnabled(True)
                self.pushButton_browse_config.setEnabled(True)
                self.label_SD_image_display.setEnabled(True)
                QApplication.processEvents()  # Ensure UI updates

            check_download_progress()  # Start checking for progress

        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error!")
            msg_box.setText("COM port got disconnected!")
            msg_box.exec()

            self.label_SD_image_system_download_2.setVisible(False)
            self.label_SD_image_system_download.setVisible(False)
            self.pushButton_refresh_config.setEnabled(True)
            self.fs_system_edit_btn.setEnabled(True)
            self.fs_system_submit_btn.setEnabled(True)
            self.label_fs_system_display.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_login.setEnabled(True)
            self.pushButton_browse_config.setEnabled(True)
            self.label_SD_image_display.setEnabled(True)
            
            QApplication.processEvents()  # Ensure UI updates
            self.open_after_disconnection()

    
    def rebuild_image_1(self):
        self.label_SD_image_system_download_2.setVisible(False)
        self.label_SD_image_system_download.setVisible(True)
        self.pushButton_refresh_config.setEnabled(False)
        self.fs_system_edit_btn.setEnabled(False)
        self.fs_system_submit_btn.setEnabled(False)
        self.label_fs_system_display.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_login.setEnabled(False)
        #time.sleep(2)
        global download
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active:   
                    send_command(bytearray(f'cd /home/root/adc4bits/libiio/build/ && cmake ../ -DWITH_EXAMPLES=ON -DWITH_ZSTD=OFF && make clean && make -j4\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cd /home/root/adc4bits/libiio/build/ && cmake ../ -DWITH_EXAMPLES=ON -DWITH_ZSTD=OFF && make clean && make -j4\n')
                    testcount = 0
                    breakloop = False
                    # GUI Setup
                    while(True):
                        testcount += 1
                        lines = read_lines()
                        #print(lines)
                        decoded_lines = [line.decode() for line in lines]
                        for line in decoded_lines:
                            #print(line)
                            if "[" and "]" in line:
                                download = line.split("[")[1].split("]")[0].strip()
                                print(download)
                            if "[100%]" in line:
                                breakloop = True
                                print("done.........................")
                                break
                                
                        if breakloop == True:
                            breakloop = False
                            self.label_SD_image_system_download_2.setVisible(True)
                            self.label_SD_image_system_download.setVisible(False)
                            self.pushButton_refresh_config.setEnabled(True)
                            self.fs_system_edit_btn.setEnabled(True)
                            self.fs_system_submit_btn.setEnabled(True)
                            self.label_fs_system_display.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            break
                        #self.label_SD_image_system_download.setText(f"Dowload percentage: {download}")
                        time.sleep(2)
        else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.label_SD_image_system_download_2.setVisible(False)
                    self.label_SD_image_system_download.setVisible(False)
                    self.pushButton_refresh_config.setEnabled(True)
                    self.fs_system_edit_btn.setEnabled(True)
                    self.fs_system_submit_btn.setEnabled(True)
                    self.label_fs_system_display.setEnabled(True)
                    self.pushButton_5.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.pushButton_2.setEnabled(True)
                    self.pushButton_login.setEnabled(True)
                    self.open_after_disconnection()
                    return
             
    def give_nvme_info(self):
        global flag_raised
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active: 
            send_command(bytearray(f'lsblk ; (echo END) > /dev/null\n', 'ascii'))
            if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   lsblk ; (echo END) > /dev/null\n')
            lines = self.read_Response_END()  # Call the function
            if lines is None:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                    msg_box_11.exec()
                    return  # Stop execution
            print(lines)
            output = ''.join([line.decode('utf-8') for line in lines[1:-2]])
            
            def raise_flag():
                global flag_raised
                flag_raised = False

            if not gui_opened and not flag_raised:
                    flag_raised = True
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("NVME Information")
                    msg_box_11.setText(f"{output}")
                    # Connect the finished signal to raise the flag
                    msg_box_11.finished.connect(raise_flag)
                    msg_box_11.exec()
        else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Comport got disconnected")
                    msg_box_11.exec()
                    #self.open_after_disconnection()
                    return 
    ###########################################################################################################################################
            
    def submit_to_edit(self):
        count = 0
        global fs_system, ser, submit_btn_clicked, Edit_btn_clicked, nvme_label_found, ser, executable_rx, executable_tx
        print(self.fs_system_GUI)
        if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True):
            return
        if not "/dev/" in self.fs_system_GUI:
            nvme_label_found = False
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Please enter a valid label of nvme SSD")
            msg_box_11.exec()
            return
        length_ssd = len(str(self.fs_system_GUI).split("/"))
        if not length_ssd >= 3:
            nvme_label_found = False
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Please enter a valid label of nvme SSD")
            msg_box_11.exec()
            return
        folder_name_ssd = str(self.fs_system_GUI).split('/dev/')[1].strip()
        if folder_name_ssd == "":
            nvme_label_found = False
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Please enter a valid label of nvme SSD")
            msg_box_11.exec()
            return
            
        fs_system = self.fs_system_GUI 
        directory = read_selected_file_path    
        command = check_command(directory)
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active: 
            send_command(bytearray(f'cd {command}\n', 'ascii'))
            if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cd {command}\n')
            lines = read_lines()
        else:
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
            msg_box_11.exec()
            self.open_after_disconnection()
            return
    
        comport_is_active = interface_is_online(self.comport)
        actual_nvme = check_command(nvmelabel_file)
        actual_filename = check_command(filename_txt)
        if comport_is_active:                    
            send_command(bytearray(f'cat {actual_nvme}\n', 'ascii'))
            if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cat {actual_nvme}\n')
            lines = read_lines()
            print(lines)
        else:
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
            msg_box_11.exec()
            self.open_after_disconnection()
            return

        if len(lines) >= 2:
            if not nvmelabel_file in str(lines[0]):
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Oops! 'HW_files' folder is not found\nIn the directory {read_selected_file_path}")
                msg_box_11.exec() 
                return
        else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops!, Please check the connections\nIs the AD9361 Hardware connected?")
                    msg_box_11.exec() 
                    return
        #########################################################################
        lines = lines[1:-1]
        try:
            decoded_lines = [line.decode() for line in lines]
        except UnicodeDecodeError as e:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Oops! Something went wrong, Please check the connections")
                msg_box_11.exec() 
                return
        
        if not "No such file or directory" in (decoded_lines[-1]):
                for line in decoded_lines:
                    count += 1
                    if "fs_system:" in line:
                        comport_is_active = interface_is_online(self.comport)
                        command = check_command(read_selected_file_path)
                        if comport_is_active: 
                            send_command(bytearray(f'cd {command}\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   cd {command}\n')
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                            
                        comport_is_active = interface_is_online(self.comport)
                        actual_nvme = check_command(nvmelabel_file)
                        actual_filename = check_command(filename_txt)
                        if comport_is_active: 
                            send_command(bytearray(f'sed -i "/^fs_system:/d" {actual_nvme}\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   sed -i "/^fs_system:/d" {actual_nvme}\n')
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return

                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f"sed -i '/^$/d' {actual_nvme}\n", 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   sed -i '/^$/d' {actual_nvme}\n")
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        new_lines = f"fs_system: {fs_system}"
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f"echo '{new_lines}'>>{actual_nvme}\n", 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   echo '{new_lines}'>>{actual_nvme}\n")
                            response = read_lines()
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        
        elif "No such file or directory" in (decoded_lines[-1]):
                    ###########################################################################################
                    comport_is_active = interface_is_online(self.comport)
                    command = check_command(directory)
                    if comport_is_active: 
                        send_command(bytearray(f'cd {command}\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   cd {command}\n')
                    else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    ###########################################################################################
                    comport_is_active = interface_is_online(self.comport)
                    actual_nvme = check_command(nvmelabel_file)
                    actual_filename = check_command(filename_txt)
                    if comport_is_active: 
                        send_command(bytearray(f'touch {actual_nvme}\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   touch {actual_nvme}\n')
                    else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    #############################################################################################
                    text_file_content = "fs_system: /dev/"
                    tx_rx_file_content = f"\nRx: {executable_rx}\nTx: {executable_tx}"
                    comport_is_active = interface_is_online(self.comport)
                    if comport_is_active: 
                        send_command(bytearray(f'echo  "{text_file_content}">> {actual_nvme}\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   echo  "{text_file_content}">> {actual_nvme}\n')
                                fs_system = "/dev/"
                    else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    bs = read_lines()
                    print(bs)
                    ###############################################################################################
                    comport_is_active = interface_is_online(self.comport)
                    if comport_is_active: 
                        send_command(bytearray(f'echo  "{tx_rx_file_content}">> {actual_nvme}\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   echo  "{tx_rx_file_content}">> {actual_nvme}\n')
                    else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    bs = read_lines()
                    print(bs)
                    ################################################################################################
                    developer_tx_rx_content = f"\nDRx: {developer_executable_rx}\nDTx: {developer_executable_tx}"
                    comport_is_active = interface_is_online(self.comport)
                    if comport_is_active: 
                        send_command(bytearray(f'echo  "{developer_tx_rx_content}">> {actual_nvme}\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   echo  "{developer_tx_rx_content}">> {actual_nvme}\n')
                    else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not submit the changes")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                    bs = read_lines()
                    print(bs)
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Info")
                    msg_box_11.setText(f"The file {nvmelabel_file} not found\n\nA new {nvmelabel_file} file is created\n\nDirectory:{directory}")
                    msg_box_11.exec()
                    ################################################################################################
        submit_btn_clicked = False
        Edit_btn_clicked = True
        self.fs_system_submit_btn.setVisible(False)
        self.fs_system_edit_btn.setVisible(True)
        self.lineEdit_fs_system.setEnabled(False)
        self.lineEdit_fs_system.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #4A6375;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        self.lineEdit_fs_system.setText(fs_system)

    def edit_to_submit(self):
        global fs_system, submit_btn_clicked, Edit_btn_clicked
        submit_btn_clicked = True
        Edit_btn_clicked = False
        self.fs_system_submit_btn.setVisible(True)
        self.fs_system_edit_btn.setVisible(False)
        self.lineEdit_fs_system.setEnabled(True)
        self.lineEdit_fs_system.setStyleSheet("""
                                        QLineEdit {
                                            background-color: #2C3E50;
                                            color: #FFFFFF;
                                            border: 2px solid #1ABC9C;
                                            border-radius: 5px;
                                            padding: 5px;
                                        }
                                        QLineEdit:focus {
                                            border: 2px solid #2E5;
                                        }
                                    """)
        fs_system = self.fs_system_GUI 
        self.lineEdit_fs_system.setText(fs_system)
################################################################################################################################################################
    def hide_to_show_path(self):
        global show_path_btn_active, hide_path_btn_active, show_path_btn_active_replay, hide_path_btn_active_replay, selected_inside_folder
        if record_tab:
            if Lg_path == "":
                return
            if folder_name == "":
                return
            
            self.show_path_btn.setVisible(False)
            self.hide_path_btn.setVisible(True)
            show_path_btn_active = False
            hide_path_btn_active = True  
            if not Lg_path == "":  
                if selected_inside_folder:
                    path = f'{Lg_path}'
                if not selected_inside_folder:
                    path = f'{Lg_path}'

            self.lineEdit_browse_record.setText(path)  
            #self.lineEdit_browse_record.setReadOnly(True)
        if replay_tab:
            if Lg_path == "":
                return
            if filename == "":
                return

            self.show_path_btn_replay.setVisible(False)
            self.hide_path_btn_replay.setVisible(True)
            show_path_btn_active_replay = False
            hide_path_btn_active_replay = True  
            if not Lg_path == "":  
                path = f'{Lg_path}{filename}'
                self.lineEdit9.setText(path)  
            #self.lineEdit_browse_record.setReadOnly(True)
        print("hide")

    def show_to_hide_path(self):
        global show_path_btn_active, hide_path_btn_active, hide_path_btn_active_replay, show_path_btn_active_replay
        if record_tab:
            self.show_path_btn.setVisible(True)
            self.hide_path_btn.setVisible(False)
            show_path_btn_active = True
            hide_path_btn_active = False
            if not folder_name == "":  
                self.lineEdit_browse_record.setText(folder_name)
            #self.lineEdit_browse_record.setReadOnly(True)
            print("show")   
        if replay_tab:
            self.show_path_btn_replay.setVisible(True)
            self.hide_path_btn_replay.setVisible(False)
            show_path_btn_active_replay = True
            hide_path_btn_active_replay = False
            #filename = Lg_path.split("/")[-2]
            #print(filename)
            if not filename == "":  
                self.lineEdit9.setText(filename)
            #self.lineEdit_browse_record.setReadOnly(True)
            print("show")

    def hide_to_show_path_rtcm(self):
        global show_path_btn_active_rtcm, hide_path_btn_active_rtcm, show_path_btn_active_replay_rtcm, hide_path_btn_active_replay_rtcm, selected_inside_folder
        if self.radioButton_rtcm.isChecked():
            if record_tab:
                if rtcm_folder_path == "":
                    return
                self.show_path_btn_rtcm.setVisible(False)
                self.hide_path_btn_rtcm.setVisible(True)
                show_path_btn_active_rtcm = False
                hide_path_btn_active_rtcm = True  
                self.lineEdit_browse_record_rtcm.setText(rtcm_folder_path)  
                return
                #self.lineEdit_browse_record.setReadOnly(True)
            if replay_tab:
                if rtcm_file_path == "":
                    return
                self.show_path_btn_replay_rtcm.setVisible(False)
                self.hide_path_btn_replay_rtcm.setVisible(True)
                show_path_btn_active_replay_rtcm = False
                hide_path_btn_active_replay_rtcm = True  
                self.lineEdit_replay_rtcm.setText(rtcm_file_path)
                return
                #self.lineEdit_browse_record.setReadOnly(True)
            print("hide")

    def show_to_hide_path_rtcm(self):
        global show_path_btn_active_rtcm, hide_path_btn_active_rtcm, hide_path_btn_active_replay_rtcm, show_path_btn_active_replay_rtcm
        if self.radioButton_rtcm.isChecked():
            if record_tab:
                self.show_path_btn_rtcm.setVisible(True)
                self.hide_path_btn_rtcm.setVisible(False)
                show_path_btn_active_rtcm = True
                hide_path_btn_active_rtcm = False
                self.lineEdit_browse_record_rtcm.setText(rtcm_folder_name)
                print("show")   
                return
            if replay_tab:
                self.show_path_btn_replay_rtcm.setVisible(True)
                self.hide_path_btn_replay_rtcm.setVisible(False)
                show_path_btn_active_replay_rtcm = True
                hide_path_btn_active_replay_rtcm = False
                rtcmfile = rtcm_file_name.split(".rtcm")[0]
                self.lineEdit_replay_rtcm.setText(rtcmfile)
                print("show")
                return
###################################################################################################################################################################
    def invisible_button(self):
        print("helloo")
        global click_count
        if not replay_started and not browse_files and not browse_folder and not config_browse_file and not delete_gui:
            if ((self.baudrate != None) and
                (self.comport != None)):
                if not submitted:
                    return
                fs_system_len = fs_system.split("/")
                if not fs_system == "/dev/" and len(fs_system_len)>=3:
                    click_count += 1
                    if click_count == satellite_clicks:
                        self.open_new_window()

    def open_pdf(self):
        if os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)  # Opens the file with the default PDF viewer (Windows)
            except AttributeError:  # For non-Windows systems
                os.system(f'xdg-open "{pdf_path}"')
        else:
            print("The PDF file does not exist.")
    

    def open_new_window(self):
        global click_count, gui_opened
        global executable_rx, executable_tx, developer_executable_rx, developer_executable_tx, ser, root, current_in_use

        if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True):
            return
        
        if developer_rx_tx:
            current_in_use = "Developer"
        else:
            current_in_use = "Released"
        
        comport_is_active = interface_is_online(self.comport)
        actual_nvme = check_command(nvmelabel_file)
        actual_filename = check_command(filename_txt)
        command = check_command(read_selected_file_path)
        if comport_is_active: 
            send_command(bytearray(f'cd {command}\n', 'ascii'))
            if Commands_file_user:
                with open(file_path, 'a') as file:
                    file.write(f'\n{get_current_datetime()}   cd {command}\n')
            lines = read_lines()
        else:
            return
        comport_is_active = interface_is_online(self.comport)
        if comport_is_active:                       
            send_command(bytearray(f'cat {actual_nvme}\n', 'ascii'))
            if Commands_file_user:
                with open(file_path, 'a') as file:
                    file.write(f'\n{get_current_datetime()}   cat {actual_nvme}\n')
            lines = read_lines()
        else:
            return
        
        #print(lines)
        if len(lines) >= 2:
            if not nvmelabel_file in str(lines[0]):
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Oops! 'HW_files' folder is not found\nIn the directory {read_selected_file_path}")
                msg_box_11.exec() 
                return
        else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops!, Please check the connections\nIs the AD9361 Hardware connected?")
                    msg_box_11.exec() 
                    return
        #######################################################################################
        lines = lines[1:-1]
        print(lines)
        try:
            decoded_lines = [line.decode() for line in lines]
        except UnicodeDecodeError as e:
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Oops! Something went wrong, Please check the connections")
            msg_box_11.exec() 
            return
        print(decoded_lines)

        if not "No such file or directory" in (decoded_lines[-1]):
            for line in decoded_lines:
                if line.startswith("Rx:"):
                    executable_rx = str(line.split(":")[-1]).strip()
                if line.startswith("Tx:"):
                    executable_tx = str(line.split(":")[-1]).strip()
                    print(executable_tx)
                if "DRx:" in line:
                    developer_executable_rx = str(line.split(":")[-1]).strip()
                    print(developer_executable_rx)
                if "DTx:" in line:
                    developer_executable_tx = str(line.split(":")[-1]).strip()      
                    print(developer_executable_tx)  
            
          
        elif "No such file or directory" in (decoded_lines[-1]):
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"Oops!, {nvmelabel_file} not found!")
            msg_box_11.exec() 
            return
        print(executable_rx)
        
        if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True):
            return
        
        # Display a message or open a new window
        def on_radio_button_change():
            global executable_rx, executable_tx, developer_executable_rx, developer_executable_tx
            selected_option = radio_var.get()
            print(selected_option)
            if selected_option == "Developer":        
                developer_executable_tx_2 = developer_executable_tx.split("nice --20")[1].strip()
                developer_executable_rx_2 = developer_executable_rx.split("nice --20")[1].strip()
                hello_label.config(text=f"Rx: {developer_executable_rx_2}")
                hello_label_tx.config(text=f"Tx: {developer_executable_tx_2}")
                entry.config(state="normal")
                entry.delete(0, tk.END)  # Clear current text
                entry.insert(0, f"{developer_executable_rx_2}")  # Set text to "hii"

                entry_tx.config(state="normal")
                entry_tx.delete(0, tk.END)  # Clear current text
                entry_tx.insert(0, f"{developer_executable_tx_2}")
                submit_button.config(state="normal")  # Enable the submit button
            elif selected_option == "Released":
                print(executable_rx)
                executable_rx_2 = executable_rx_fixed.split("nice --20")[1].strip()
                executable_tx_2 = executable_tx_fixed.split("nice --20")[1].strip()
                hello_label.config(text=f"Rx: {executable_rx_2}")
                hello_label_tx.config(text=f"Tx: {executable_tx_2}")
                entry.delete(0, tk.END)  # Clear text when disabled
                entry.insert(0, f"{executable_rx_2}")  # Reset to placeholder
                entry.config(state="disabled")

                
                entry_tx.delete(0, tk.END)  # Clear text when disabled
                entry_tx.insert(0, f"{executable_tx_2}")  # Reset to placeholder
                entry_tx.config(state="disabled")
                submit_button.config(state="normal")  # Disable the submit button

        def on_submit():
            print("hi")
            global developer_executable_rx, developer_executable_tx, ser, line_tx_rx_count, developer_rx_tx, executable_rx, executable_tx, gui_opened
            developer_executable_rx_2 = entry.get()
            developer_executable_tx_2 = entry_tx.get()
            developer_executable_rx = f"nice --20 {developer_executable_rx_2}"
            developer_executable_tx = f"nice --20 {developer_executable_tx_2}"
            print(developer_executable_rx)
            print(developer_executable_tx)
            selected_option = radio_var.get()

            if selected_option == "Developer":
                 developer_rx_tx = True
            else:
                 developer_rx_tx = False

            if developer_rx_tx:
                self.label_developer.setVisible(True)
            else:
                self.label_developer.setVisible(False)
            
            directory = read_selected_file_path   
            comport_is_active = interface_is_online(self.comport)
            command = check_command(read_selected_file_path)
            actual_nvme = check_command(nvmelabel_file)
            actual_filename = check_command(filename_txt)
            if comport_is_active: 
                send_command(bytearray(f'cd {command}\n', 'ascii'))
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f'\n{get_current_datetime()}   cd {command}\n')
                lines = read_lines()
            #print(lines)
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"COM port got disconnected!")
                msg_box_11.exec() 
                self.open_after_disconnection()
                return
            comport_is_active = interface_is_online(self.comport)
            if comport_is_active:                      
                send_command(bytearray(f'cat {actual_nvme}\n', 'ascii'))
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f'\n{get_current_datetime()}   cat {actual_nvme}\n')
                lines = read_lines()
                print(lines)
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"COM port got disconnected!")
                msg_box_11.exec() 
                self.open_after_disconnection()
                return
            
            if len(lines) >= 2:
                if not nvmelabel_file in str(lines[0]):
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops! 'HW_files' folder is not found\nIn the directory {read_selected_file_path}")
                    msg_box_11.exec() 
                    return
            else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops!, Please check the connections\nIs the AD9361 Hardware connected?")
                    msg_box_11.exec() 
                    return
            #######################################################################################
            lines = lines[1:-1]
            print(lines)
            try:
                    decoded_lines = [line.decode() for line in lines]
            except UnicodeDecodeError as e:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops! Something went wrong, Please check the connections")
                    msg_box_11.exec() 
                    return
            print(decoded_lines)
            if not "No such file or directory" in (decoded_lines[-1]):
                    ##########################################################
                    if developer_rx_tx:
                        for line in decoded_lines:
                            if gui_opened:
                                line_tx_rx_count += 1
                                if "DRx:" in line:
                                    #############################################################################
                                    comport_is_active = interface_is_online(self.comport)
                                    command = check_command(read_selected_file_path)
                                    if comport_is_active: 
                                        send_command(bytearray(f'cd {command}\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   cd {command}\n')
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected!")
                                        msg_box_11.exec()
                                        self.open_after_disconnection() 
                                        return
                                    comport_is_active = interface_is_online(self.comport)
                                    actual_nvme = check_command(nvmelabel_file)
                                    actual_filename = check_command(filename_txt)
                                    if comport_is_active: 
                                        send_command(bytearray(f'sed -i "/^DRx\|^DTx/d" {actual_nvme}\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   sed -i "/^DRx\|^DTx/d" {actual_nvme}\n')
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected!")
                                        msg_box_11.exec() 
                                        self.open_after_disconnection()
                                        return
                                    

                                    new_lines = f"\nDRx: {developer_executable_rx}\nDTx: {developer_executable_tx}"
                                    comport_is_active = interface_is_online(self.comport)
                                    if comport_is_active: 
                                        send_command(bytearray(f'echo "{new_lines}">>{actual_nvme}\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   echo "{new_lines}">>{actual_nvme}\n')
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected!")
                                        msg_box_11.exec()
                                        self.open_after_disconnection() 
                                        return
                                    response = read_lines()
                                    comport_is_active = interface_is_online(self.comport)
                                    if comport_is_active: 
                                        send_command(bytearray(f"sed -i '/^$/d' {actual_nvme}\n", 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f"\n{get_current_datetime()}   sed -i '/^$/d' {actual_nvme}\n")
                                        response = read_lines()
                                        print(f"response: {response}")
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected!")
                                        msg_box_11.exec() 
                                        self.open_after_disconnection()
                                        return
                                    if gui_opened:
                                        if developer_rx_tx:
                                            executable_rx = developer_executable_rx
                                            executable_tx = developer_executable_tx
                                        print(f"Submitted value: {developer_executable_rx}")
                    on_secondary_close_()                
                            
            else:
                msg_box_11 = QMessageBox()
                msg_box_11.setWindowTitle("Error!")
                msg_box_11.setText(f"Oops!, {nvmelabel_file} is not found!")
                msg_box_11.exec() 
                return
            
        def on_entry_focus_in(event):
            if entry.get() == "Enter your text here...":
                entry.delete(0, tk.END)
                entry.config(foreground="black")

            if entry_tx.get() == "Enter your text here...":
                entry_tx.delete(0, tk.END)
                entry_tx.config(foreground="black")

        def on_entry_focus_out(event):
            if not entry.get():
                entry.insert(0, "Enter your text here...")
                entry.config(foreground="grey")

            if not entry_tx.get():
                entry_tx.insert(0, "Enter your text here...")
                entry_tx.config(foreground="grey")

        # Create the main window
        def on_secondary_close_():
            print("Terminated")
            global gui_opened, click_count
            if gui_opened:
                gui_opened = False
                click_count = 0
                root.destroy()
            return

        import tkinter as tk
        from tkinter import ttk

        root = tk.Tk()
        root.title("Developer/Release")
        print(executable_rx)
        gui_opened = True

        # Create the main frame with padding
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the radio buttons
        radio_frame = ttk.Frame(main_frame)
        radio_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Create a variable to hold the value of the selected radio button
        if current_in_use == "Released":
            radio_var = tk.StringVar(value="Released")
        else:
            radio_var = tk.StringVar(value="Developer")

        # Create two radio buttons
        radio_button1 = ttk.Radiobutton(radio_frame, text="Released", variable=radio_var, value="Released", command=on_radio_button_change)
        radio_button2 = ttk.Radiobutton(radio_frame, text="Developer", variable=radio_var, value="Developer", command=on_radio_button_change)

        # Pack the radio buttons side by side
        radio_button1.pack(side="left", padx=10)
        radio_button2.pack(side="left", padx=10)

        label = tk.Label(main_frame, text=f"Current path: {current_in_use}", font=("Arial", 12), fg="blue")
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create the hello label above the entry fields
        if current_in_use == "Released":
            executable_rx_2 = executable_rx.split("nice --20")[1].strip()
            executable_tx_2 = executable_tx.split("nice --20")[1].strip()
        else:
            executable_rx_2 = developer_executable_rx.split("nice --20")[1].strip()
            executable_tx_2 = developer_executable_tx.split("nice --20")[1].strip()

        hello_label = ttk.Label(main_frame, text=f"Rx: {executable_rx_2}")  # Default to "Hi"
        hello_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        hello_label_tx = ttk.Label(main_frame, text=f"Tx: {executable_tx_2}")  # Default to "Hi"
        hello_label_tx.grid(row=3, column=0, columnspan=2, pady=10)

        # Create a label and entry widget side by side
        entry_label = ttk.Label(main_frame, text="Enter Rx:")
        entry_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        entry = ttk.Entry(main_frame, foreground="grey", width= 50 )
        
        entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Bind events to simulate placeholder behavior
        """entry.bind("<FocusIn>", on_entry_focus_in)
        entry.bind("<FocusOut>", on_entry_focus_out)"""

        # Initially disable the entry widget since Option 2 is selected by default
        if current_in_use == "Released":
            entry.insert(0, f"{executable_rx_2}")  # Placeholder text
            entry.config(state="disabled")
        else:
            entry.insert(0, f"{executable_rx_2}")
            entry.config(state="enabled")

        entry_label_tx = ttk.Label(main_frame, text="Enter Tx:")
        entry_label_tx.grid(row=5, column=0, padx=10, pady=5, sticky="e")

        entry_tx = ttk.Entry(main_frame, foreground="grey", width= 50)
        #entry_tx.insert(0, "Enter the Tx here...")  # Placeholder text
        entry_tx.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Bind events to simulate placeholder behavior
        """entry_tx.bind("<FocusIn>", on_entry_focus_in)
        entry_tx.bind("<FocusOut>", on_entry_focus_out)"""

        # Initially disable the entry widget since Option 2 is selected by default
        if current_in_use == "Released":
            entry_tx.insert(0, f"{executable_tx_2}")  # Placeholder text
            entry_tx.config(state="disabled")
        else:
            entry_tx.insert(0, f"{executable_tx_2}")
            entry_tx.config(state="enabled")

        # Create a Submit button centered in the window
        submit_button = ttk.Button(main_frame, text="Submit", command=on_submit)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Initially disable the submit button
        submit_button.config(state="normal")

        # Make the columns expand equally to ensure centering
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Start the GUI loop
        root.protocol("WM_DELETE_WINDOW", on_secondary_close_)
        root.mainloop()


    def browse_file(self):
        global HW_file_path
        if config_button:
            self.populate_table()
            if len(self.variable_names) >= 4:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Error!")
                msg_box_2.setText("Already there are 4 files!")
                msg_box_2.exec()
                return
                
        def on_secondary_close():
            global root, browse_files
            browse_files = False
            # Load the SVG file using QSvgRenderer
            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
            # Create a QPixmap and render the SVG onto it
            pixmap = QPixmap(45, 45)  # Set the size of the icon
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
            # Use QPainter to render the SVG on the QPixmap
            painter = QPainter(pixmap)
            svg_renderer.render(painter)
            painter.end()
            # Set the rendered SVG as the icon for the QPushButton
            icon = QIcon(pixmap)
            self.pushButton_8.setIcon(icon)
            self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size
    
            self.pushButton_7.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_login.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_select_file.setEnabled(True)

            print("terminated")
            root.destroy()

        if not replay_started:
            global browse_files, root, ser, back_btn_clicked,current_path, path, folders_available, back_button, response,bandwidth, Sampling_frequency, log_duration, bits, bandwidthflag, Sampling_frequency_flags, log_durationflags, bits_flags, response, directory, filename
            if not browse_files:
                import tkinter as tk
                from tkinter import ttk, simpledialog, messagebox
                import serial, time
                browse_files = True
                back_btn_clicked = False
                self.pushButton_7.setEnabled(False)
                self.pushButton_6.setEnabled(False)
                self.pushButton_login.setEnabled(False)
                self.pushButton_2.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(False)
                self.pushButton_select_file.setEnabled(False)
                # Load the SVG file using QSvgRenderer
                if not browse_file_for_HWUSB:
                    svg_renderer = QSvgRenderer("selected_file.svg")  # Replace with your SVG image path
                    # Create a QPixmap and render the SVG onto it
                    pixmap = QPixmap(45, 45)  # Set the size of the icon
                    pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                    # Use QPainter to render the SVG on the QPixmap
                    painter = QPainter(pixmap)
                    svg_renderer.render(painter)
                    painter.end()
                    # Set the rendered SVG as the icon for the QPushButton
                    icon = QIcon(pixmap)
                    self.pushButton_8.setIcon(icon)
                    self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size
                #path = 'cd\ncd /run/media/nvme0n1p1/logs/\nls -l\n'
                comport_is_active = interface_is_online(self.comport)
                
                # Send initial commands to Serial
                #path = 'cd\ncd /run/media/nvme0n1p1/logs/\nls -l\n'
                print(current_path)
                comport_is_active = interface_is_online(self.comport)
                command = check_command(current_path)
                print(f"command: {command}")

                comport_is_active = interface_is_online(self.comport)
                if comport_is_active: 
                    if not (browse_file_for_HWUSB):
                        send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command}; (echo END) > /dev/null\n', 'ascii'))
                        with open(file_path, 'a') as file:
                            file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command}; (echo END) > /dev/null\n")
                    else:
                        
                        send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode rtcm; (echo END) > /dev/null\n', 'ascii'))
                        with open(file_path, 'a') as file:
                            file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode rtcm; (echo END) > /dev/null\n")
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   ls -l ; (echo END) > /dev/null\n')
                # time.sleep(0.5)
                else:
                     messagebox.showwarning("Warning", "Comport got disconnected")
                     self.open_after_disconnection()
                     return
                lines = self.read_Response_END() 
                try:
                    lines = [line.decode('ascii').strip() for line in lines]
                except UnicodeDecodeError as e:
                    messagebox.showwarning("Error!", "Oops! Something went wrong, Please check the connections")
                print(f"lines: {lines}  ")
                if lines is None:
                    messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                    browse_files = False
                    self.pushButton_7.setEnabled(True)
                    self.pushButton_6.setEnabled(True)
                    self.pushButton_login.setEnabled(True)
                    self.pushButton_2.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.pushButton_5.setEnabled(True)
                    self.pushButton_select_file.setEnabled(True)
                    # Load the SVG file using QSvgRenderer
                    svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                    # Create a QPixmap and render the SVG onto it
                    pixmap = QPixmap(45, 45)  # Set the size of the icon
                    pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                    # Use QPainter to render the SVG on the QPixmap
                    painter = QPainter(pixmap)
                    svg_renderer.render(painter)
                    painter.end()
                    # Set the rendered SVG as the icon for the QPushButton
                    icon = QIcon(pixmap)
                    self.pushButton_8.setIcon(icon)
                    self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size
                    return
               
                if Commands_file_user:
                            with open(file_path_to_read_response, 'a') as file:
                                file.write(f'{get_current_datetime()} :Response after ls -l')
                                file.write(f'\n{get_current_datetime()}   {lines}\n\n')
                #################################################################################################################################################
                folders_names_1 = []
                file_names_1 = []
                folders_names_1, file_names_1 = extract_sections(lines)
                # Example folder and file data
                folders_available = folders_names_1 + file_names_1
                print(folders_available)

                # Initialize the main window
                root = tk.Tk()
                root.minsize(500, 400)
                # Set window to be resizable
                root.grid_columnconfigure(0, weight=1)
                root.grid_rowconfigure(0, weight=1)
                #root.geometry("500x500")
                root.resizable(True, True)
                root.title("Browse files")
                # Load the image using Pillow (PIL)
                icon_image = Image.open("Files_image.png")  # Replace with your image path
                icon_photo = ImageTk.PhotoImage(icon_image)

                # Set the image as the window icon
                root.iconphoto(False, icon_photo)
                #current_path = base_path
                # Create a label to display the current path
                current_path_label = tk.Label(root, text=f"Current Path:{current_path.strip()}", foreground="green")
                current_path_label.pack(pady=5)

                # Create a frame for folder and file selection
                main_frame = tk.Frame(root)
                main_frame.pack(padx=10, pady=10)

                # Create a vertical scrollbar for the listbox
                v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
                v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                # Create a horizontal scrollbar for the listbox
                h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)
                h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

                # Create a Listbox to display folders and files
                listbox = tk.Listbox(main_frame, height=10, width=40, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
                listbox.pack(pady=5)

                # Configure the scrollbars
                v_scrollbar.config(command=listbox.yview)
                h_scrollbar.config(command=listbox.xview)

                # Populate the Listbox with folder names
                for folder in folders_available:
                    listbox.insert(tk.END, folder)

                # Select the first item by default
                if folders_available:
                    listbox.select_set(0)
                style = ttk.Style()
                # Configure the style
                style.configure("Red.TButton", background="red", foreground="red", font=("Arial", 8, "bold"))
                style_2 = ttk.Style()
                # Configure the style
                style_2.configure("Green.TButton", background="green", foreground="green", font=("Arial", 8, "bold"))
                style_3 = ttk.Style()
                # Configure the style
                style_3.configure("Orange.TButton", background="darkorange", foreground="darkorange", font=("Arial", 8, "bold"))

                buttons_frame = tk.Frame(root)
                buttons_frame.pack(pady=5)
                # Define buttons outside functions to manage their visibility
                open_files_button = ttk.Button(buttons_frame, text="Open", style="Green.TButton", command=lambda: open_file_selection())
                delete_files_button = ttk.Button(buttons_frame, text="Delete", style="Red.TButton", command=lambda: confirm_delete_folder())
                rename_files_button = ttk.Button(buttons_frame, text="Rename", style="Orange.TButton", command=lambda: confirm_rename_file())
                open_files_button.pack(side=tk.LEFT, padx=5)
                delete_files_button.pack(side=tk.LEFT, padx=20)
                rename_files_button.pack(side=tk.LEFT, padx=5)

                buttons_frame.pack(pady=10)
                back_button = ttk.Button(root, text="Back", command=lambda: back_folder())
                back_button.pack(pady=10)
                # Function to update the listbox with new contents
                def update_listbox(contents):
                    listbox.delete(0, tk.END)  # Clear the current listbox content
                    for item in folders_available:
                        listbox.insert(tk.END, item)
                    # Select the first item by default
                    if folders_available:
                        listbox.select_set(0)

                def show_file_selection(folder):
                    global path, current_path, back_btn_clicked, back_button, folders_available, selected_folder, ser, true_path
                    selected_folder = folder

                    back_button.pack_forget()
                    #print(f'pwd\n')
                    #time.sleep(0.5)
                    #dirct = self.read_Response_END()  # Call the function
                    #print(f"dirct: {dirct}")
                    #if dirct is None:
                        #messagebox.showwarning("Error!", "Response not received within the timeout.\nPlease retry / check hardware connection!")
                        #return  # Stop execution
                    #dirct = read_lines()
                    #decoded_lines = [line.decode('ascii').strip() for line in dirct]
                
                    if back_btn_clicked:
                        print(true_path)
                        true_path = current_path.split("/")
                        print(true_path)
                        true_path = true_path[:-2]
                        print(true_path)
                    
                        true_path = "/".join(filter(None, true_path))
                        directory = true_path
                        current_path = f"/{directory}/"
                        print(f"back_btn: {true_path}")
                        #########################################################
                        #########################################################
                        comport_is_active = interface_is_online(self.comport)
                        command = check_command(f"/{directory}/")
                        print(f"command: {command}")
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            if browse_file_for_HWUSB:
                                send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command}; (echo END) > /dev/null\n', 'ascii'))
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command}; (echo END) > /dev/null\n")
                            else:
                                send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode rtcm; (echo END) > /dev/null\n', 'ascii'))
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {command} --mode rtcm; (echo END) > /dev/null\n")
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   ls -l ; (echo END) > /dev/null\n')
                        # time.sleep(0.5)
                        else:
                            messagebox.showwarning("Warning", "Comport got disconnected")
                            root.destroy()
                            self.open_after_disconnection()
                            return
                        #lines = self.read_Response_END() 
                        #print(f'hicd\ncd {directory}\nls -l\n')
                        back_btn_clicked = False
                    else:
                        #dirct = decoded_lines[1]
                        #path = f'cd\ncd {dirct}/{selected_folder}/\nls -l\n'
                        current_path = f"{current_path}{selected_folder}/"
                        current_path_1 = check_command(current_path)
                        print(f"current_path: {current_path}")
                        comport_is_active = interface_is_online(self.comport)
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            if not (browse_file_for_HWUSB):
                                send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {current_path_1}; (echo END) > /dev/null\n', 'ascii'))
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {current_path_1}; (echo END) > /dev/null\n")
                            else:
                                send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {current_path_1} --mode rtcm; (echo END) > /dev/null\n', 'ascii'))
                                with open(file_path, 'a') as file:
                                    file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --dir {current_path_1} --mode rtcm; (echo END) > /dev/null\n")
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   ls -l ; (echo END) > /dev/null\n')
                        # time.sleep(0.5)
                        else:
                            messagebox.showwarning("Warning", "Comport got disconnected")
                            self.open_after_disconnection()
                            return
                        #print(f'hiicd\ncd {dirct}/{selected_folder}/\nls -l\n')
                    # time.sleep(0.5)
                    bs = self.read_Response_END()  # Call the function
                    bs = [line.decode('ascii').strip() for line in bs]
                    if bs is None:
                        messagebox.showwarning("Error!", "Response not received within the timeout.\nPlease retry / check hardware connection!")
                        return  # Stop execution
                                 
                    folders_names_1 = []
                    file_names_1 = []
                    folders_names_1, file_names_1 = extract_sections(bs)
                    # Example folder and file data
                    folders_available = folders_names_1 + file_names_1
                    print(folders_available)

                    back_button = ttk.Button(root, text="Back", command=lambda: back_folder())
                    back_button.pack(pady=5)
                    # Update the existing listbox with new contents
                    update_listbox(folders_available)
                    listbox.bind("<Double-1>", lambda event: open_file_selection())
                    # Update the current path label
                    current_path_label.config(text=f"Current Path: {current_path.strip()}")
                # Function to open file selection frame
                def open_file_selection():
                    global HW_file_path
                    global ser, filename_bin, back_from_nolog, gainfile_1, gainfile_2,proceed_button_nolog,back_to_files_nolog, bandwidth, Sampling_frequency, log_duration, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2
                    global col_title,label2,filename_bin, filename,params_table,params_table_2, proceed_button, back_to_files, response, decoded_lines, label1, filename_1
                    #global center_frequency_2, center_frequency, center_frequency_flag, center_frequency_flag_2, filename_1, bandwidth, bits_flags_2, bandwidth_2, back_to_files, Sampling_frequency,bandwidthflag_2,Sampling_frequency_flags_2, Sampling_frequency_2, bits_2 , log_duration, bits, bandwidthflag, Sampling_frequency_flags, log_durationflags, bits_flags, filename_1, total_bytes
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_item = listbox.get(selected_indices[0])
                        if str(selected_item).startswith("(d)"):
                            selected_item = str(selected_item).split("  ")[1]
                            show_file_selection(selected_item)
                        else:
                            if ".bin" in str(selected_item):
                                filename = str(str(selected_item).split(".bin")[0])
                            else:
                                HW_file_path = f"{current_path}{selected_item}/"
                                selected_proceed()

                            directory = current_path
                        
                            filename_2 = f'{filename}.log'
                            filename_bin = f'{filename}.bin'
                            if not browse_file_for_HWUSB:
                                commond = check_command(filename_2)
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active:
                                    send_command(bytearray(f'chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --mode contents --file {current_path}/{filename_2}; (echo END) > /dev/null\n', 'ascii'))
                                    with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   chmod +x /home/root/adc4bits/libiio/list_contents.sh; /home/root/adc4bits/libiio/list_contents.sh --mode contents --file {current_path}/{filename_2}; (echo END) > /dev/null\n")
                                    if Commands_file_user:
                                        #with open(file_path, 'a') as file:
                                            #file.write(f'\n{get_current_datetime()}   cat {commond} ; (echo END) > /dev/null\n')
                                        lines = self.read_Response_END()  # Call the function
                                        if lines is None:
                                            messagebox.showwarning("Error!", "Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                                            return
                                        decoded_lines = [line.decode() for line in lines]
                                        print(decoded_lines)
                                else:
                                    messagebox.showwarning("Warning", "COM port got disconnected!")
                                    root.destroy()
                                    self.open_after_disconnection()
                                    return
                                error_in_file_path = False
                                for line in decoded_lines:
                                    if "Error" in line:
                                        error_in_file_path = True
                                if not error_in_file_path:
                                        back_from_nolog = False
                                        # Disable listbox and buttons
                                        listbox.config(state=tk.DISABLED)
                                        open_files_button.config(state=tk.DISABLED)
                                        delete_files_button.config(state=tk.DISABLED)
                                        back_button.config(state=tk.DISABLED)

                                        label1 = tk.Label(root, text=f" File name: {filename} ", foreground="green")
                                        label1.pack(pady=10)
                                        
                                        def main(filename):
                                                global single_channel_rx1_replay, single_channel_rx2_replay, Dual_channel_replay
                                                global log_duration_2, center_frequency_2, reference_Frequency_log, filename_bin, gainfile_1, gainfile_2, center_frequency, center_frequency_flag, center_frequency_flag_2, filename_1, bandwidth, bits_flags_2, bandwidth_2, back_to_files, Sampling_frequency,bandwidthflag_2,Sampling_frequency_flags_2, Sampling_frequency_2, bits_2 , log_duration, bits, bandwidthflag, Sampling_frequency_flags, log_durationflags, bits_flags, filename_1, total_bytes
                                                filename = f'{filename}.log'
                                                
                                                filename_1 = filename.split(".log")[0]
                                                log_duration = ""
                                                center_frequency = ""
                                                center_frequency_2 = ""
                                                Sampling_frequency = ""
                                                Sampling_frequency_2 = ""
                                                bits = ""
                                                bits_2 = ""
                                                log_duration_2 = ""
                                                bandwidth = ""
                                                bandwidth_2 = ""
                                                gainfile_1 = ""
                                                gainfile_2 = ""
                                                reference_Frequency_log = ""
                                                mode_in_file = ""
                                                for line in decoded_lines:
                                                    if "LO1 " in line:
                                                        if "not found" in line:
                                                            center_frequency = "Not found"
                                                        else:
                                                            center_frequency = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "LO2 " in line:
                                                        if "not found" in line:
                                                            center_frequency_2 = "Not found"
                                                        else:
                                                            print(f"center_frequency_2: {line}")   
                                                            center_frequency_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "Bandwidth1 " in line:
                                                        if "not found" in line:  
                                                            bandwidth = "Not found"
                                                        else: 
                                                            bandwidth = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "Bandwidth2 " in line:
                                                        if "not found" in line:
                                                            bandwidth_2 = "Not found"
                                                        else:
                                                            bandwidth_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "fSamp1 " in line:
                                                        if "not found" in line:
                                                            Sampling_frequency = "Not found"    
                                                        else:
                                                            print(f"Sampling_frequency: {line}")
                                                            Sampling_frequency = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "fSamp2 " in line:
                                                        if "not found" in line:
                                                            Sampling_frequency_2 = "Not found"
                                                        else:
                                                            print(f"Sampling_frequency_2: {line}")
                                                            Sampling_frequency_2 = round((int(line.split(":")[-1].strip().split(" ")[0].strip())/ 1000000), 2)
                                                    elif "ADC Bits1 " in line:
                                                        if "not found" in line:
                                                            bits = "Not found"
                                                        else:
                                                            print(f"bits: {line}")
                                                            bits = line.split(":")[-1].strip().split(" ")[0].strip()
                                                    elif "ADC Bits2 " in line:
                                                        if "not found" in line:
                                                            bits_2 = "Not found"
                                                        else:
                                                            print(f"bits_2: {line}")
                                                            bits_2 = line.split(":")[-1].strip().split(" ")[0].strip()
                                                    elif "Total .bin File Size "  in line:
                                                        if "not found" in line:
                                                            total_bytes = "Not found"
                                                        else:
                                                            total_bytes = line.split(":")[-1].strip().split(" ")[0].strip()
                                                            total_bytes = math.floor(int(total_bytes)-512)
                                                    elif "Gain2 " in line:
                                                        if "not found" in line:
                                                            gainfile_2 = "Not found"
                                                        else:
                                                            gainfile_2 = str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                                    elif "Gain1 " in line:
                                                        if "not found" in line:
                                                            gainfile_1 = "Not found"
                                                        else:
                                                            gainfile_1 = str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                                    elif "Gain1 " in line: 
                                                        if not "not found" in line:
                                                            gainfile_2 =  str(line.split(":")[-1].strip().split(" ")[0].strip()).split(".")[0]
                                                        else:
                                                            gainfile_2 = "Not found"
                                                    elif "Mode " in line:
                                                        mode_in_file = int(line.split(":")[-1].strip())
                                                        
                                                if mode_in_file == "":
                                                    log_duration = "Not found"
                                                    log_duration_2 = "Not found"
                                                if mode_in_file == 0:
                                                    bytes_per_sample = ((int(bits)*2)/8)
                                                    bytes_per_second = bytes_per_sample*Sampling_frequency
                                                    log_duration = int((int(total_bytes) / int(bytes_per_second))/1000000)
                                                    log_duration_2 = "Not found"
                                                elif mode_in_file == 4:
                                                    bytes_per_sample = ((int(bits_2)*2)/8)
                                                    bytes_per_second = bytes_per_sample*Sampling_frequency_2
                                                    log_duration_2 = int((int(total_bytes) / int(bytes_per_second))/1000000)
                                                    log_duration = "Not found"
                                                elif mode_in_file == 2:
                                                    bytes_per_sample = ((int(bits_2)*2)/8)
                                                    bytes_per_second = bytes_per_sample*Sampling_frequency_2
                                                    log_duration_2 = int(int((int(total_bytes) / int(bytes_per_second))/1000000)/2)
                                                    log_duration = log_duration_2
                                                if reference_Frequency_log == "":
                                                    reference_Frequency_log = "Not found"

                                                update_gui(bandwidth, Sampling_frequency, log_duration, log_duration_2,  bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2, gainfile_1, gainfile_2)

                                        def update_gui(bandwidth, Sampling_frequency, log_duration, log_duration_2, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2, gainfile_1, gainfile_2):
                                            global Dual_channel_replay, single_channel_rx1_replay, single_channel_rx2_replay
                                            if center_frequency_2 and bits_2 == "Not found":
                                                Dual_channel_replay = False
                                                single_channel_rx2_replay = False
                                                single_channel_rx1_replay = True
                                            elif center_frequency and bits == "Not found":
                                                Dual_channel_replay = False
                                                single_channel_rx2_replay = True
                                                single_channel_rx1_replay = False
                                            else:
                                                Dual_channel_replay = True
                                                single_channel_rx2_replay = False
                                                single_channel_rx1_replay = False

                                            
                                            try:
                                                duration = second_to_hhmmss(log_duration)
                                            except:
                                                duration =  log_duration

                                            try:
                                                duration_2 = second_to_hhmmss(log_duration_2)
                                            except:
                                                duration_2 =  log_duration_2
                                            
                                            params_table.insert("", tk.END, values=("Center Freq (MHz)", center_frequency, center_frequency_2), tags=("oddrow",))
                                            params_table.insert("", tk.END, values=("#ADC Bits", bits, bits_2), tags=("evenrow",))
                                            params_table.insert("", tk.END, values=("Bandwidth (MHz)", bandwidth, bandwidth_2), tags=("oddrow",))
                                            params_table.insert("", tk.END, values=("Rx Gain (dB)", gainfile_1, gainfile_2), tags=("evenrow",))
                                            params_table.insert("", tk.END, values=("Sampling Freq (MHz)", Sampling_frequency, Sampling_frequency_2), tags=("oddrow",))
                                            params_table.insert("", tk.END, values=("Log Duration", duration, duration_2), tags=("evenrow",))
                                            params_table.insert("", tk.END, values=("Reference freq (MHZ)", reference_Frequency_log, reference_Frequency_log ), tags=("oddrow",))

                                        disable_and_hide_widgets()

                                        # Create a Treeview to display the parameters in a table with reduced size and alternating row colors
                                        columns = ("Parameter", "Value1", "Value2")
                                        params_table = ttk.Treeview(root, columns=columns, show="headings", height=7)
                                        params_table.heading("Parameter", text="Parameter")
                                        params_table.heading("Value1", text="Rx 1")
                                        params_table.heading("Value2", text="Rx 2")
                                        params_table.column("Parameter", anchor="w", width=70)
                                        params_table.column("Value1", anchor="w", width=70)
                                        params_table.column("Value2", anchor="w", width=70)

                                        params_table.pack(pady=(root.winfo_height() // 2 - params_table.winfo_height() // 2))
                                            
                                        # Apply styles for gridlines and alternating row colors
                                        style = ttk.Style()
                                        style.configure("Treeview", rowheight=45)
                                        style.map("Treeview", background=[("selected", "#ececec")], foreground=[("selected", "black")])
                                        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
                                        params_table.tag_configure("oddrow", background="lightgreen")
                                        params_table.tag_configure("evenrow", background="white")
                                        

                                        params_table.pack(fill="both", expand=False, padx=1, pady=1)

                                        proceed_button = ttk.Button(root, text="Proceed", command=selected_proceed)
                                        proceed_button.pack(pady=10)

                                        back_to_files = ttk.Button(root, text="Back", command=back_to_file)
                                        back_to_files.pack(pady=10)

                                        # Call the main function to process the file and update the GUI
                                        main(filename)
                                else:
                                    if not config_button:
                                        result = messagebox.askyesno('No .log found!', f'{filename}.log not found\nDo you want to continue the Replay?')
                                        if result:
                                                global checkbox1, checkbox2, label2, label3, frame, params_table_2
                                                back_from_nolog = True
                                                def toggle_checkbox1():
                                                    global label2, dual_channel_in_Replay
                                                    if checkbox_var1.get() == 1:
                                                        checkbox_var2.set(0)
                                                        dual_channel_in_Replay = False
                                                        # Update label text and make it visible
                                                        label2.config(text=f"Selected Channel: {col_title}")
                                                        label2.pack(pady=10)  # Ensure the label is packed (visible)
                                                    print("Checkbox 1 selected")

                                                def toggle_checkbox2():
                                                    global label2, dual_channel_in_Replay
                                                    if checkbox_var2.get() == 1:
                                                        dual_channel_in_Replay = True
                                                        checkbox_var1.set(0)
                                                        label2.config(text=f"Selected Channel: Rx 1 & Rx 2")
                                                        label2.pack(pady=10)  # Hide the label if "Dual Channel" is selected
                                                    print("Checkbox 2 selected")

                                                global params_table_2
                                                #if bandwidth is None:
                                                bandwidth = "Not found"
                                                #if Sampling_frequency is None:
                                                Sampling_frequency = "Not found"
                                                #if log_duration is None:
                                                log_duration = "Not found"
                                                #if bits is None:
                                                bits = "Not found"
                                                #if bandwidth_2 is None:
                                                bandwidth_2 = "Not found"
                                                #if Sampling_frequency_2 is None:
                                                Sampling_frequency_2 = "Not found"
                                            # if bits_2 is None:
                                                bits_2 = "Not found"
                                                #if center_frequency_2 is None:
                                                center_frequency_2 = "Not found"
                                                #if center_frequency is None:
                                                center_frequency = "Not found"
                                                log_duration_2 = "Not found"
                                                #update_gui(bandwidth, Sampling_frequency, log_duration, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2)                                     
                                                #function()
                                                #def update_gui(bandwidth, Sampling_frequency, log_duration, bits, bandwidth_2, Sampling_frequency_2, bits_2, center_frequency, center_frequency_2):
                                                if center_frequency_2 == "Not found":
                                                        log_duration_2 = "Not found"
                                                else:
                                                        log_duration_2 = log_duration
                                                    #params_table_2.insert("", tk.END, values=("Bits", bits), tags=("oddrow",))
                                                
                                                disable_and_hide_widgets()

                                                # Create a Treeview to display the parameters in a table with reduced size and alternating row colors
                                                columns = ("Parameter", "Value1", "Value2")
                                                params_table_2 = ttk.Treeview(root, columns=columns, show="headings", height=5)
                                                params_table_2.heading("Parameter", text="Parameter")
                                                params_table_2.heading("Value1", text="Rx 1")
                                                params_table_2.heading("Value2", text="Rx 2")
                                                params_table_2.column("Parameter", anchor="w", width=70)
                                                params_table_2.column("Value1", anchor="w", width=70)
                                                params_table_2.column("Value2", anchor="w", width=70)

                                                params_table_2.pack(pady=(root.winfo_height() // 2 - params_table_2.winfo_height() // 2))
                                                    
                                                # Apply styles for gridlines and alternating row colors
                                                style = ttk.Style()
                                                style.configure("Treeview", rowheight=45)
                                                style.map("Treeview", background=[("selected", "#ececec")], foreground=[("selected", "black")])
                                                style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
                                                params_table_2.tag_configure("oddrow", background="lightgreen")
                                                params_table_2.tag_configure("evenrow", background="white")
                                                
                                                params_table_2.pack(fill="both", expand=False, padx=1, pady=1)
                                                params_table_2.insert("", tk.END, values=("Center Freq (MHz)", center_frequency, center_frequency_2), tags=("oddrow",))
                                                params_table_2.insert("", tk.END, values=("#ADC Bits", bits, bits_2), tags=("evenrow",))
                                                params_table_2.insert("", tk.END, values=("Bandwidth (MHz)", bandwidth, bandwidth_2), tags=("oddrow",))
                                                #params_table_2.insert("", tk.END, values=("Rx Gain (dB)", gainfile_1, gainfile_2), tags=("evenrow",))
                                                params_table_2.insert("", tk.END, values=("Sampling Freq (MHz)", Sampling_frequency, Sampling_frequency_2), tags=("evenrow",))
                                                params_table_2.insert("", tk.END, values=("Log Duration", log_duration, log_duration_2), tags=("oddrow",))
                                                
                                                params_table_2.bind('<Double-1>', on_double_click)
                                                params_table_2.bind('<Button-1>', on_header_click)
                                                
                                                # Create a frame to hold the checkboxes
                                                frame = ttk.Frame(root, padding="5")
                                                frame.pack(padx=5, pady=5)

                                                # Variables to store the state of the checkboxes (0 or 1)
                                                checkbox_var1 = tk.IntVar(value=1)  # Set default value to 1 for the first checkbox
                                                checkbox_var2 = tk.IntVar()

                                                # Create Checkbuttons (checkboxes)
                                                checkbox1 = ttk.Checkbutton(frame, text="Single Channel", variable=checkbox_var1, command=toggle_checkbox1)
                                                checkbox2 = ttk.Checkbutton(frame, text="Dual Channel", variable=checkbox_var2, command=toggle_checkbox2)

                                                # Place the checkboxes in the frame beside each other using grid
                                                checkbox1.grid(row=0, column=0, padx=5, pady=5)
                                                checkbox2.grid(row=0, column=1, padx=5, pady=5)
                                                label2 = tk.Label(root, text=f"Selected Channel: {col_title}", foreground="green", font=("Arial", 12, "bold"))
                                                label2.pack(pady=5) 

                                                label3 = tk.Label(root, text=f" File name: {filename} ", foreground="green")
                                                label3.pack(pady=5)

                                                proceed_button_nolog = ttk.Button(root, text="Proceed", command=selected_proceed_nolog)
                                                proceed_button_nolog.pack(pady=10)

                                                back_to_files_nolog = ttk.Button(root, text="Back", command=back_to_file)
                                                back_to_files_nolog.pack(pady=10)
                                    else:
                                        log_duration = ""
                                        msg_box_compare = QMessageBox()
                                        msg_box_compare.setWindowTitle(".log file error")
                                        #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                                        msg_box_compare.setInformativeText(".log file not found!, Do you want to Continue?")
                                        msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                        msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                        msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                        msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                        reply_3 = msg_box_compare.exec()
                                        if reply_3 == QMessageBox.StandardButton.Yes:
                                            filename
                                            selected_proceed()
                                            print("Logging within available memory...")
                                        else:
                                            print("Logging not performed.") 
                                    
                    else:
                        messagebox.showwarning("Warning", "Please select the Folder! / The Folder is empty!")

                def on_header_click(event):
                    global col, label2, col_title
                    if not dual_channel_in_Replay:
                        region = params_table_2.identify_region(event.x, event.y)
                        if region == 'heading':
                            # Get the column index from the header click event
                            col = params_table_2.identify_column(event.x)
                            print(col)
                            if col:
                                col_index = int(col[1:]) - 1  # Column index is 0-based
                                col_title = params_table_2.heading(col)["text"]
                                print(f"Column title clicked: {col_title}")
                                if label2:
                                    label2.config(text=f"Selected Channel: {col_title}")
                                
                                style.configure(f"Treeview.Heading.{col}", background="red")

                def on_double_click(event):
                    # Get the region where the click occurred
                    region = params_table_2.identify_region(event.x, event.y)
                    if region == 'cell':
                        row_id = params_table_2.identify_row(event.y)  # Get the clicked row
                        column = params_table_2.identify_column(event.x)  # Get the clicked column

                        # Prevent editing the first column ("Parameter")
                        if column == "#1":  # '#1' corresponds to the first column
                            return  # Block editing for the first column
                        if not dual_channel_in_Replay:
                            if column == col:
                            # Get the current value of the clicked cell
                                current_value = params_table_2.item(row_id, "values")[int(column[1]) - 1]
                                
                                # Place an entry widget over the cell
                                x, y, width, height = params_table_2.bbox(row_id, column)
                                entry = ttk.Entry(root)
                                entry.place(x=x, y=y, width=width, height=height)
                                entry.insert(0, current_value)
                                entry.focus()

                                def save_edit(event):
                                    # Get the new value entered in the entry
                                    new_value = entry.get()
                                    current_values = list(params_table_2.item(row_id, "values"))
                                    current_values[int(column[1]) - 1] = new_value
                                    params_table_2.item(row_id, values=current_values)  # Update the Treeview with the new value
                                    entry.destroy()  # Remove the entry widget

                                # Bind "Enter" key press to save the edit
                                entry.bind('<Return>', save_edit)
                                entry.bind('<FocusOut>', lambda event: entry.destroy())
                        else:
                            current_value = params_table_2.item(row_id, "values")[int(column[1]) - 1]
                                
                            # Place an entry widget over the cell
                            x, y, width, height = params_table_2.bbox(row_id, column)
                            entry = ttk.Entry(root)
                            entry.place(x=x, y=y, width=width, height=height)
                            entry.insert(0, current_value)
                            entry.focus()

                            def save_edit(event):
                                    # Get the new value entered in the entry
                                    new_value = entry.get()
                                    current_values = list(params_table_2.item(row_id, "values"))
                                    current_values[int(column[1]) - 1] = new_value
                                    params_table_2.item(row_id, values=current_values)  # Update the Treeview with the new value
                                    entry.destroy()  # Remove the entry widget

                            # Bind "Enter" key press to save the edit
                            entry.bind('<Return>', save_edit)
                            entry.bind('<FocusOut>', lambda event: entry.destroy())
                             
                def back_to_file():
                    global current_path, back_from_nolog
                    #current_path = f"{str(current_path)}/remove/"
                    # Show the Listbox and Buttons again
                    if back_from_nolog:
                        back_from_nolog = False
                        checkbox1.pack_forget()
                        checkbox2.pack_forget()
                        frame.pack_forget()
                        label3.pack_forget()
                        label2.pack_forget()
                        params_table_2.pack_forget()
                        proceed_button_nolog.pack_forget()
                        back_to_files_nolog.pack_forget()
                    else:
                        params_table.pack_forget()
                        label1.pack_forget()
                        back_to_files.pack_forget()
                        proceed_button.pack_forget()

                    current_path_label.pack(pady=5)
                    main_frame.pack(pady=5)
                    v_scrollbar.pack(pady=5)
                    h_scrollbar.pack(pady=5)
                    listbox.pack(pady=5)
                    buttons_frame.pack(pady=5)
                    #open_files_button.pack(pady=5)
                    #delete_files_button.pack(pady=5)
                    back_button.pack(pady=5)
                    listbox.config(state=tk.NORMAL)
                    open_files_button.config(state=tk.NORMAL)
                    delete_files_button.config(state=tk.NORMAL)
                    back_button.config(state=tk.NORMAL) 

                def selected_proceed_nolog():
                    global refile, browse_files, current_path, ser, nolog_high, single_channel_rx1_replay, single_channel_rx2_replay, Dual_channel_replay
                    global rx2_sf,rx1_adc, rx1_bw, rx1_cf, rx1_duration, rx1_sf, rx2_adc, rx2_bw, rx2_cf, rx2_duration, filename_bin, rx1_gain, rx2_gain
                    print(filename_bin)
                    # Retrieve and print the contents of the Treeview table
                    for child in params_table_2.get_children():
                        row_values = params_table_2.item(child, 'values')
                        #print(row_values)
                        if "Center Freq (MHz)" in row_values:
                            rx1_cf = list(row_values)[1]
                            print(rx1_cf)
                            rx2_cf = list(row_values)[2]
                            print(rx2_cf)
                        if "#ADC Bits" in row_values:
                            rx1_adc = list(row_values)[1]
                            print(rx1_adc)
                            rx2_adc = list(row_values)[2]
                            print(rx2_adc)
                        if "Bandwidth (MHz)" in row_values:
                            rx1_bw = list(row_values)[1]
                            print(rx1_bw)
                            rx2_bw = list(row_values)[2]
                            print(rx2_bw)
                        if "Sampling Freq (MHz)" in row_values:
                            rx1_sf = list(row_values)[1]
                            print(rx1_sf)
                            rx2_sf = list(row_values)[2]
                            print(rx2_sf)
                        if "Log Duration" in row_values:
                            rx1_duration = list(row_values)[1]
                            print(rx1_duration)
                            print(type(rx1_duration))
                            rx2_duration = list(row_values)[2]
                            print(rx2_duration)
                        """if "Rx Gain (dB)" in row_values:
                            rx1_gain = list(row_values)[1]
                            print(rx1_gain)
                            rx2_gain = list(row_values)[2]
                            print(rx2_gain)"""
                    if not dual_channel_in_Replay:
                        if col_title == "Rx 1":
                            single_channel_rx1_replay = True
                            single_channel_rx2_replay = False
                            Dual_channel_replay = False
                            if single_channel_rx1_replay or single_channel_rx2_replay:
                                        if self.radioButton_single.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in dual channel, since you have selected single channel!")
                                            return
                            elif Dual_channel_replay:
                                        if self.radioButton_double.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in single channel,  since you have selected dual channel!")
                                            return
                            if (rx1_adc or rx1_bw or rx1_cf or rx1_sf or rx1_duration) == "Not found":
                                messagebox.showwarning("Error!", "Please enter all the details of Rx 1!")
                                return
                            else:
                                pass
                            try:
                                rx1_adc = int(rx1_adc)
                                rx1_bw = float(rx1_bw)
                                rx1_cf = float(rx1_cf)
                                rx1_sf = float(rx1_sf)
                                #rx1_gain = float(rx1_gain)
                            except ValueError:
                                messagebox.showwarning("Error!", "Please enter valid values  for ADC bits, Bandwidth, Center frequency, Sampling frequency, Gain")
                                return
                            if int(rx1_adc) not in [4, 8, 16]:
                                messagebox.showwarning("Error!", "Please Valid ADC bit!")
                                return
                            """if rx1_gain >= 0 or rx1_gain <= -89.5:
                                messagebox.showwarning("Error!", "Gain should be between 0 to -89")
                                return"""
                            rx1_duration = validate_time(rx1_duration)
                            if rx1_duration == None:
                                msg_box_error = QMessageBox()
                                msg_box_error.setWindowTitle("Invalid Format")
                                msg_box_error.setText("Duration value is in a wrong format")
                                msg_box_error.exec()
                                return
                            
                            if int(rx1_adc) == 4 and not float(rx1_bw) <= (0.9*61.44) and not float(rx1_sf) <= (61.44):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*61.44}MHz and {61.44}MHZ respectively")
                                return  
                            if int(rx1_adc) == 8 and not float(rx1_bw) <= (0.9*48) and not float(rx1_sf) <= (48):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*48}MHz and {48}MHZ respectively")
                                return
                            if int(rx1_adc) == 16 and not float(rx1_bw) <= (0.9*24) and not float(rx1_sf) <= (24):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*24}MHz and {24}MHZ respectively")
                                return
                            
                            if float(rx1_sf) <= float(rx1_bw):
                                result = messagebox.askyesno("Warning!", f"Sampling frequency {rx1_sf} is not greater than Bandwidth {rx1_bw}\nDo you want to continue?")
                                if result:
                                    pass
                                else:
                                    return
                            
                            

                            lo_value_1 = check_value_lo(rx1_cf)
                            if lo_value_1 == None:
                                msg_box_error_1 = QMessageBox()
                                msg_box_error_1.setWindowTitle("Invalid Data")
                                msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                                msg_box_error_1.exec()
                                return
                            ########################################################################################################################
                            directory = current_path
                            command = check_command(directory)
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                send_command(bytearray(f'cd {command}\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd {command}\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                send_command(bytearray(f'ls -l\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   ls -l\n')
                                response_1 = read_lines()
                                decoded_lines_1 = [line.decode() for line in response_1]
                                print(decoded_lines_1)
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return         
                            
                            for line in decoded_lines_1:
                                if filename_bin in line:
                                    total_bytes = str(line.split("root root")[1].strip()).split(" ")[0]
                                    total_bytes = int(total_bytes)-512
                            bytes_per_sample = ((int(rx1_adc)*2)/8)
                            print(bytes_per_sample)
                            bytes_per_second = bytes_per_sample*rx1_sf
                            print(bytes_per_second)
                            total_duration = int((int(total_bytes) / int(bytes_per_second))/1000000)

                            log_duration = second_to_hhmmss(total_duration)
                            ###############################################################################################################################
                            if not str(log_duration) == str(rx1_duration):
                                #messagebox.showwarning("Error!", f"Entered Duration does not match with the computed duration {log_duration}")
                                msg_box_compare = QMessageBox()
                                msg_box_compare.setWindowTitle("Warning")
                                #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                                msg_box_compare.setInformativeText(f"Entered Duration does not match with the computed duration {log_duration}\nDo you want to continue")
                                msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                reply_3 = msg_box_compare.exec()
                                # Check the user's choice
                                if reply_3 == QMessageBox.StandardButton.Yes:
                                    string = compare_times(str(log_duration), str(rx1_duration))
                                    if "earlier" in string:
                                         rx1_duration = log_duration
                                    else:
                                         rx1_duration = rx1_duration
                                else:
                                    return
                        ############################################################  Rx 2 ##########################################################################    
                        if col_title == "Rx 2":
                            single_channel_rx1_replay = False
                            single_channel_rx2_replay = True
                            Dual_channel_replay = False
                            if single_channel_rx1_replay or single_channel_rx2_replay:
                                        if self.radioButton_single.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in dual channel,  since you have selected single channel!")
                                            return
                            elif Dual_channel_replay:
                                        if self.radioButton_double.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in single channel,  since you have selected dual channel!")
                                            return
                            if (rx2_adc or rx2_bw or rx2_cf or rx2_sf or rx2_duration) == "Not found":
                                messagebox.showwarning("Error!", "Please enter all the details of Rx 2!")
                                return
                            try:
                                rx2_adc = int(rx2_adc)
                                rx2_bw = float(rx2_bw)
                                rx2_cf = float(rx2_cf)
                                rx2_sf = float(rx2_sf)
                                #rx2_gain = float(rx2_gain)
                            except ValueError:
                                messagebox.showwarning("Error!", "Please enter valid values  for ADC bits, Bandwidth, Center frequency, Sampling frequency, Gain")
                                return
                            """if rx2_gain >= 0 or rx2_gain <= -89.5:
                                messagebox.showwarning("Error!", "Gain should be between 0 to -89")
                                return"""
                            if int(rx2_adc) not in [4, 8, 16]:
                                messagebox.showwarning("Error!", "Please Valid ADC bit!")
                                return
                            rx2_duration = validate_time(rx2_duration)
                            if rx2_duration == None:
                                msg_box_error = QMessageBox()
                                msg_box_error.setWindowTitle("Invalid Format")
                                msg_box_error.setText("Duration value is in a wrong format")
                                msg_box_error.exec()
                                return
                            
                            if int(rx2_adc) == 4 and not float(rx2_bw) <= (0.9*61.44) and not float(rx2_sf) <= (61.44):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*61.44}MHz and {61.44}MHZ respectively")
                                return  
                            if int(rx2_adc) == 8 and not float(rx2_bw) <= (0.9*48) and not float(rx2_sf) <= (48):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*48}MHz and {48}MHZ respectively")
                                return
                            if int(rx2_adc) == 16 and not float(rx2_bw) <= (0.9*24) and not float(rx2_sf) <= (24):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {0.9*24}MHz and {24}MHZ respectively")
                                return
                            
                            if float(rx2_sf) <= float(rx2_bw):
                                result = messagebox.askyesno("Warning!", f"Sampling frequency {rx2_sf} is not greater than Bandwidth {rx2_bw}\nDo you want to continue?")
                                if result:
                                    pass
                                else:
                                    return
                            
                            lo_value_2 = check_value_lo(rx2_cf)
                            if lo_value_2 == None:
                                msg_box_error_1 = QMessageBox()
                                msg_box_error_1.setWindowTitle("Invalid Data")
                                msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                                msg_box_error_1.exec()
                                return
                            ########################################################################################################################
                            directory = current_path
                            comport_is_active = interface_is_online(self.comport)
                            command = check_command(directory)
                            if comport_is_active: 
                                send_command(bytearray(f'cd {command}\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd {command}\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                send_command(bytearray(f'ls -l\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   ls -l\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            response_1 = read_lines()
                            decoded_lines_1 = [line.decode() for line in response_1]
                            for line in decoded_lines_1:
                                if filename_bin in line:
                                    total_bytes = str(line.split("root root")[1].strip()).split(" ")[0]
                                    total_bytes = int(total_bytes)-512
                            bytes_per_sample = ((int(rx1_adc)*2)/8)
                            print(bytes_per_sample)
                            bytes_per_second = bytes_per_sample*rx1_sf
                            print(bytes_per_second)
                            total_duration = int((int(total_bytes) / int(bytes_per_second))/1000000)
                            log_duration = second_to_hhmmss(total_duration)
                            ###############################################################################################################################
                            if not str(log_duration) == str(rx2_duration):
                                #messagebox.showwarning("Error!", f"Entered Duration does not match with the computed duration {log_duration}")
                                msg_box_compare = QMessageBox()
                                msg_box_compare.setWindowTitle("Warning")
                                #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                                msg_box_compare.setInformativeText(f"Entered Duration does not match with the computed duration {log_duration}\nDo you want to continue")
                                msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                reply_3 = msg_box_compare.exec()
                                # Check the user's choice
                                if reply_3 == QMessageBox.StandardButton.Yes:
                                    string = compare_times(str(log_duration), str(rx1_duration))
                                    if "earlier" in string:
                                         rx1_duration = log_duration
                                    else:
                                         rx1_duration = rx1_duration
                                else:
                                    return
                    ############################################################  Dual channel  ####################################################################
                    else:
                            single_channel_rx1_replay = False
                            single_channel_rx2_replay = False
                            Dual_channel_replay = True
                            if single_channel_rx1_replay or single_channel_rx2_replay:
                                        if self.radioButton_single.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in dual channel, since you have selected single channel!")
                                            return
                            elif Dual_channel_replay:
                                        if self.radioButton_double.isChecked():
                                            pass
                                        else:
                                            messagebox.showwarning("Warning", "You cannot Replay a file in single channel, since you have selected dual channel!")
                                            return
                            if (rx1_adc or rx1_bw or rx1_cf or rx1_sf or rx1_duration) == "Not found":
                                messagebox.showwarning("Error!", "Please enter all the details of Rx 1!")
                                return
                            if (rx2_adc or rx2_bw or rx2_cf or rx2_sf or rx2_duration) == "Not found":
                                messagebox.showwarning("Error!", "Please enter all the details of Rx 2!")
                                return
                            try:
                                rx1_adc = int(rx1_adc)
                                rx1_bw = float(rx1_bw)
                                rx1_cf = float(rx1_cf)
                                rx1_sf = float(rx1_sf)
                                rx2_adc = int(rx2_adc)
                                #rx1_gain = float(rx1_gain)
                                #rx2_gain = float(rx2_gain)
                                rx2_bw = float(rx2_bw)
                                rx2_cf = float(rx2_cf)
                                rx2_sf = float(rx2_sf)
                                
                            except ValueError:
                                messagebox.showwarning("Error!", "Please enter valid values  for ADC bits, Bandwidth, Center frequency, Sampling frequency")
                                return
                            """if rx2_gain >= 0 or rx2_gain <= -89.5:
                                messagebox.showwarning("Error!", "Gain should be between 0 to -89")
                                return
                            if rx1_gain >= 0 or rx1_gain <= -89.5:
                                messagebox.showwarning("Error!", "Gain should be between 0 to -89")
                                return"""
                            if int(rx1_adc) not in [4, 8, 16]:
                                messagebox.showwarning("Error!", "Please Valid ADC bit!")
                                return
                            if int(rx2_adc) not in [4, 8, 16]:
                                messagebox.showwarning("Error!", "Please Valid ADC bit!")
                                return
                            rx1_duration = validate_time(rx1_duration)
                            if rx1_duration == None:
                                msg_box_error = QMessageBox()
                                msg_box_error.setWindowTitle("Invalid Format")
                                msg_box_error.setText("Duration value is in a wrong format")
                                msg_box_error.exec()
                                return
                            print(rx1_adc)
                            print(rx2_adc)
                            if self.reference_frequency == "0":
                                if not float(rx1_cf) == float(rx2_cf):
                                    messagebox.showwarning("Error!", f"Lo of Rx 1 and RX 2 are not equal")
                                    return
                            if not int(rx1_adc) == int(rx2_adc):
                                messagebox.showwarning("Error!", f"ADC bits of Rx 1 and RX 2 are not equal")
                                return
                            if not float(rx1_sf) == float(rx2_sf):
                                messagebox.showwarning("Error!", f"Sampling frequency of Rx 1 and RX 2 are not equal")
                                return 
                            if int(rx1_adc) == 4 and not float(rx1_bw) <= ((0.9*61.44)/2) and not float(rx1_sf) <= ((61.44)/2):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {(0.9*61.44)/2}MHz and {(61.44)/2}MHZ respectively")
                                return  
                            if int(rx1_adc) == 8 and not float(rx1_bw) <= ((0.9*48)/2) and not float(rx1_sf) <= ((48)/2):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {(0.9*48)/2}MHz and {(48)/2}MHZ respectively")
                                return
                            if int(rx1_adc) == 16 and not float(rx1_bw) <= ((0.9*24)/2) and not float(rx1_sf) <= ((24)/2):
                                messagebox.showwarning("Error!", f"Bandwidth and Sampling frequency should not be greater than {(0.9*24)/2}MHz and {(24)/2}MHZ respectively")
                                return
                            
                            if float(rx1_sf) <= float(rx1_bw):
                                result = messagebox.askyesno("Warning!", f"Sampling frequency {rx1_sf} is not greater than Bandwidth {rx1_bw}\nDo you want to continue?")
                                if result:
                                    pass
                                else:
                                    return
                            
                            if float(rx2_sf) <= float(rx2_bw):
                                result = messagebox.askyesno("Warning!", f"Sampling frequency {rx2_sf} is not greater than Bandwidth {rx2_bw}\nDo you want to continue?")
                                if result:
                                    pass
                                else:
                                    return
                            
                            lo_value_1 = check_value_lo(rx1_cf)
                            if lo_value_1 == None:
                                msg_box_error_1 = QMessageBox()
                                msg_box_error_1.setWindowTitle("Invalid Data")
                                msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                                msg_box_error_1.exec()
                                return
                            
                            lo_value_2 = check_value_lo(rx2_cf)
                            if lo_value_2 == None:
                                msg_box_error_1 = QMessageBox()
                                msg_box_error_1.setWindowTitle("Invalid Data")
                                msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                                msg_box_error_1.exec()
                                return
                            ########################################################################################################################
                            directory = current_path
                            comport_is_active = interface_is_online(self.comport)
                            command = check_command(directory)
                            if comport_is_active: 
                                send_command(bytearray(f'cd {command}\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd {command}\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            comport_is_active = interface_is_online(self.comport)
                            if comport_is_active: 
                                send_command(bytearray(f'ls -l\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   ls -l\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            response_1 = read_lines()
                            decoded_lines_1 = [line.decode() for line in response_1]
                            for line in decoded_lines_1:
                                if filename_bin in line:
                                    total_bytes = str(line.split("root root")[1].strip()).split(" ")[0]
                                    total_bytes = int(total_bytes)-512
                            bytes_per_sample = ((int(rx1_adc)*2)/8)
                            print(bytes_per_sample)
                            bytes_per_second = bytes_per_sample*rx1_sf
                            print(bytes_per_second)
                            total_duration = int((int(total_bytes) / int(bytes_per_second))/1000000)
                            total_duration = math.floor(total_duration/2)
                            log_duration = second_to_hhmmss(total_duration)
                            ###############################################################################################################################
                            if not str(log_duration) == str(rx1_duration):
                                #messagebox.showwarning("Error!", f"Entered Duration does not match with the computed duration {log_duration}")
                                msg_box_compare = QMessageBox()
                                msg_box_compare.setWindowTitle("Warning")
                                #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                                msg_box_compare.setInformativeText(f"Entered Duration does not match with the computed duration {log_duration}\nDo you want to continue")
                                msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                                msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                                msg_box_compare.addButton(QMessageBox.StandardButton.No)
                                msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                                reply_3 = msg_box_compare.exec()
                                # Check the user's choice
                                if reply_3 == QMessageBox.StandardButton.Yes:
                                    string = compare_times(str(log_duration), str(rx1_duration))
                                    if "earlier" in string:
                                         rx1_duration = log_duration
                                    else:
                                         rx1_duration = rx1_duration
                                else:
                                    return
                    ###############################################################################################################################################    
                    print("proceed")     
                    # Load the SVG file using QSvgRenderer
                    svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                    # Create a QPixmap and render the SVG onto it
                    pixmap = QPixmap(45, 45)  # Set the size of the icon
                    pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                    # Use QPainter to render the SVG on the QPixmap
                    painter = QPainter(pixmap)
                    svg_renderer.render(painter)
                    painter.end()
                    # Set the rendered SVG as the icon for the QPushButton
                    icon = QIcon(pixmap)
                    self.pushButton_8.setIcon(icon)
                    self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size   
                    global Lg_path
                    Lg_path = current_path
                    if single_channel_rx1_replay or single_channel_rx2_replay:
                                if self.radioButton_single.isChecked():
                                     pass
                                else:
                                     messagebox.showwarning("Warning", "You cannot Replay a file in dual channel, which is recorded using single channel!")
                                     return
                    elif Dual_channel_replay:
                                if self.radioButton_double.isChecked():
                                     pass
                                else:
                                     messagebox.showwarning("Warning", "You cannot Replay a file in single channel, which is recorded using dual channel!")
                                     return
                    refile = True
                    browse_files = False
                    nolog_high = True
                    self.pushButton_7.setEnabled(True)
                    self.pushButton_6.setEnabled(True)
                    self.pushButton_login.setEnabled(True)
                    self.pushButton_2.setEnabled(True)
                    self.pushButton_4.setEnabled(True)
                    self.pushButton_5.setEnabled(True)
                    self.pushButton_select_file.setEnabled(True)
                    self.start_time_value = None
                    self.lineEdit_7.setText("")
                    self.lineEdit_replay.clear()
                    self.stop_time_value = None
                    self.lineEdit_8.setText("")
                    if show_path_btn_active_replay:
                        self.lineEdit9.setText(filename)
                    else:
                        self.lineEdit9.setText(Lg_path)
                    root.destroy()
#################################################################################################################################################################################
                def selected_proceed():
                    global refile, browse_files, current_path, ser, read_selected_file_path, filename, nolog_high
                    if browse_file_for_HWUSB:
                        refile = True
                        browse_files = False
                        nolog_high = False
                        self.pushButton_7.setEnabled(True)
                        self.pushButton_6.setEnabled(True)
                        self.pushButton_login.setEnabled(True)
                        self.pushButton_2.setEnabled(True)
                        self.pushButton_4.setEnabled(True)
                        self.pushButton_5.setEnabled(True)
                        self.pushButton_select_file.setEnabled(True)
                        self.start_time_value = None
                        self.lineEdit_7.setText("")
                        self.lineEdit_replay.clear()
                        self.stop_time_value = None
                        self.lineEdit_8.setText("")
                        root.destroy()
                        return
                    if not log_duration == "Not found" or not log_duration_2 == "Not found":
                        global Lg_path
                        Lg_path = current_path
                        if not config_button:
                            if single_channel_rx1_replay or single_channel_rx2_replay:
                                if self.radioButton_single.isChecked():
                                     pass
                                else:
                                     messagebox.showwarning("Warning", "You cannot Replay a file in dual channel, which is recorded using single channel!")
                                     return
                            elif Dual_channel_replay:
                                if self.radioButton_double.isChecked():
                                     pass
                                else:
                                     messagebox.showwarning("Warning", "You cannot Replay a file in single channel, which is recorded using dual channel!")
                                     return
                            refile = True
                            browse_files = False
                            # Load the SVG file using QSvgRenderer
                            svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                            # Create a QPixmap and render the SVG onto it
                            pixmap = QPixmap(45, 45)  # Set the size of the icon
                            pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                            # Use QPainter to render the SVG on the QPixmap
                            painter = QPainter(pixmap)
                            svg_renderer.render(painter)
                            painter.end()
                            # Set the rendered SVG as the icon for the QPushButton
                            icon = QIcon(pixmap)
                            self.pushButton_8.setIcon(icon)
                            self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size
                            self.pushButton_7.setEnabled(True)
                            self.pushButton_6.setEnabled(True)
                            self.pushButton_login.setEnabled(True)
                            self.pushButton_2.setEnabled(True)
                            self.pushButton_4.setEnabled(True)
                            self.pushButton_5.setEnabled(True)
                            self.pushButton_select_file.setEnabled(True)
                            self.start_time_value = None
                            self.lineEdit_7.setText("")
                            self.lineEdit_replay.clear()
                            self.stop_time_value = None
                            self.lineEdit_8.setText("")


                            if show_path_btn_active_replay:
                                self.lineEdit9.setText(filename)
                            else:
                                self.lineEdit9.setText(Lg_path)

                            nolog_high = False
                            root.destroy()
                        elif config_button:
                            global selected_files_paths
                            if not filename in self.variable_names:
                                self.variable_names.append(filename)

                                print(self.variable_names)

                                self.populate_table()

                                directory = read_selected_file_path
                                comport_is_active = interface_is_online(self.comport)
                                command = check_command(directory)
                                if comport_is_active: 
                                    send_command(bytearray(f'cd {command}\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   cd {command}\n')
                                else:
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                comport_is_active = interface_is_online(self.comport)
                                selected_file_actual = check_command(filename_txt)
                                if comport_is_active: 
                                    send_command(bytearray(f'cat {selected_file_actual}\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   cat {selected_file_actual}\n')
                                else:
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                lines = read_lines()
                                print(lines)
                                decoded_lines = [line.decode() for line in lines]
                                for line in decoded_lines:
                                    print(line)
                                
                                selected_files_paths.append(f"{current_path}{filename}")
                                new_lines = f"selected_files: {current_path}{filename}"
                                #print(new_lines)
                                comport_is_active = interface_is_online(self.comport)
                                command = check_command(directory)
                                if comport_is_active: 
                                    send_command(bytearray(f'cd {command}\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   cd {command}\n')
                                else:
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                comport_is_active = interface_is_online(self.comport)
                                
                                if comport_is_active: 
                                    send_command(bytearray(f'echo "{new_lines}">>{filename_txt}\n', 'ascii'))
                                    if Commands_file_user:
                                        with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   echo "{new_lines}">>{filename_txt}\n')
                                else:
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"COM port got disconnected!, Could not proceed!")
                                    msg_box_11.exec()
                                    self.open_after_disconnection()
                                    return
                                if len(self.variable_names) >= 4:
                                    refile = True
                                    browse_files = False
                                    # Load the SVG file using QSvgRenderer
                                    svg_renderer = QSvgRenderer("NEW_FILE.svg")  # Replace with your SVG image path
                                    # Create a QPixmap and render the SVG onto it
                                    pixmap = QPixmap(45, 45)  # Set the size of the icon
                                    pixmap.fill(QtCore.Qt.GlobalColor.transparent)  # Make the pixmap background transparent
                                    # Use QPainter to render the SVG on the QPixmap
                                    painter = QPainter(pixmap)
                                    svg_renderer.render(painter)
                                    painter.end()
                                    # Set the rendered SVG as the icon for the QPushButton
                                    icon = QIcon(pixmap)
                                    self.pushButton_8.setIcon(icon)
                                    self.pushButton_8.setIconSize(QSize(30, 30))  # Set icon size
                                    self.pushButton_7.setEnabled(True)
                                    self.pushButton_6.setEnabled(True)
                                    self.pushButton_login.setEnabled(True)
                                    self.pushButton_2.setEnabled(True)
                                    self.pushButton_4.setEnabled(True)
                                    self.pushButton_5.setEnabled(True)
                                    self.pushButton_select_file.setEnabled(True)
                                    self.start_time_value = None
                                    self.lineEdit_7.setText("")
                                    self.lineEdit_replay.clear()
                                    self.stop_time_value = None
                                    self.lineEdit_8.setText("")
                                    root.destroy()
                            else:
                                messagebox.showwarning("Error!", "You have already selected this file!")
                    else:
                        messagebox.showwarning("Error!", "You cannot proceed! Duration is not found!")

                def disable_and_hide_widgets():
                    # Hide the Listbox and Buttons
                    listbox.pack_forget()
                    back_button.pack_forget()
                    current_path_label.pack_forget()
                    #scrollbar.pack_forget()
                    main_frame.pack_forget()
                    buttons_frame.pack_forget()

                def back_folder():
                    global true_path
                    true_path = current_path
                    print(f"true path: {true_path}")
                    determine_path = current_path.split("/")
                    determine_path = "/".join(determine_path[:-1])
                    if base_path in str(determine_path):
                        global back_btn_clicked
                        back_btn_clicked = True
                        selected_indices = listbox.curselection()
                        if selected_indices:
                            selected_item = listbox.get(selected_indices[0])
                            show_file_selection(selected_item)
                        else:
                            selected_item = ""
                            show_file_selection(selected_item)
                    else:
                        messagebox.showwarning("Warning", "You cannot move back from here!")

                # Function to confirm folder deletion
                def confirm_rename_file():
                    global ser
                    print(current_path)
                    listbox_items = listbox.get(0, tk.END)
                    print(listbox_items)
                    print(f"current path {current_path}")
                    selected_indices = listbox.curselection()
                    if selected_indices:
                        selected_folder = listbox.get(selected_indices[0])
                        print(selected_folder)
                        test = current_path.split("/")
                        print(len(test))
                        if len(test) <= 4:
                            messagebox.showwarning("Warning", "You cannot rename this folder!")
                            return
                        if str(selected_folder).startswith("(d)"):
                            # Ask the user for the new folder name
                            new_folder_name = simpledialog.askstring("Rename Folder", "Enter the new folder name:")
                            if new_folder_name == "":
                                messagebox.showwarning("Invalid Name", "No new folder name provided.")
                                return
                            if new_folder_name in listbox_items and not new_folder_name == selected_folder:
                                messagebox.showwarning("Invalid Name", "A folder with this name already exists.")
                                return
                            if new_folder_name == selected_folder:
                                messagebox.showwarning("No changes!", "The entered name is the same as the selected folder.")
                                return
                            if new_folder_name:
                                # If a new name is provided, proceed with renaming
                                result = messagebox.askyesno("Rename Folder", f"Are you sure you want to rename the folder '{selected_folder}' to '{new_folder_name}'?")
                                if result:
                                    folders_available.remove(selected_folder)
                                    folders_available.append(new_folder_name)
                                    listbox.delete(selected_indices[0])
                                    listbox.insert(selected_indices[0], f"(d)  {new_folder_name}")
                                    new_folder_name = str(new_folder_name).split("(d)  ")[-1].strip()
                                    print(new_folder_name)
                                    selected_folder = str(selected_folder).split("(d)  ")[-1].strip()

                                    # Execute the rename command
                                    comport_is_active = interface_is_online(self.comport)
                                    if comport_is_active:
                                        # Use the 'mv' command for renaming
                                        send_command(bytearray(f'mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}"\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}"\n')
                                    else:
                                        messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                        root.destroy()
                                        self.open_after_disconnection()
                                        return

                                    # Check the file system (optional, based on your needs)
                                    print(fs_system)

                                    ########################################################################
                                    if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True, destroy_root=True):
                                        return
                                    ########################################################################
                                    lines = read_lines()
                                    ###################################################################################
                                    
                                    if comport_is_active:
                                        # Use the 'mv' command for renaming
                                        send_command(bytearray(f'cat "{read_selected_file_path}{filename_txt}" ; (echo END) > /dev/null\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   cat "{read_selected_file_path}{filename_txt}"\n')
                                    
                                    else:
                                        messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                        root.destroy()
                                        self.open_after_disconnection()
                                        return
                                
                                    lines = self.read_Response_END()  # Call the function
                                    if lines is None:
                                        messagebox.showwarning("Error!", "Response not received within the timeout.\nPlease retry / check hardware connection!")
                                        return  # Stop execution
                                    decoded_lines = [line.decode() for line in lines]
                                    print(decoded_lines)
                                    test_flag_2 = False
                                    for line in decoded_lines:
                                        line = line.split("selected_files:")[-1].strip()
                                        print(line)
                                        print(f"{current_path}{selected_folder}")
                                        if f'{current_path}{selected_folder}' in line:
                                             line_to_edit = line
                                             print(f".......................{line}\n\n\n{current_path}{selected_folder}")
                                             print("yes")
                                             test_flag_2 = True
                                             print((line.split(f"{current_path}{selected_folder}")))
                                             line_needs_to_be_added = current_path+new_folder_name+(line.split(f"{current_path}{selected_folder}")[-1])
                                             print(line_needs_to_be_added)
                                             #break
                                    if test_flag_2:
                                        print("hii")
                                        test_flag_2 = False
                                        
                                        line_to_edit = filename_txt_string_editor(line_to_edit)
                                        comport_is_active = interface_is_online(self.comport)

                                        if comport_is_active:
                                            send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                            file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return
                                        
                                        if comport_is_active:
                                            send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {line_needs_to_be_added}" >> {filename_txt}\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {line_needs_to_be_added}" >> {filename_txt}\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return
                                    #self.get_max_duration()
                        else:
                            new_folder_name = simpledialog.askstring("Rename File", "Enter the new File name:")
                            if new_folder_name == "":
                                messagebox.showwarning("Invalid Name", "No new File name provided.")
                                return
                            if new_folder_name in listbox_items and not new_folder_name == selected_folder:
                                messagebox.showwarning("Invalid Name", "A File with this name already exists.")
                                return
                            if new_folder_name == selected_folder:
                                messagebox.showwarning("No changes!", "The entered name is the same as the selected file.")
                                return
                            if new_folder_name:
                                # If a new name is provided, proceed with renaming
                                result = messagebox.askyesno("Rename File", f"Are you sure you want to rename the File '{selected_folder}' to '{new_folder_name}.bin'?")
                                if result:
                                    folders_available.remove(selected_folder)
                                    folders_available.append(new_folder_name)

                                    print(f"file name: {new_folder_name}")
                                    new_folder_name = str(new_folder_name).strip()
                                    if ".bin" in new_folder_name:
                                        print("helloo")
                                        new_folder_name = new_folder_name.split(".bin")[0]

                                    # Execute the rename command
                                    comport_is_active = interface_is_online(self.comport)
                                    
                                    check_selected_folder_2 = str(selected_folder).split(".bin")[0]
                                    if comport_is_active:
                                        # Use the 'mv' command for renaming
                                        send_command(bytearray(f'mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}.bin" && \ \nmv "{current_path}{check_selected_folder_2}.log" "{current_path}{new_folder_name}.log"\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   mv "{current_path}{selected_folder}" "{current_path}{new_folder_name}.bin" && \ \nmv "{current_path}{check_selected_folder_2}.log" "{current_path}{new_folder_name}.log"\n')
                                    
                                    else:
                                        messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                        root.destroy()
                                        self.open_after_disconnection()
                                        return
                                    
                                    if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True, destroy_root=True):
                                        return
                                    ########################################################################
                                    lines = read_lines()
                                    ###################################################################################
                                    
                                    if comport_is_active:
                                        # Use the 'mv' command for renaming
                                        send_command(bytearray(f'cat "{read_selected_file_path}{filename_txt}" ; (echo END) > /dev/null\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   cat "{read_selected_file_path}{filename_txt}"\n')
                                    else:
                                        messagebox.showwarning("Warning", "COM port got disconnected!\nCould not rename the selected folder.")
                                        root.destroy()
                                        self.open_after_disconnection()
                                        return
                                
                                    lines = self.read_Response_END()  # Call the function
                                    if lines is None:
                                        messagebox.showwarning("Error!", "Response not received within the timeout.\nPlease retry / check hardware connection!")
                                        return  # Stop execution
                                    decoded_lines = [line.decode() for line in lines]
                                    print(decoded_lines)
                                    test_flag = False
                                    for line in decoded_lines:
                                        line = line.split("selected_files:")[-1].strip()
                                        print(line)
                                        print(f"{current_path}{selected_folder}")
                                        if f'{current_path}{selected_folder}' == f"{line}.bin":
                                             line_to_edit = line
                                             print("yes")
                                             test_flag = True
                                             #break
                                    if test_flag:
                                        print("hii")
                                        test_flag = False
                                       
                                        line_to_edit = filename_txt_string_editor(line_to_edit)
                                       
                                        comport_is_active = interface_is_online(self.comport)

                                        if comport_is_active:
                                            send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                            file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return
                                        
                                        if comport_is_active:
                                            send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {current_path}{new_folder_name}" >> {filename_txt}\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt} && \ \necho "selected_files: {current_path}{new_folder_name}" >> {filename_txt}\n')
                                        else:
                                            msg_box_11 = QMessageBox()
                                            msg_box_11.setWindowTitle("Error!")
                                            msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                            msg_box_11.exec()
                                            self.open_after_disconnection()
                                            return
                                        
                                    rename_file = str(selected_folder).split(".bin")[0].strip()
                                    if rename_file in self.variable_names:
                                        index_rename_file =  self.variable_names.index(rename_file)
                                        self.variable_names[index_rename_file] = new_folder_name
                                        
                                    listbox.delete(selected_indices[0])
                                    listbox.insert(selected_indices[0], f"{new_folder_name}.bin")
                                    
                                    if config_button:
                                        print("hi printed")
                                        self.populate_table()
                                    ########################################################################
                                    #self.get_max_duration()
                    else:
                        messagebox.showwarning("Select Folder", "No folder is selected to Rename!")
                # Function to confirm folder deletion
                def confirm_delete_folder():
                        global ser
                        selected_indices = listbox.curselection()
                        if selected_indices:
                                test = current_path.split("/")
                                if len(test) <= 4:
                                    messagebox.showwarning("Warning", "You cannot delete this file!")
                                    return
                                #print(selected_indices)
                                selected_folder = listbox.get(selected_indices[0])
                                #print(selected_folder)
                                if not str(selected_folder).startswith("(d)"):
                                    result = messagebox.askyesno("Delete File", "Are you sure you want to delete the selected file?")
                                    if result:
                                        print(f"hiii: {selected_folder}")
                                        print(folders_available)
                                        folders_available.remove(selected_folder)
                                        listbox.delete(selected_indices[0])
                                        print(selected_folder)
                                        #print(f"Deleting folder: {selected_folder}")  # Placeholder action
                                        comport_is_active = interface_is_online(self.comport)
                                        if comport_is_active: 
                                            send_command(bytearray(f'rm "{current_path}{selected_folder[:-4]}"*\n', 'ascii'))
                                            if Commands_file_user:
                                                with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   rm "{current_path}{selected_folder[:-4]}"*\n')
                                        else:
                                            messagebox.showwarning("Warning", "COM port got disconnected! could not delete")
                                            root.destroy()
                                            self.open_after_disconnection()
                                            return
                                        lines = read_lines()
                                        
                                    line_to_edit = current_path+str(selected_folder).split(".bin")[0]
                                    print(line_to_edit)
                                
                                    line_to_edit = filename_txt_string_editor(line_to_edit)
                                    comport_is_active = interface_is_online(self.comport)

                                    if comport_is_active:
                                        send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   "cd {read_selected_file_path}"\n')
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                        msg_box_11.exec()
                                        self.open_after_disconnection()
                                        return
                                                
                                    if comport_is_active:
                                        send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt}\n', 'ascii'))
                                        if Commands_file_user:
                                            with open(file_path, 'a') as file:
                                                file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt}\n')
                                    else:
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                        msg_box_11.exec()
                                        self.open_after_disconnection()
                                        return
                                    
                                    print(selected_folder)
                                    selected_file_to_delete = selected_folder.split(".bin")[0].strip()
                                    if selected_file_to_delete in self.variable_names:
                                        self.variable_names.remove(selected_file_to_delete)

                                    if config_button:
                                        print(self.variable_names)
                                        self.populate_table()
                                else:
                                    result = messagebox.askyesno("Delete Folder", "Are you sure you want to delete the selected Folder? All the files inside the folder will be deleted")
                                    if result:
                                        folders_available.remove(selected_folder)
                                        listbox.delete(selected_indices[0])
                                        selected_folder = str(selected_folder).split("(d)  ")[1]
                                        comport_is_active = interface_is_online(self.comport)
                                        if comport_is_active: 
                                            send_command(bytearray(f'rm -r "{current_path}{selected_folder}"\npwd\n', 'ascii'))
                                            if Commands_file_user:
                                                print(current_path)
                                                with open(file_path, 'a') as file:
                                                    file.write(f'\n{get_current_datetime()}   rm -r "{current_path}{selected_folder}"\n{get_current_datetime()}   pwd\n')
                                        else:
                                             messagebox.showwarning("Warning", "COM port got disconnected! could not delete")
                                             root.destroy()
                                             self.open_after_disconnection()
                                             return
                                        lines = read_lines()
                                    self.check_selected_files_availability()
                        else:
                            messagebox.showwarning("Select a file", "No file is selected to delete!")

                # Bind double-click event to the Listbox
                listbox.bind("<Double-1>", lambda event: open_file_selection())
                root.protocol("WM_DELETE_WINDOW", on_secondary_close)
                root.mainloop()
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText("Replay is ON!")
            msg_box_2.exec()

    def open_about_dialog(self):
        if gui_opened:
             return
        global config_button, ser, click_count
        click_count = 0
        if not (recording_started or replay_started or browse_files or browse_folder or config_browse_file or delete_gui):
            config_button = False
            if Commands_file_user:
                with open(file_path, 'a') as file:
                    file.write(f'\n{get_current_datetime()}   *----Opened About window----*\n')
            self.show_path_btn_replay.setVisible(False)
            self.vericalline_fs_system.setVisible(False)
            self.label_SD_image_system.setVisible(False)
            self.label_SD_image_display.setVisible(False)
            self.show_path_btn_replay_rtcm.setVisible(False)
            self.hide_path_btn_replay_rtcm.setVisible(False)
            self.label_SSD_capacity.setVisible(False)
            self.comboBox_number_of_files.setVisible(False)
            self.label_MHz_BW.setVisible(False)
            self.label_SD_image_system_download_2.setVisible(False)
            self.label_SD_image_system_download.setVisible(False)
            self.pushButton_refresh_config_maxduration.setVisible(False)
            self.label_MHz_LO.setVisible(False)
            self.label_MHz_SF.setVisible(False)
            self.label_files_select.setVisible(False)
            self.label_current_file.setVisible(False)
            self.label_available_Duration.setVisible(False)
            self.hide_path_btn_replay.setVisible(False)
            self.show_path_btn.setVisible(False)
            self.hide_path_btn.setVisible(False)
            self.show_path_btn_rtcm.setVisible(False)
            self.hide_path_btn_rtcm.setVisible(False)
            self.table_widget.setVisible(False)
            self.label_fs_system.setVisible(False)
            self.label_fs_system_display.setVisible(False)
            self.lineEdit_fs_system.setVisible(False)
            self.line_fs_system.setVisible(False)
            self.fs_system_edit_btn.setVisible(False)
            self.fs_system_submit_btn.setVisible(False)
            #self.pushButton_select_file.setVisible(False)
            self.label_config.setVisible(False)
            self.pushButton_browse_config.setVisible(False)
            self.pushButton_refresh_config.setVisible(False)
            #self.green_satellite.setVisible(True)
            self.radioButton_autoplay.setVisible(False)
            self.label_Gain_Tx.setVisible(False)
            self.label_Gain_Tx_2ch.setVisible(False)
            self.label_Gain_Tx_2_2ch.setVisible(False) 
            self.label_Gain_Tx_2.setVisible(False)
            self.lineEdit_Gain_Tx_2.setVisible(False)
            self.label_Gain_Tx_3ch.setVisible(False)
            self.line_vertical_Replay.setVisible(False)
            self.lineEdit_Gain_Tx.setVisible(False)
            self.lineEdit_rate.setVisible(False)
            self.label_rate.setVisible(False)
            self.radioButton_Rx_1.setVisible(False)
            self.radioButton_Rx_2.setVisible(False)
            self.label_sampling.setVisible(False)
            self.label_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq_2.setVisible(False)
            self.red_light_record.setVisible(False)
            self.green_light_record.setVisible(False)
            self.green_light.setVisible(False)
            self.pushButton_invisible.setVisible(True)
            self.pushButton_pdf.setVisible(True)
            self.red_light.setVisible(False)
            self.line_record.setVisible(False)
            self.line_vertical.setVisible(False)
            self.line_vertical_2.setVisible(False)
            self.label_browse_record.setVisible(False)
            self.label_browse_record_rtcm.setVisible(False)
            self.radioButton_GPIO_Record.setVisible(False)
            self.lineEdit_browse_record.setVisible(False)
            self.lineEdit_browse_record_rtcm.setVisible(False)
            self.pushButton_browse_record.setVisible(False)
            self.pushButton_browse_record_rtcm.setVisible(False)
            self.label_connectivity.setVisible(False)
            self.pushButton_login.setEnabled(True)
            
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(True)
            self.pushButton_3.setVisible(False)
            self.pushButton_4.setVisible(True)
            self.pushButton_5.setVisible(True)
            self.lineEdit.setVisible(False)
            self.lineEdit_2.setVisible(False)
            self.lineEdit_3.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_6.setVisible(False)
            self.label.setVisible(False)
            self.label_10.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.label_8.setVisible(False)
            self.label_9.setVisible(False)
            self.comboBox.setVisible(False)
            self.radioButton_double.setVisible(False)
            self.radioButton_single.setVisible(False)
            self.label_radio.setVisible(False)
            self.lineEdit_hostname.setVisible(False)
            self.lineEdit_password.setVisible(False)
            self.label_ssid.setVisible(False)
            self.label_hostname.setVisible(False)
            self.label_gpiomode.setVisible(False)
            self.radioButton_gpiomode.setVisible(False)
            self.radioButton_rfmdmode.setVisible(False)
            if (comport_connected == True):
                self.label_connected.setVisible(False)
                self.label_connected_rtcm.setVisible(False)
                self.button_reconnect.setVisible(False)
                self.button_reboot.setVisible(False)
                self.button_shutdown.setVisible(False)
                self.label_connectivity.setVisible(False)
                self.radioButton_double.setVisible(False)
                self.radioButton_single.setVisible(False)
                self.label_radio.setVisible(False)
                self.lineEdit_hostname.setVisible(False)
                self.label_ssid.setVisible(False)
                self.lineEdit_password.setVisible(False)
                self.label_hostname.setVisible(False)
                self.label_gpiomode.setVisible(False)
                self.radioButton_gpiomode.setVisible(False)
                self.radioButton_rfmdmode.setVisible(False)
            self.comboBox_2.setVisible(False)
            self.label_bandwidth.setVisible(False)
            self.label_gain.setVisible(False)
            self.lineEdit_bandwidth.setVisible(False)
            self.lineEdit_gain_1.setVisible(False)
            self.lineEdit_gain_2.setVisible(False)
            self.lineEdit_bandwidth_2.setVisible(False)
            self.lineEdit_replay.setVisible(False)
            self.label_replay.setVisible(False)

            self.pushButton_6.setVisible(False)
            self.pushButton_7.setVisible(False)
            self.lineEdit_7.setVisible(False)
            self.lineEdit_8.setVisible(False)
            self.label_11.setVisible(False)
            self.label_12.setVisible(False)
            self.radioButton_GPIO_Replay.setVisible(False)
            self.pushButton_8.setVisible(False)
            self.lineEdit9.setVisible(False)
            self.lineEdit_replay_rtcm.setVisible(False)
            self.pushButton_browse_replay_rtcm.setVisible(False)
            self.label_files_rtcm.setVisible(False)
            self.label_13.setVisible(False)
            self.label_about_2.setVisible(True)
            self.label_about_3.setVisible(True)
            self.line_2.setVisible(False)
            self.pushButton_submit.setVisible(False)
            self.comboBox_baudrate.setVisible(False)
            self.comboBox_comport.setVisible(False)
            self.label_ref_freq.setVisible(False)
            self.comboBox_ref_freq.setVisible(False)
            self.comboBox_baudrate_rtcm.setVisible(False)
            self.radioButton_ad9361.setVisible(False)
            self.radioButton_rtcm.setVisible(False)
            self.lineEdit_deviceid.setVisible(False)
            self.label_deviceid.setVisible(False)
            self.lineEdit_busno.setVisible(False)
            self.label_busno.setVisible(False)
            self.pushButton_usb_info.setVisible(False)
            self.comboBox_comport_rtcm.setVisible(False)

            self.pushButton_4.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_2.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_5.setStyleSheet("QPushButton{"
                                         "background-color: #1ABC9C;"
                                         "color: white;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_login.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_select_file.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText("You cannot switch to About when Recording/Replay is ON!")
            msg_box_2.exec()

    def open_login_dialog(self):
        if gui_opened:
             return
        global config_button
        if not (recording_started or replay_started or browse_folder or browse_files or config_browse_file or delete_gui): 
            config_button = False
            if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f'\n{get_current_datetime()}   *----Opened Connect window----*\n')
            self.show_path_btn_replay.setVisible(False)
            self.vericalline_fs_system.setVisible(False)
            self.label_SD_image_system.setVisible(False)
            self.label_SD_image_display.setVisible(False)
            self.label_SSD_capacity.setVisible(False)
            self.show_path_btn_replay_rtcm.setVisible(False)
            self.pushButton_refresh_config_maxduration.setVisible(False)
            self.hide_path_btn_replay_rtcm.setVisible(False)
            self.comboBox_number_of_files.setVisible(False)
            self.pushButton_invisible.setVisible(False)
            self.pushButton_pdf.setVisible(False)
            self.label_SD_image_system_download_2.setVisible(False)
            self.label_SD_image_system_download.setVisible(False)
            self.label_MHz_BW.setVisible(False)
            self.label_MHz_LO.setVisible(False)
            self.label_MHz_SF.setVisible(False)
            self.label_files_select.setVisible(False)
            self.label_current_file.setVisible(False)
            self.label_SSD_capacity.setVisible(False)
            self.label_available_Duration.setVisible(False)
            self.hide_path_btn_replay.setVisible(False)
            self.table_widget.setVisible(False)
            self.show_path_btn.setVisible(False)
            self.hide_path_btn.setVisible(False)
            self.show_path_btn_rtcm.setVisible(False)
            self.hide_path_btn_rtcm.setVisible(False)
            self.label_fs_system.setVisible(False)
            self.label_fs_system_display.setVisible(False)
            self.lineEdit_fs_system.setVisible(False)
            self.line_fs_system.setVisible(False)
            self.fs_system_edit_btn.setVisible(False)
            self.fs_system_submit_btn.setVisible(False)
            #self.pushButton_select_file.setVisible(False)
            self.label_config.setVisible(False)
            self.pushButton_browse_config.setVisible(False)
            self.pushButton_refresh_config.setVisible(False)
            #self.green_satellite.setVisible(False) 
            self.radioButton_Rx_1.setVisible(False)
            self.radioButton_Rx_2.setVisible(False)  
            self.label_sampling.setVisible(False)
            self.radioButton_autoplay.setVisible(False)
            self.label_Gain_Tx.setVisible(False)
            self.label_Gain_Tx_2ch.setVisible(False)
            self.label_Gain_Tx_2_2ch.setVisible(False) 
            self.label_Gain_Tx_2.setVisible(False)
            self.lineEdit_Gain_Tx_2.setVisible(False)
            self.label_Gain_Tx_3ch.setVisible(False)
            self.line_vertical_Replay.setVisible(False)
            self.lineEdit_Gain_Tx.setVisible(False)
            self.lineEdit_rate.setVisible(False)
            self.label_rate.setVisible(False)
            self.label_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq.setVisible(False)
            self.lineEdit_samplingfreq_2.setVisible(False)
            self.red_light_record.setVisible(False)
            self.green_light_record.setVisible(False)
            self.green_light.setVisible(False)
            self.red_light.setVisible(False)
            self.line_record.setVisible(False)
            self.line_vertical.setVisible(False)
            self.line_vertical_2.setVisible(False)
            self.label_browse_record.setVisible(False)
            self.label_browse_record_rtcm.setVisible(False)
            self.radioButton_GPIO_Record.setVisible(False)
            self.lineEdit_browse_record.setVisible(False)
            self.lineEdit_browse_record_rtcm.setVisible(False)
            self.pushButton_browse_record.setVisible(False)
            self.pushButton_browse_record_rtcm.setVisible(False)
            self.pushButton_login.setEnabled(False)
            self.pushButton.setVisible(False)
            self.pushButton_2.setVisible(True)
            self.pushButton_3.setVisible(False)
            self.pushButton_4.setVisible(True)
            
            self.pushButton_5.setVisible(True)
            self.lineEdit.setVisible(False)
            if(not comport_connected):
                self.comboBox_comport.setVisible(True)
                self.label_ref_freq.setVisible(False)
                self.comboBox_ref_freq.setVisible(False)
                self.comboBox_baudrate.setVisible(True)
                self.pushButton_submit.setVisible(True)
                self.label_connectivity.setVisible(True)
                self.radioButton_double.setVisible(True)
                self.radioButton_single.setVisible(True)
                self.label_radio.setVisible(True)
                item = self.comboBox_comport.currentText()
                if item == WIFI_INTERFACE_OPTION:
                    self.lineEdit_hostname.setVisible(True)
                    self.label_ssid.setVisible(True)
                    self.lineEdit_password.setVisible(False)
                    self.label_hostname.setVisible(True)
                else:
                    self.lineEdit_hostname.setVisible(False)
                    self.label_ssid.setVisible(False)
                    self.lineEdit_password.setVisible(False)
                    self.label_hostname.setVisible(False)
                self.label_gpiomode.setVisible(False)
                self.radioButton_gpiomode.setVisible(False)
                self.radioButton_rfmdmode.setVisible(False)
                self.comboBox_baudrate_rtcm.setVisible(True)
                self.radioButton_ad9361.setVisible(True)
                self.radioButton_rtcm.setVisible(True)
                if self.comboBox_comport_rtcm.currentText() == "HW USB":
                    self.lineEdit_deviceid.setVisible(True)
                    self.label_deviceid.setVisible(True)
                    self.lineEdit_busno.setVisible(True)
                    self.label_busno.setVisible(True)
                    self.pushButton_usb_info.setVisible(True)
                else:
                    self.lineEdit_deviceid.setVisible(False)
                    self.label_deviceid.setVisible(False)
                    self.lineEdit_busno.setVisible(False)
                    self.label_busno.setVisible(False)
                    self.pushButton_usb_info.setVisible(False)
                self.comboBox_comport_rtcm.setVisible(True)
            if(comport_connected):
                if (self.radioButton_rtcm.isChecked()):
                    self.label_connected_rtcm.setVisible(True)
                else:
                    self.label_connected_rtcm.setVisible(False)
                self.label_connected.setVisible(True)
                self.button_reconnect.setVisible(True)
                self.button_reboot.setVisible(True)
                self.button_shutdown.setVisible(True)
                self.radioButton_double.setVisible(False)
                self.radioButton_single.setVisible(False)
                self.label_radio.setVisible(False)
                self.lineEdit_hostname.setVisible(False)
                self.lineEdit_password.setVisible(False)
                self.label_ssid.setVisible(False)
                self.label_hostname.setVisible(False)
                self.label_gpiomode.setVisible(False)
                self.radioButton_gpiomode.setVisible(False)
                self.radioButton_rfmdmode.setVisible(False)
                self.comboBox_baudrate_rtcm.setVisible(False)
                self.radioButton_ad9361.setVisible(False)
                self.radioButton_rtcm.setVisible(False)
                self.lineEdit_deviceid.setVisible(False)
                self.label_deviceid.setVisible(False)
                self.lineEdit_busno.setVisible(False)
                self.label_busno.setVisible(False)
                self.pushButton_usb_info.setVisible(False)
                self.comboBox_comport_rtcm.setVisible(False)
            self.lineEdit_2.setVisible(False)
            self.lineEdit_3.setVisible(False)
            self.lineEdit_4.setVisible(False)
            self.lineEdit_6.setVisible(False)
            self.label.setVisible(False)
            self.label_10.setVisible(False)
            self.label_2.setVisible(False)
            self.label_3.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.label_8.setVisible(False)
            self.label_9.setVisible(False)
            self.comboBox.setVisible(False)
            self.comboBox_2.setVisible(False)
            self.label_bandwidth.setVisible(False)
            self.label_gain.setVisible(False)
            self.lineEdit_bandwidth.setVisible(False)
            self.lineEdit_gain_1.setVisible(False)
            self.lineEdit_gain_2.setVisible(False)
            self.lineEdit_bandwidth_2.setVisible(False)
            self.lineEdit_replay.setVisible(False)
            self.label_replay.setVisible(False)

            self.pushButton_6.setVisible(False)
            self.pushButton_7.setVisible(False)
            self.lineEdit_7.setVisible(False)
            self.lineEdit_8.setVisible(False)
            self.label_11.setVisible(False)
            self.label_12.setVisible(False)
            self.radioButton_GPIO_Replay.setVisible(False)
            self.pushButton_8.setVisible(False)
            self.lineEdit9.setVisible(False)
            self.lineEdit_replay_rtcm.setVisible(False)
            self.pushButton_browse_replay_rtcm.setVisible(False)
            self.label_files_rtcm.setVisible(False)
            self.label_13.setVisible(False)
            self.label_about_2.setVisible(False)
            self.label_about_3.setVisible(False)
            self.line_2.setVisible(False)
            self.pushButton_4.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_2.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_login.setStyleSheet("QPushButton{"
                                         "background-color: #1ABC9C;"
                                         "color: white;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_5.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_select_file.setStyleSheet("QPushButton{"
                                         "background-color: white;"
                                         "color: black;"
                                         "border-style: outset;"
                                         "border-width: 2px;"
                                         "border-color: black;"
                                         "border-radius: 20px;"
                                         "}"
                                         "QPushButton:hover {"
                                         "background-color: #B2DFDB;"  # Light teal
                                         "}"
                                         "QPushButton:pressed {"
                                         "background-color: #5A9;"  # Change color when pressed if desired
                                         "}")
            self.pushButton_4.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText("You cannot switch to Connect when Recording/Replay is ON!")
            msg_box_2.exec()
        
    def open_select_file_dialog(self):
        if (developer_rx_tx):
             print("hiii")
             self.vericalline_fs_system.setVisible(True)
             self.label_fs_system.setGeometry(QtCore.QRect(45, 80, 350, 50))
             self.fs_system_edit_btn.setGeometry(QtCore.QRect(145, 170, 50, 31))
             self.fs_system_submit_btn.setGeometry(QtCore.QRect(145, 170, 50, 31))
             self.lineEdit_fs_system.setGeometry(QtCore.QRect(73, 125, 200, 31))  # Adjust position to fit next to progress bar
             self.label_fs_system_display.setGeometry(QtCore.QRect(130, 215, 80, 30))
             self.label_SD_image_system.setVisible(True)
             self.label_SD_image_display.setVisible(True)
        else:
             self.vericalline_fs_system.setVisible(False)
             self.label_SD_image_system.setVisible(False)
             self.label_SD_image_display.setVisible(False)
             self.label_fs_system.setGeometry(QtCore.QRect(220, 80, 350, 50))
             self.label_fs_system_display.setGeometry(QtCore.QRect(310, 215, 80, 30))
             self.lineEdit_fs_system.setGeometry(QtCore.QRect(251, 125, 200, 31))
             self.fs_system_submit_btn.setGeometry(QtCore.QRect(325, 170, 50, 31))
             self.fs_system_edit_btn.setGeometry(QtCore.QRect(325, 170, 50, 31))
        if gui_opened:
             return
        global ser, config_button, nvme_label_found
        if not (recording_started or replay_started or browse_files or browse_folder or config_browse_file or delete_gui): 
            if (self.baudrate != None and
                self.comport != None):
                if not submitted:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Submit!")
                    msg_box_11.setText("Please Submit the selected parameters")
                    msg_box_11.exec()
                    return
                if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f'\n{get_current_datetime()}   *----Opened Files window----*\n')
                #############################################################################
                #####################################################################
                """if ser.isOpen():
                    self.ensure_interface_disconnection()
                try:
                    ser = serial.Serial(self.comport, self.baudrate, timeout=0.5)
                except serial.SerialException as e:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error!")
                    msg_box_2.setText("You cannot open this COM Port!")
                    msg_box_2.exec()
                    self.open_after_disconnection() 
                    return"""
                #######################################################################
                """comport_is_active = interface_is_online(self.comport)
                if comport_is_active: 
                    send_command(b'\x03')
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   \x03')
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return
                comport_is_active = interface_is_online(self.comport)
                if comport_is_active: 
                    send_command(bytearray('clear\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   clear\n')
                    read_lines()
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return"""
                ################################################################################
                #directory = read_selected_file_path
                """if ser.isOpen():
                    self.ensure_interface_disconnection()
                try:
                    ser = serial.Serial(self.comport, self.baudrate, timeout=timeout_time)
                    read_lines()
                except serial.SerialException as e:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Error!")
                    msg_box_2.setText("You cannot open this COM Port!")
                    msg_box_2.exec()
                    self.open_after_disconnection() 
                    return"""
                """comport_is_active = interface_is_online(self.comport)
                
                if comport_is_active:   
                    send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                    lines = read_lines()
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return
                comport_is_active = interface_is_online(self.comport)

                if comport_is_active:               
                    send_command(bytearray(f'cat "{filename_txt}" ; (echo END) > /dev/null\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   cat "{filename_txt}" ; (echo END) > /dev/null\n')
                    #lines = read_lines()
                    
                    lines = self.read_Response_END()  # Call the function
                    if lines is None:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        msg_box_11.exec()
                        return
                    #print(f"\n\n\n\nimp:{lines}\n\n\n")
                   
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"COM port got disconnected!")
                    msg_box_11.exec()
                    self.open_after_disconnection()
                    return
                if len(lines) >= 3:
                    if not filename_txt in str(lines[0]):
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! 'HW_files' folder is not found\nIn the directory {read_selected_file_path}")
                        msg_box_11.exec() 
                        return
                else:
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Oops!, Please check the connections\nIs the AD9361 Hardware connected?")
                    msg_box_11.exec() 
                    return
                ######################################################################################
                lines = lines[1:-2]
                #print(lines)
                try:
                    decoded_lines = [line.decode() for line in lines]
                except UnicodeDecodeError as e:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Recevied messages are not decoded")
                        msg_box_11.exec() 
                        return"""
                    
                #print(decoded_lines)
                """file_names = decoded_lines
                count = 0
                directories_files = {}
                self.variable_names = []
                if decoded_lines == []:
                    self.variable_names = []"""
                
                """elif not "No such file or directory" in (decoded_lines[-1]):
                    for line in decoded_lines:
                        if "selected_files:" in line:
                            print(line)
                            extracted_line = "/"+"/".join(line.split("/")[1:-1]).split("\\")[0].strip()
                            print(extracted_line)
                            extracted_file_name = line.split("/")[-1].split("\\")[0].strip()+".bin"
                            print(extracted_file_name)
                            count += 1
                            directories_files[count] = extracted_line, extracted_file_name

                    # Build the command dynamically
                    command_parts = []
                    print(directories_files)
                    for _, (directory, filename) in directories_files.items():
                        command_parts.append(
                            f'cd "{directory}" && [ -f "{filename}" ] && echo "{directory}/{filename}:- Found" || echo "{directory}/{filename}:- Not Found"'
                        )

                    ################################################################################################
                    # Join all commands with a semicolon
                    command_file_read = "; ".join(command_parts) + ' ; (echo END) > /dev/null\n'
                    print(command_file_read)
                    #print(command_file_read)
                    send_command(bytearray(command_file_read, 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}  {command_file_read}')
                    lines = self.read_Response_END()  # Call the function
                    if lines is None:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"Oops! Response not received within timeout time\nPlease retry/ check the hardware connection.")
                        msg_box_11.exec()
                        return
                    #print(lines)
                    decoded_lines = [line.decode() for line in lines]
                    #print(f"\n\n\n{decoded_lines}\n\n\n")
                    for line in decoded_lines:
                        #print(f"\n\n\n\nline:{line}\n\n\n\n")
                        message = str(line.split(":-")[-1]).strip()
                        print(f"\n\n\n{message}\n\n\n\n")
                        if message == "Not Found":
                            line_to_edit = line.split(":-")[0].split(".bin")[0].strip()
                           
                            line_to_edit = filename_txt_string_editor(line_to_edit)
                            comport_is_active = interface_is_online(self.comport)

                            if comport_is_active:
                                send_command(bytearray(f'cd "{read_selected_file_path}"\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   cd "{read_selected_file_path}"\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                                        
                            if comport_is_active:
                                send_command(bytearray(f'sed -i "/{line_to_edit}/d" {filename_txt}\n', 'ascii'))
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   sed -i "/{line_to_edit}/d" {filename_txt}\n')
                            else:
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected! Please reconnect")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                                        
                        if message == "Found":
                            print(f"\n\n\n{line}")
                            self.variable_names.append(line.split(":-")[0].split("/")[-1].strip().split(".bin")[0].strip())
                    ################################################################################################
                elif "No such file or directory" in (decoded_lines[-1]):
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Info")
                    msg_box_11.setText(f"The file {filename_txt} not found\n\nA new {filename_txt} file is created\n\nDirectory:{directory}")
                    msg_box_11.exec()
                    comport_is_active = interface_is_online(self.comport)
                    
                    if comport_is_active: 
                        send_command(bytearray(f'cd "{directory}"\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   cd "{directory}"\n')
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"COM port got disconnected!")
                        msg_box_11.exec()
                        self.open_after_disconnection()
                        return
                    comport_is_active = interface_is_online(self.comport)
                   
                    if comport_is_active: 
                        send_command(bytearray(f'touch "{filename_txt}"\n', 'ascii'))
                        if Commands_file_user:
                            with open(file_path, 'a') as file:
                                file.write(f'{get_current_datetime()}   touch "{filename_txt}"\n')
                    else:
                        msg_box_11 = QMessageBox()
                        msg_box_11.setWindowTitle("Error!")
                        msg_box_11.setText(f"COM port got disconnected!")
                        msg_box_11.exec()
                        self.open_after_disconnection()
                        return
                    read_lines()
                    self.variable_names = []"""
                ###############################################################################################
                #self.variable_names.append(line)
                #print(file_dictionary)
                #print(self.variable_names)
                #read_lines()
                self.populate_table()
                #####################################################################################
                config_button = True
                self.pushButton_refresh_config_maxduration.setVisible(False)
                self.label_SD_image_system_download_2.setVisible(False)
                self.label_SD_image_system_download.setVisible(False)
                self.pushButton_invisible.setVisible(False)
                self.pushButton_pdf.setVisible(False)
                self.comboBox_number_of_files.setVisible(False)
                self.label_MHz_BW.setVisible(False)
                self.label_MHz_LO.setVisible(False)
                self.label_MHz_SF.setVisible(False)
                self.label_files_select.setVisible(False)
                self.label_current_file.setVisible(False)
                self.show_path_btn_replay.setVisible(False)
                self.show_path_btn_replay_rtcm.setVisible(False)
                self.hide_path_btn_replay_rtcm.setVisible(False)
                self.label_SSD_capacity.setVisible(False)
                self.label_available_Duration.setVisible(False)
                self.hide_path_btn_replay.setVisible(False)
                if submit_btn_clicked:
                    self.fs_system_submit_btn.setVisible(True)
                    self.fs_system_edit_btn.setVisible(False)                                    
                if Edit_btn_clicked:
                    self.fs_system_edit_btn.setVisible(True)
                    self.fs_system_submit_btn.setVisible(False)
                self.show_path_btn.setVisible(False)
                self.hide_path_btn.setVisible(False)
                self.show_path_btn_rtcm.setVisible(False)
                self.hide_path_btn_rtcm.setVisible(False)
                self.table_widget.setVisible(True)
                self.label_config.setVisible(True)
                self.label_fs_system.setVisible(True)
                self.label_fs_system_display.setVisible(True)
                self.lineEdit_fs_system.setVisible(True)
                self.line_fs_system.setVisible(True)
                #self.fs_system_submit_btn.setVisible(True)
                #self.pushButton_select_file.setVisible(True)
                self.pushButton_browse_config.setVisible(True)
                self.pushButton_refresh_config.setVisible(True)
                self.pushButton_login.setEnabled(True)
                #self.green_satellite.setVisible(False) 
                self.radioButton_Rx_1.setVisible(False)
                self.radioButton_Rx_2.setVisible(False)  
                self.label_sampling.setVisible(False)
                self.radioButton_autoplay.setVisible(False)
                self.label_Gain_Tx.setVisible(False)
                self.label_Gain_Tx_2ch.setVisible(False)
                self.label_Gain_Tx_2_2ch.setVisible(False) 
                self.label_Gain_Tx_2.setVisible(False)
                self.lineEdit_Gain_Tx_2.setVisible(False)
                self.label_Gain_Tx_3ch.setVisible(False)
                self.line_vertical_Replay.setVisible(False)
                self.lineEdit_Gain_Tx.setVisible(False)
                self.lineEdit_rate.setVisible(False)
                self.label_rate.setVisible(False)
                self.label_samplingfreq.setVisible(False)
                self.lineEdit_samplingfreq.setVisible(False)
                self.lineEdit_samplingfreq_2.setVisible(False)
                self.red_light_record.setVisible(False)
                self.green_light_record.setVisible(False)
                self.green_light.setVisible(False)
                self.red_light.setVisible(False)
                self.line_record.setVisible(False)
                self.line_vertical.setVisible(False)
                self.line_vertical_2.setVisible(False)
                self.label_browse_record.setVisible(False)
                self.label_browse_record_rtcm.setVisible(False)
                self.radioButton_GPIO_Record.setVisible(False)
                self.lineEdit_browse_record.setVisible(False)
                self.lineEdit_browse_record_rtcm.setVisible(False)
                self.pushButton_browse_record.setVisible(False)
                self.pushButton_browse_record_rtcm.setVisible(False)
                self.pushButton_login.setEnabled(False)
                self.pushButton.setVisible(False)
                self.pushButton_2.setVisible(True)
                self.pushButton_3.setVisible(False)
                self.pushButton_4.setVisible(True)
               
                self.pushButton_5.setVisible(True)
                self.lineEdit.setVisible(False)
                if(not comport_connected):
                    self.comboBox_comport.setVisible(False)
                    self.label_ref_freq.setVisible(False)
                    self.comboBox_ref_freq.setVisible(False)
                    self.comboBox_baudrate.setVisible(False)
                    self.pushButton_submit.setVisible(False)
                    self.label_connectivity.setVisible(False)
                    self.radioButton_double.setVisible(False)
                    self.radioButton_single.setVisible(False)
                    self.label_radio.setVisible(False)
                    self.lineEdit_hostname.setVisible(False)
                    self.lineEdit_password.setVisible(False)
                    self.label_ssid.setVisible(False)
                    self.label_hostname.setVisible(False)
                    self.label_gpiomode.setVisible(False)
                    self.radioButton_gpiomode.setVisible(False)
                    self.radioButton_rfmdmode.setVisible(False)
                    self.comboBox_baudrate_rtcm.setVisible(False)
                    self.radioButton_ad9361.setVisible(False)
                    self.radioButton_rtcm.setVisible(False)
                    self.lineEdit_deviceid.setVisible(False)
                    self.label_deviceid.setVisible(False)
                    self.lineEdit_busno.setVisible(False)
                    self.label_busno.setVisible(False)
                    self.pushButton_usb_info.setVisible(False)
                    self.comboBox_comport_rtcm.setVisible(False)
                if(comport_connected):
                    self.label_connected.setVisible(False)
                    self.label_connected_rtcm.setVisible(False)
                    self.button_reconnect.setVisible(False)
                    self.button_reboot.setVisible(False)
                    self.button_shutdown.setVisible(False)
                    self.radioButton_double.setVisible(False)
                    self.radioButton_single.setVisible(False)
                    self.label_radio.setVisible(False)
                    self.lineEdit_hostname.setVisible(False)
                    self.lineEdit_password.setVisible(False)
                    self.label_ssid.setVisible(False)
                    self.label_hostname.setVisible(False)
                    self.label_gpiomode.setVisible(False)
                    self.radioButton_gpiomode.setVisible(False)
                    self.radioButton_rfmdmode.setVisible(False)
                self.lineEdit_2.setVisible(False)
                self.lineEdit_3.setVisible(False)
                self.lineEdit_4.setVisible(False)
                self.lineEdit_6.setVisible(False)
                self.label.setVisible(False)
                self.label_10.setVisible(False)
                self.label_2.setVisible(False)
                self.label_3.setVisible(False)
                self.label_4.setVisible(False)
                self.label_5.setVisible(False)
                self.label_8.setVisible(False)
                self.label_9.setVisible(False)
                self.comboBox.setVisible(False)
                self.comboBox_2.setVisible(False)
                self.label_bandwidth.setVisible(False)
                self.label_gain.setVisible(False)
                self.lineEdit_bandwidth.setVisible(False)
                self.lineEdit_gain_1.setVisible(False)
                self.lineEdit_gain_2.setVisible(False)
                self.lineEdit_bandwidth_2.setVisible(False)
                self.lineEdit_replay.setVisible(False)
                self.label_replay.setVisible(False)

                self.pushButton_6.setVisible(False)
                self.pushButton_7.setVisible(False)
                self.lineEdit_7.setVisible(False)
                self.lineEdit_8.setVisible(False)
                self.label_11.setVisible(False)
                self.label_12.setVisible(False)
                self.radioButton_GPIO_Replay.setVisible(False)
                self.pushButton_8.setVisible(False)
                self.lineEdit9.setVisible(False)
                self.lineEdit_replay_rtcm.setVisible(False)
                self.pushButton_browse_replay_rtcm.setVisible(False)
                self.label_files_rtcm.setVisible(False)
                self.label_13.setVisible(False)
                self.label_about_2.setVisible(False)
                self.label_about_3.setVisible(False)
                self.line_2.setVisible(False)
                self.pushButton_4.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                self.pushButton_2.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                self.pushButton_select_file.setStyleSheet("QPushButton{"
                                            "background-color: #1ABC9C;"
                                            "color: white;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                self.pushButton_5.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                self.pushButton_login.setStyleSheet("QPushButton{"
                                            "background-color: white;"
                                            "color: black;"
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-color: black;"
                                            "border-radius: 20px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: #B2DFDB;"  # Light teal
                                            "}"
                                            "QPushButton:pressed {"
                                            "background-color: #5A9;"  # Change color when pressed if desired
                                            "}")
                self.pushButton_4.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_5.setEnabled(True)
                self.pushButton_login.setEnabled(True)
            else:
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Missing Data")
                msg_box_9.setText("Please select the Com port")
                msg_box_9.exec()
        else:
            msg_box_2 = QMessageBox()
            msg_box_2.setWindowTitle("Error!")
            msg_box_2.setText("You cannot switch to Connect when Recording/Replay is ON!")
            msg_box_2.exec()
        
    def start_timer(self):
        """thread_1 = threading.Thread(target=self.start_timerr())
        thread_2 = threading.Thread(target=self.get_max_duration())        
        # Start threads
        thread_1.start()
        thread_2.start()"""
        #self.get_max_duration()
        self.start_timerr()
        
    def start_timerr(self):
        global ser, recorded_time, count_one, read_response,  terminated,  read_response, Lg_path, recording_started, duration_valid, file_name_starts_with_dot, fs_system, recording_rx1_channel, recording_dual_channel, recording_rx2_channel, file_count_variable, rtcm_create_file
        #print(recording_started)
        def check_recording():
            global read_response, recording_started, terminated, flag_raised_for_stop_Recording
            while True:
                if read_response:
                    print("read")
                    line = self.read_decoded_line()
                    print(f"line decider: {line}")
                    if "Terminated before the full duration!" in line:
                        terminated = True
                        break
                else:
                    break

        if not recording_started:
            global available_memory
            if checked_both_without_HWUSB:
                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                if not comport_2_rtcm:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                    msg_box_2.exec()
                    self.open_after_disconnection()
                    return
            
                
            file_count_variable = int(self.number_of_files)
            #count_one = 0
            if self.progressrecording is not None:
                self.progressrecording = None
                self.lineEdit_6.clear()
            self.msg_box_2_shown = False
            self.msg_box_error_shown = False
            if checked_both_without_HWUSB or HW_USB_in_use:
               if self.folder_name_record_rtcm is None:
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("Missing Data")
                    msg_box_2.setText("Please enter all the required data before starting the recording")
                    msg_box_2.exec()
                    return
            
            if self.radioButton_double.isChecked():
                start_time = time.time()  # Record start time
                if (self.selected_adc_bits1 is None or
                        self.selected_adc_bits2 is None or
                        self.file_name is None or
                        self.selected_center_frequency1 is None or
                        self.selected_center_frequency2 is None or
                        self.bandwidth is None or
                        self.bandwidth_2 is None or
                        self.duration_value is None or
                        self.samplingfreq_1 is None or
                        self.samplingfreq_2 is None or
                        self.folder_name_record is None):
                    #print("Condition met!")    
                    
                    if not self.msg_box_2_shown:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Missing Data")
                        msg_box_2.setText("Please enter all the required data before starting the recording")
                        msg_box_2.exec()
                        self.msg_box_2_shown = True  # Set the flag to True after showing the message box
                        return
                    
                gain = self.lineEdit_gain_1.text()
                if gain == None or gain == "":
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Missing Data")
                        msg_box_2.setText("Please enter all the required data before starting the recording")
                        msg_box_2.exec()
                        return

                if gain.lower() in ("slow attack", "slowattack"):
                    gain = 100
                    #self.lineEdit_gain_1.setText("Slow attack")
                elif gain.lower() in ("fast attack", "fastattack"):
                    gain = 200
                    #self.lineEdit_gain_1.setText("Fast attack")
                elif gain.lower() == "hybrid":
                    gain = 300
                    #self.lineEdit_gain_1.setText("Hybrid")
                else:
                    try:
                        gain = float(gain)
                    except ValueError:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("error")
                        msg_box_2.setText("please enter a valid Gain")
                        msg_box_2.exec() 
                        return 
                
                if (not (-10 <= gain <= 73)) and gain not in {100, 200, 300}:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Error!")
                        msg_box_2.setText("Gain should be between -10dB and 73dB, except 100, 200, 300")
                        msg_box_2.exec()
                        return
                
                if gain == 100:
                  self.lineEdit_gain_1.setText("Slow attack")
                elif gain == 200:
                     self.lineEdit_gain_1.setText("Fast attack") 
                elif gain == 300:
                     self.lineEdit_gain_1.setText("Hybrid")  
                
                gain_2 = self.lineEdit_gain_2.text()
                if gain_2 == None or gain_2 == "":
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Missing Data")
                            msg_box_2.setText("Please enter all the required data before starting the recording")
                            msg_box_2.exec()
                            return
                if gain_2.lower() in ("slow attack", "slowattack"):
                    gain_2 = 100
                    #self.lineEdit_gain_1.setText("Slow attack")
                elif gain_2.lower() in ("fast attack", "fastattack"):
                    gain_2 = 200
                    #self.lineEdit_gain_1.setText("Fast attack")
                elif gain_2.lower() == "hybrid":
                    gain_2 = 300
                else:
                    try:
                        gain_2 = float(gain_2)
                    except ValueError:
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("error")
                            msg_box_2.setText("please enter a valid Gain")
                            msg_box_2.exec() 
                            return 
                if gain_2 == 100:
                  self.lineEdit_gain_2.setText("Slow attack")
                elif gain_2 == 200:
                     self.lineEdit_gain_2.setText("Fast attack") 
                elif gain_2 == 300:
                     self.lineEdit_gain_2.setText("Hybrid") 
                    
                if (not (-10 <= gain_2 <= 73)) and gain_2 not in {100, 200, 300}:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Error!")
                        msg_box_2.setText("Gain should be between -10dB and 73dB, except 100, 200, 300")
                        msg_box_2.exec()
                        return
                
                if str(self.file_name) == "":
                    msg_box_2 = QMessageBox()
                    msg_box_2.setWindowTitle("missing file name")
                    msg_box_2.setText("please enter the file name")
                    msg_box_2.exec() 
                    return

                duration_valid = validate_time(self.duration_value)
                print(duration_valid)
                if duration_valid == None:
                    msg_box_error = QMessageBox()
                    msg_box_error.setWindowTitle("Invalid Format")
                    msg_box_error.setText("Duration value is in a wrong format")
                    msg_box_error.exec()
                    return
                
                try:
                    self.bandwidth = float(self.bandwidth)
                    self.bandwidth_2 = float(self.bandwidth_2)
                except ValueError:
                    msg_box_error_1 = QMessageBox()
                    msg_box_error_1.setWindowTitle("Invalid Data Type")
                    msg_box_error_1.setText("Bandwidth must be numeric values")
                    msg_box_error_1.exec()
                    return
                
                try:
                    self.selected_center_frequency1 = float(self.selected_center_frequency1)
                    self.selected_center_frequency2 = float(self.selected_center_frequency2)
                except ValueError:
                    if not self.msg_box_error_shown:
                        msg_box_error = QMessageBox()
                        msg_box_error.setWindowTitle("Invalid Data Type")
                        msg_box_error.setText("Center frequency must be numeric values")
                        msg_box_error.exec()
                        self.msg_box_error_shown = True
                    return
                
                try:
                    self.samplingfreq_1 = float(self.samplingfreq_1)
                    self.samplingfreq_2 = float(self.samplingfreq_2)
                except ValueError:
                    if not self.msg_box_error_shown:
                        msg_box_error = QMessageBox()
                        msg_box_error.setWindowTitle("Invalid Data Type")
                        msg_box_error.setText("Sampling Frequency must be numeric values")
                        msg_box_error.exec()
                        self.msg_box_error_shown = True
                    return
                

                if self.selected_adc_bits1 == 4:
                    print("hellochannel1")
                    if float(self.bandwidth) > ((0.9*61.44)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*61.44)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_1) > ((61.44)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((61.44)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    
                if self.selected_adc_bits2 == "4":
                    print("hellochannel2")
                    if float(self.bandwidth_2) > ((0.9*61.44)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*61.44)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_2) > ((61.44)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((61.44)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return

                if self.selected_adc_bits1 == 8:
                    if float(self.bandwidth) > ((0.9*48)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*48)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_1) > ((48)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((48)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    
                if self.selected_adc_bits2 == "8":
                    if float(self.bandwidth_2) > ((0.9*48)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*48)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_2) > ((48)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((48)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return

                if self.selected_adc_bits1 == 16:
                    if float(self.bandwidth) > ((0.9*24)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*24)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_1) > ((24)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((24)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    
                if self.selected_adc_bits2 == "16":
                    if float(self.bandwidth_2) > ((0.9*24)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round((0.9*24)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    if float(self.samplingfreq_2) > ((24)/2):
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {round((24)/2, 2)}MHz")
                        msg_box_error_1.exec()
                        return
                    
                lo_value_1 = check_value_lo(self.selected_center_frequency1)
                if lo_value_1 == None:
                    msg_box_error_1 = QMessageBox()
                    msg_box_error_1.setWindowTitle("Invalid Data")
                    msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                    msg_box_error_1.exec()
                    return
                
                lo_value_2 = check_value_lo(self.selected_center_frequency2)
                if lo_value_2 == None:
                    msg_box_error_1 = QMessageBox()
                    msg_box_error_1.setWindowTitle("Invalid Data")
                    msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                    msg_box_error_1.exec()
                    return
                
                get_the_length = f"{self.file_name}_YYYY_MM_DD_HH_MM_SS"
                print(len(get_the_length))
                get_the_length = str(get_the_length).strip()
                valid, message = validate_file_and_folder_name_linux(get_the_length)
                if not valid:
                    msg_box_error_1 = QMessageBox()
                    msg_box_error_1.setWindowTitle("Error!")
                    msg_box_error_1.setText(f"{message}")
                    msg_box_error_1.exec()
                    return
                if file_name_starts_with_dot:
                    file_name_starts_with_dot = False
                    msg_box_compare = QMessageBox()
                    msg_box_compare.setWindowTitle("Warning")
                    msg_box_compare.setText("File name starts with a dot (.) and will be hidden")
                    msg_box_compare.setInformativeText("Hidden files are not visible during replay\nAre you sure you want to continue?")
                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                    reply_3 = msg_box_compare.exec()
                    if reply_3 == QMessageBox.StandardButton.No:
                        return
                    elif reply_3 == QMessageBox.StandardButton.Yes:
                        pass

                if float(self.samplingfreq_1) <= float(self.bandwidth):
                    msg_box_compare = QMessageBox()
                    msg_box_compare.setWindowTitle("Warning")
                    #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                    msg_box_compare.setInformativeText(f"Sampling frequency {self.samplingfreq_1} is not greater than bandwidth {self.bandwidth}.\nDo you want to continue?")
                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                    reply_3 = msg_box_compare.exec()
                    # Check the user's choice
                    if reply_3 == QMessageBox.StandardButton.Yes:
                        pass
                    else:
                        return
                    
                if float(self.samplingfreq_2) <= float(self.bandwidth_2):
                    msg_box_compare = QMessageBox()
                    msg_box_compare.setWindowTitle("Warning")
                    #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                    msg_box_compare.setInformativeText(f"Sampling frequency {self.samplingfreq_2} is not greater than bandwidth {self.bandwidth_2}.\nDo you want to continue?")
                    msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                    msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_compare.addButton(QMessageBox.StandardButton.No)
                    msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                    reply_3 = msg_box_compare.exec()
                    # Check the user's choice
                    if reply_3 == QMessageBox.StandardButton.Yes:
                        pass
                    else:
                        return
                    
                end_time = time.time()  # Record end time
                execution_time = end_time - start_time
                print(f"Execution Time before are you sure: {execution_time:.2f} seconds")
                msg_box_1 = QMessageBox()
                msg_box_1.setWindowTitle("Confirmation")
                msg_box_1.setText("Are you sure you want to start the recording?")
                msg_box_1.setIcon(QMessageBox.Icon.Question)
                msg_box_1.addButton(QMessageBox.StandardButton.Yes)
                msg_box_1.addButton(QMessageBox.StandardButton.No)
                msg_box_1.setDefaultButton(QMessageBox.StandardButton.No) 
                reply_2 = msg_box_1.exec()
                #
                # 
                # self.get_max_duration()

                if reply_2 == QMessageBox.StandardButton.Yes:
                    #self.get_max_duration()
                    
                    #lgTime_s = time_to_seconds(self.duration_value)
                    # Check memory availability
                    available_memory = SSD_free_space
                    #available_memory  = get_memory_available(fs_system)
                    mem_avail_time = memory_check_for_rx_log_2(available_memory, time_to_seconds(duration_valid), float(self.samplingfreq_1), int(self.selected_adc_bits1), float(self.samplingfreq_2), int(self.selected_adc_bits2))
                    if mem_avail_time > 0:
                        self.comboBox.setEnabled(False)
                        self.comboBox_2.setEnabled(False)
                        self.lineEdit_gain_1.setEnabled(False)
                        self.lineEdit_gain_2.setEnabled(False)
                        self.lineEdit_bandwidth.setEnabled(False)
                        self.lineEdit_bandwidth_2.setEnabled(False)
                        self.lineEdit_2.setEnabled(False)
                        self.lineEdit.setEnabled(False)
                        self.lineEdit_samplingfreq.setEnabled(False)
                        self.lineEdit_samplingfreq_2.setEnabled(False)
                        self.lineEdit_3.setEnabled(False)
                        self.lineEdit_4.setEnabled(False)
                        self.radioButton_Rx_1.setEnabled(False)
                        if self.radioButton_gpiomode.isChecked():
                           self.radioButton_GPIO_Record.setEnabled(False)
                        self.radioButton_Rx_2.setEnabled(False)
                        recording_started = True
                        self.comboBox_number_of_files.setEnabled(False)
                        self.red_light_record.setVisible(False)
                        self.green_light_record.setVisible(True)
                        self.lineEdit_gain_1.setEnabled(False)
                        self.lineEdit_gain_2.setEnabled(False)
                        self.lineEdit_2.setText(duration_valid)
                        duration = second_to_hhmmss(mem_avail_time)
                        self.lineEdit_2.setText(duration)
                        match_timer = True
                        self.worker.running = True  # Ensure the thread runs when started
                        self.worker.start() 
            
                        if self.selected_adc_bits1 is not None:
                            print("Selected ADC Bits of rx1:", self.selected_adc_bits1)
                        if self.selected_adc_bits2 is not None:
                            print("Selected ADC Bits of rx2:", self.selected_adc_bits2)
                        if self.file_name is not None:
                            print("Entered file name is:", self.file_name)
                        if self.selected_center_frequency1 is not None:
                            print("Entered center frequency of Rx1:", self.selected_center_frequency1)
                        if self.selected_center_frequency2 is not None:
                            print("Entered center frequency of Rx2:", self.selected_center_frequency2)
                        if self.bandwidth is not None:
                            print("Entered Bandwidth of Rx1:", self.bandwidth)
                        if self.bandwidth_2 is not None:
                            print("Entered Bandwidth of Rx2:", self.bandwidth_2)
                        if self.duration_value is not None:
                            print("Entered Duration is:", self.duration_value)
                            #print("Entered Duration in seconds is:", time_to_seconds(self.duration_value))
                        print("Duration to log in s is ",mem_avail_time)
                        
                        mode = 2
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
                       
                        final_string = (
                            f"{executable_rx} "                                # executable_rx
                            f"{mode} "           # Var1
                            f"{self.selected_center_frequency1}e6 "           # Var1
                            f"{self.selected_center_frequency2}e6 "           # Var2
                            f"{self.selected_adc_bits1} "                    # Var3
                            f"{self.selected_adc_bits2} "                    # Var3
                            f'"{Lg_path}"'                                   # Var3
                            f'"{self.file_name}_{current_time}.bin" '
                            f"{mem_avail_time} " 
                            f"{self.bandwidth}e6 "                               
                            f"{self.bandwidth_2}e6 " 
                            f"{self.samplingfreq_1}e6 "                              
                            f"{self.samplingfreq_2}e6 "                                                              
                            f"{gain} "                               
                            f"{gain_2} " 
                            f"{self.reference_frequency} "                                                                # Var3
                            f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log" \n'
                        )
                        #print("the command is ",final_string)
                        if checked_both_without_HWUSB:
                            comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                            if not comport_2_rtcm:
                                msg_box_2 = QMessageBox()
                                msg_box_2.setWindowTitle("Missing Data")
                                msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                                msg_box_2.exec()
                                self.open_after_disconnection()
                                return           
                            try:
                                rtcm_create_file = f'{rtcm_folder_path}/{self.file_name}_{current_time}.rtcm'
                                with open(rtcm_create_file, 'w'):
                                    pass
                            except PermissionError as e:
                                                        self.comboBox.setEnabled(True)
                                                        self.comboBox_2.setEnabled(True)
                                                        self.lineEdit_gain_1.setEnabled(True)
                                                        self.lineEdit_gain_2.setEnabled(True)
                                                        self.lineEdit_bandwidth.setEnabled(True)
                                                        self.lineEdit_bandwidth_2.setEnabled(True)
                                                        self.lineEdit_2.setEnabled(True)
                                                        self.lineEdit.setEnabled(True)
                                                        self.lineEdit_samplingfreq.setEnabled(True)
                                                        self.lineEdit_samplingfreq_2.setEnabled(True)
                                                        self.lineEdit_3.setEnabled(True)
                                                        self.lineEdit_4.setEnabled(True)
                                                        self.radioButton_Rx_1.setEnabled(True)
                                                        if self.radioButton_gpiomode.isChecked():
                                                            self.radioButton_GPIO_Record.setEnabled(True)
                                                        self.radioButton_Rx_2.setEnabled(True)
                                                        recording_started = False
                                                        self.comboBox_number_of_files.setEnabled(True)
                                                        self.red_light_record.setVisible(True)
                                                        self.stop_GPIO_record_replay()
                                                        self.green_light_record.setVisible(False)
                                                        self.worker.stop()  # Tell the thread to stop
                                                        self.worker.wait()
                                                        self.worker.running = False
                                                        msg_box_11 = QMessageBox()
                                                        msg_box_11.setWindowTitle("Error!")
                                                        msg_box_11.setText(f"Permission denied! Recording not started!\nYou cannot select this folder for RTCM recording!")
                                                        msg_box_11.exec()     
                                                        return
                            
                        comport_is_active = interface_is_online(self.comport)
                        if HW_USB_in_use:
                            record_folder_path = f"{rtcm_folder_path}{self.file_name}_{current_time}"
                            self.rtcm_record_command(record_folder_path)
                        if comport_is_active: 
                            self.GPIO_record_replay(Lg_path, f"{self.file_name}_{current_time}.gpio", mem_avail_time, 0)
                            send_command(bytearray(final_string,'ascii')) 
                            recording_thread = threading.Thread(target=check_recording)
                            recording_thread.start()  
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   {final_string}")
                            
                        else:
                            self.comboBox.setEnabled(True)
                            self.comboBox_2.setEnabled(True)
                            self.lineEdit_gain_1.setEnabled(True)
                            self.lineEdit_gain_2.setEnabled(True)
                            self.lineEdit_bandwidth.setEnabled(True)
                            self.lineEdit_bandwidth_2.setEnabled(True)
                            self.lineEdit_2.setEnabled(True)
                            self.lineEdit.setEnabled(True)
                            self.lineEdit_samplingfreq.setEnabled(True)
                            self.lineEdit_samplingfreq_2.setEnabled(True)
                            self.lineEdit_3.setEnabled(True)
                            self.lineEdit_4.setEnabled(True)
                            self.radioButton_Rx_1.setEnabled(True)
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Record.setEnabled(True)
                            self.radioButton_Rx_2.setEnabled(True)
                            recording_started = False
                            self.comboBox_number_of_files.setEnabled(True)
                            self.red_light_record.setVisible(True)
                            self.green_light_record.setVisible(False)
                            self.worker.stop()  # Tell the thread to stop
                            self.worker.wait()
                            self.worker.running = False
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"COM port got disconnected!, Could not Start the Recording!")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                      
                        lines = read_lines()
                        print(f'12{lines}')
                        decoded_lines = [line.decode() for line in lines]
                        print(decoded_lines)
                     
                        for line in decoded_lines:
                            if "Recorded time:" in line:
                                print(line)
                                print("hiiiiiii")
                                recorded_time = True
                            if "Destroying" in line:
                                print(line)
                                print("hiiiiiii123")
                                if not recorded_time:
                                    print("hiiiiiii123")
                                    recorded_time = False
                                    self.comboBox.setEnabled(True)
                                    self.comboBox_2.setEnabled(True)
                                    self.lineEdit_gain_1.setEnabled(True)
                                    self.lineEdit_gain_2.setEnabled(True)
                                    self.lineEdit_bandwidth.setEnabled(True)
                                    self.lineEdit_bandwidth_2.setEnabled(True)
                                    self.lineEdit_2.setEnabled(True)
                                    self.lineEdit.setEnabled(True)
                                    self.lineEdit_samplingfreq.setEnabled(True)
                                    self.lineEdit_samplingfreq_2.setEnabled(True)
                                    self.lineEdit_3.setEnabled(True)
                                    self.lineEdit_4.setEnabled(True)
                                    self.radioButton_Rx_1.setEnabled(True)
                                    if self.radioButton_gpiomode.isChecked():
                                        self.radioButton_GPIO_Record.setEnabled(True)
                                    self.radioButton_Rx_2.setEnabled(True)
                                    recording_started = False
                                    read_response = False
                                    self.comboBox_number_of_files.setEnabled(True)
                                    self.red_light_record.setVisible(True)
                                    self.stop_GPIO_record_replay()
                                    self.green_light_record.setVisible(False)
                                    self.worker.stop()  # Tell the thread to stop
                                    self.worker.wait()
                                    self.worker.running = False
                                    msg_box_11 = QMessageBox()
                                    msg_box_11.setWindowTitle("Error!")
                                    msg_box_11.setText(f"Error occured! Recording not started!")
                                    msg_box_11.exec()     
                                    return
                            
                        recording_dual_channel = True
                        recording_rx1_channel = False
                        recording_rx2_channel = False
                        
                      #  time.sleep(1)
                        # Start the timer only if memory is sufficient
                        self.elapsed_time = QtCore.QTime(0, 0)
                        self.timer.start(1000)  # Update every 1 second
                        self.timer_started = True
                        self.lineEdit_2.setEnabled(False)  # Disable editing
                        self.update_timer()
                        self.label_current_file.setText("1")
                        self.label_current_file.setStyleSheet("color: #1ABC9C;") 
                                   
                elif reply_2 == QMessageBox.StandardButton.No:
                    print("Selected No")
                    #self.get_max_duration()

            elif rx1_checked:
                start_time = time.time()  # Record start time
                print("hii")
                if self.radioButton_Rx_1.isChecked():
                    if (self.selected_adc_bits1 is None or
                            self.file_name is None or
                            self.selected_center_frequency1 is None or
                            self.bandwidth is None or
                            self.duration_value is None or
                            self.samplingfreq_1 is None or
                            self.folder_name_record is None):
                        #print("Condition met!")

                        if not self.msg_box_2_shown:
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Missing Data")
                            msg_box_2.setText("Please enter all the required data before starting the recording")
                            msg_box_2.exec()
                            self.msg_box_2_shown = True  # Set the flag to True after showing the message box
                        return
                    
                    gain = str(self.lineEdit_gain_1.text()).strip()
                    print(gain)
                    if gain == None or gain == "":
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Missing Data")
                            msg_box_2.setText("Please enter all the required data before starting the recording")
                            msg_box_2.exec()
                            return
                    
                    if gain.lower() in ("slow attack", "slowattack"):
                        print("hii")
                        gain = 100
                        print(gain)
                        #self.lineEdit_gain_1.setText("Slow attack")
                    elif gain.lower() in ("fast attack", "fastattack"):
                        gain = 200
                        #self.lineEdit_gain_1.setText("Fast attack")
                    elif gain.lower() == "hybrid":
                        gain = 300
                    else:
                        try:
                            print(gain)
                            gain = float(gain)
                        except ValueError:
                                msg_box_2 = QMessageBox()
                                msg_box_2.setWindowTitle("error")
                                msg_box_2.setText("please enter a valid Gain")
                                msg_box_2.exec() 
                                return 
                    if gain == 100:
                        self.lineEdit_gain_1.setText("Slow attack")
                    elif gain == 200:
                        self.lineEdit_gain_1.setText("Fast attack") 
                    elif gain == 300:
                        self.lineEdit_gain_1.setText("Hybrid")
                    
                    if (not (-10 <= gain <= 73)) and gain not in {100, 200, 300}:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Error!")
                        msg_box_2.setText("Gain should be between -10dB and 73dB, except 100, 200, 300")
                        msg_box_2.exec()
                        return


                    if str(self.file_name) == "":
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("missing file name")
                        msg_box_2.setText("please enter the file name")
                        msg_box_2.exec() 
                        return
                    
                    duration_valid = validate_time(self.duration_value)
                    print(duration_valid)
                    if duration_valid == None:
                        msg_box_error = QMessageBox()
                        msg_box_error.setWindowTitle("Invalid Format")
                        msg_box_error.setText("Duration value is in a wrong format")
                        msg_box_error.exec()
                        return

                    try:
                        self.bandwidth = float(self.bandwidth)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data Type")
                            msg_box_error_1.setText("Bandwidth must be numeric values")
                            msg_box_error_1.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    try:
                        self.selected_center_frequency1 = float(self.selected_center_frequency1)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error = QMessageBox()
                            msg_box_error.setWindowTitle("Invalid Data Type")
                            msg_box_error.setText("Center frequency must be numeric values")
                            msg_box_error.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    try:
                        self.samplingfreq_1 = float(self.samplingfreq_1)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error = QMessageBox()
                            msg_box_error.setWindowTitle("Invalid Data Type")
                            msg_box_error.setText("Sampling Frequency must be numeric values")
                            msg_box_error.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    
                    
                    if self.selected_adc_bits1 == 4:
                        if float(self.bandwidth) > (0.9*61.44):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round(0.9*61.44, 2)}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_1) > (61.44):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {61.44}MHz")
                            msg_box_error_1.exec()
                            return

                    if self.selected_adc_bits1 == 8:
                        if float(self.bandwidth) > (0.9*48):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round(0.9*48, 2)}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_1) > (48):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {48}MHz")
                            msg_box_error_1.exec()
                            return

                    if self.selected_adc_bits1 == 16:
                        if float(self.bandwidth) > (0.9*24):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round(0.9*24, 2)}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_1) > (24):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {24}MHz")
                            msg_box_error_1.exec()
                            return
                        
                    lo_value_1 = check_value_lo(self.selected_center_frequency1)
                    if lo_value_1 == None:
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                        msg_box_error_1.exec()
                        return
                    
                        
                    get_the_length = f"{self.file_name}_YYYY_MM_DD_HH_MM_SS"
                    get_the_length = str(get_the_length).strip()
                    valid, message = validate_file_and_folder_name_linux(get_the_length)
                    if not valid:
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Error!")
                        msg_box_error_1.setText(f"{message}")
                        msg_box_error_1.exec()
                        return
                    
                    if file_name_starts_with_dot:
                        file_name_starts_with_dot = False
                        msg_box_compare = QMessageBox()
                        msg_box_compare.setWindowTitle("Warning")
                        msg_box_compare.setText("File name starts with a dot (.) and will be hidden")
                        msg_box_compare.setInformativeText("Hidden files are not visible during replay\nAre you sure you want to continue?")
                        msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                        msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                        msg_box_compare.addButton(QMessageBox.StandardButton.No)
                        msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                        reply_3 = msg_box_compare.exec()
                        if reply_3 == QMessageBox.StandardButton.No:
                            return
                        elif reply_3 == QMessageBox.StandardButton.Yes:
                            pass

                    if self.samplingfreq_1 <= self.bandwidth:
                        msg_box_compare = QMessageBox()
                        msg_box_compare.setWindowTitle("Warning")
                        #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                        msg_box_compare.setInformativeText("Sampling frequency is not greater than bandwidth.\nDo you want to continue?")
                        msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                        msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                        msg_box_compare.addButton(QMessageBox.StandardButton.No)
                        msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                        reply_3 = msg_box_compare.exec()
                        # Check the user's choice
                        if reply_3 == QMessageBox.StandardButton.Yes:
                            pass
                        else:
                            return

                    end_time = time.time()  # Record end time
                    execution_time = end_time - start_time
                    print(f"{start_time}, {end_time}")
                    print(f"Execution Time before are you sure: {execution_time:.2f} seconds")
                    msg_box_1 = QMessageBox()
                    msg_box_1.setWindowTitle("Confirmation")
                    msg_box_1.setText("Are you sure you want to start the recording?")
                    msg_box_1.setIcon(QMessageBox.Icon.Question)
                    msg_box_1.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_1.addButton(QMessageBox.StandardButton.No)
                    msg_box_1.setDefaultButton(QMessageBox.StandardButton.No) 
                    reply_2 = msg_box_1.exec()

                    if reply_2 == QMessageBox.StandardButton.Yes:
                        #self.get_max_duration()
                        
                        available_memory  = SSD_free_space
                        mem_avail_time = memory_check_for_rx_log(available_memory, time_to_seconds(duration_valid), float(self.samplingfreq_1), int(self.selected_adc_bits1))
                        if mem_avail_time > 0:
                            self.comboBox.setEnabled(False)
                            self.comboBox_2.setEnabled(False)
                            self.lineEdit_gain_1.setEnabled(False)
                            self.lineEdit_gain_2.setEnabled(False)
                            self.lineEdit_bandwidth.setEnabled(False)
                            self.lineEdit_bandwidth_2.setEnabled(False)
                            self.lineEdit_2.setEnabled(False)
                            self.lineEdit.setEnabled(False)
                            self.lineEdit_samplingfreq.setEnabled(False)
                            self.lineEdit_samplingfreq_2.setEnabled(False)
                            self.lineEdit_3.setEnabled(False)
                            self.lineEdit_4.setEnabled(False)
                            self.radioButton_Rx_1.setEnabled(False)
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Record.setEnabled(False)
                            self.radioButton_Rx_2.setEnabled(False)
                            recording_started = True
                            self.comboBox_number_of_files.setEnabled(False)
                            self.red_light_record.setVisible(False)
                            self.green_light_record.setVisible(True)
                            self.lineEdit_2.setText(duration_valid)
                            duration = second_to_hhmmss(mem_avail_time)
                            self.lineEdit_2.setText(duration)
                            self.worker.running = True  # Ensure the thread runs when started
                            self.worker.start()
                            ########################################################################
                            #self.get_max_duration()
                            ####################################################################################
                            if self.selected_adc_bits1 is not None:
                                print("Selected ADC Bits of rx1:", self.selected_adc_bits1)
                            if self.file_name is not None:
                                print("Entered file name is:", self.file_name)
                            if self.selected_center_frequency1 is not None:
                                print("Entered center frequency of Rx1:", self.selected_center_frequency1)
                            if self.bandwidth is not None:
                                print("Entered Bandwidth of Rx1:", self.bandwidth)
                            if self.duration_value is not None:
                                print("Entered Duration is:", self.duration_value)
                                #print("Entered Duration in seconds is:", time_to_seconds(self.duration_value))
                            print("Duration to log in s is ",mem_avail_time)

                            if not self.ensure_interface_connection(timeout_time, show_disconnection_dialog=True):
                                return
                            
                            mode = 0
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                            #gain = 60
                            #gain_2 = 60
                            
                            final_string = (
                                f"{executable_rx} "                                # executable_rx
                                f"{mode} "           # Var1
                                f"{self.selected_center_frequency1}e6 "           # Var1
                                f"{self.selected_center_frequency1}e6 "           # Var2
                                f"{self.selected_adc_bits1} "                    # Var3
                                f"{self.selected_adc_bits1} "                    # Var3
                                f'"{Lg_path}"'                                    # Var3
                                f'"{self.file_name}_{current_time}.bin" '
                                f"{mem_avail_time} " 
                                f"{self.bandwidth}e6 "                               
                                f"{self.bandwidth}e6 " 
                                f"{self.samplingfreq_1}e6 "                              
                                f"{self.samplingfreq_1}e6 "                                                              
                                f"{gain} "                               
                                f"{gain} "
                                f"{self.reference_frequency} "                                                                 # Var3
                                f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log"\n'
                            )
                            print("the command is ",final_string)
                            if checked_both_without_HWUSB:
                                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                                if not comport_2_rtcm:
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Missing Data")
                                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                                    msg_box_2.exec()
                                    self.open_after_disconnection()
                                    return
                                try:
                                    rtcm_create_file = f'{rtcm_folder_path}/{self.file_name}_{current_time}.rtcm'
                                    with open(rtcm_create_file, 'w'):
                                        pass
                                except PermissionError as e:
                                                            self.comboBox.setEnabled(True)
                                                            self.comboBox_2.setEnabled(True)
                                                            self.lineEdit_gain_1.setEnabled(True)
                                                            self.lineEdit_gain_2.setEnabled(True)
                                                            self.lineEdit_bandwidth.setEnabled(True)
                                                            self.lineEdit_bandwidth_2.setEnabled(True)
                                                            self.lineEdit_2.setEnabled(True)
                                                            self.lineEdit.setEnabled(True)
                                                            self.lineEdit_samplingfreq.setEnabled(True)
                                                            self.lineEdit_samplingfreq_2.setEnabled(True)
                                                            self.lineEdit_3.setEnabled(True)
                                                            self.lineEdit_4.setEnabled(True)
                                                            self.radioButton_Rx_1.setEnabled(True)
                                                            if self.radioButton_gpiomode.isChecked():
                                                                self.radioButton_GPIO_Record.setEnabled(True)
                                                            self.radioButton_Rx_2.setEnabled(True)
                                                            recording_started = False
                                                            self.worker.stop()  # Tell the thread to stop
                                                            self.worker.wait()
                                                            self.worker.running = False
                                                            self.comboBox_number_of_files.setEnabled(True)
                                                            self.red_light_record.setVisible(True)
                                                            self.stop_GPIO_record_replay()
                                                            self.green_light_record.setVisible(False)
                                                            msg_box_11 = QMessageBox()
                                                            msg_box_11.setWindowTitle("Error!")
                                                            msg_box_11.setText(f"Permission denied! Recording not started!\nYou cannot select this folder for RTCM recording!")
                                                            msg_box_11.exec()     
                                                            return
                            
                            
                            comport_is_active = interface_is_online(self.comport)
                            if HW_USB_in_use:
                                record_folder_path = f"{rtcm_folder_path}{self.file_name}_{current_time}"
                                self.rtcm_record_command(record_folder_path)
                            if comport_is_active: 
                                self.GPIO_record_replay(Lg_path, f"{self.file_name}_{current_time}.gpio", mem_avail_time, 0)
                                send_command(bytearray(final_string,'ascii'))   
                                recording_thread = threading.Thread(target=check_recording)
                                recording_thread.start() 
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   {final_string}")
                                lines = read_lines()
                                decoded_lines = [line.decode() for line in lines]
                                
                            else:
                                self.comboBox.setEnabled(True)
                                self.comboBox_2.setEnabled(True)
                                self.lineEdit_gain_1.setEnabled(True)
                                self.lineEdit_gain_2.setEnabled(True)
                                self.lineEdit_bandwidth.setEnabled(True)
                                self.lineEdit_bandwidth_2.setEnabled(True)
                                self.lineEdit_2.setEnabled(True)
                                self.lineEdit.setEnabled(True)
                                self.lineEdit_samplingfreq.setEnabled(True)
                                self.lineEdit_samplingfreq_2.setEnabled(True)
                                self.lineEdit_3.setEnabled(True)
                                self.lineEdit_4.setEnabled(True)
                                self.radioButton_Rx_1.setEnabled(True)
                                if self.radioButton_gpiomode.isChecked():
                                    self.radioButton_GPIO_Record.setEnabled(True)
                                self.radioButton_Rx_2.setEnabled(True)
                                self.worker.stop()  # Tell the thread to stop
                                self.worker.wait()
                                self.worker.running = False
                                recording_started = False
                                self.comboBox_number_of_files.setEnabled(True)
                                self.red_light_record.setVisible(True)
                                self.green_light_record.setVisible(False)
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, Could not start the Recording!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return
                            
                            print(decoded_lines)
                            for line in decoded_lines:
                                if "Recorded time:" in line:
                                    print(line)
                                    recorded_time = True
                                if "Destroying" in line:
                                    print(line)
                                    if not recorded_time:
                                        recorded_time = False
                                        self.comboBox.setEnabled(True)
                                        self.comboBox_2.setEnabled(True)
                                        self.lineEdit_gain_1.setEnabled(True)
                                        self.lineEdit_gain_2.setEnabled(True)
                                        self.lineEdit_bandwidth.setEnabled(True)
                                        self.lineEdit_bandwidth_2.setEnabled(True)
                                        self.lineEdit_2.setEnabled(True)
                                        self.lineEdit.setEnabled(True)
                                        self.lineEdit_samplingfreq.setEnabled(True)
                                        self.lineEdit_samplingfreq_2.setEnabled(True)
                                        self.lineEdit_3.setEnabled(True)
                                        self.lineEdit_4.setEnabled(True)
                                        self.radioButton_Rx_1.setEnabled(True)
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Record.setEnabled(True)
                                        self.radioButton_Rx_2.setEnabled(True)
                                        recording_started = False
                                        read_response = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        self.comboBox_number_of_files.setEnabled(True)
                                        self.red_light_record.setVisible(True)
                                        self.stop_GPIO_record_replay()
                                        self.green_light_record.setVisible(False)
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"Error occured! Recording not started!")
                                        msg_box_11.exec()     
                                        return
                            
                            recording_dual_channel = False
                            recording_rx1_channel = True
                            recording_rx2_channel = False
                            
                         #   time.sleep(1)
                            # Start the timer only if memory is sufficient
                            self.elapsed_time = QtCore.QTime(0, 0)
                            self.timer.start(1000)  # Update every 1 second
                            self.timer_started = True
                            self.lineEdit_2.setEnabled(False)  # Disable editing
                            self.update_timer()
                            self.label_current_file.setText("1")
                            self.label_current_file.setStyleSheet("color: #1ABC9C;") 
                    elif reply_2 == QMessageBox.StandardButton.No:
                        print("Selected No")
                        #self.get_max_duration()

            elif rx2_checked:
                    if (self.selected_adc_bits2 is None or
                            self.file_name is None or
                            self.selected_center_frequency2 is None or
                            self.bandwidth_2 is None or
                            self.duration_value is None or
                            self.samplingfreq_2 is None or
                            self.folder_name_record is None):
                        #print("Condition met!")

                        if not self.msg_box_2_shown:
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Missing Data")
                            msg_box_2.setText("Please enter all the required data before starting the recording")
                            msg_box_2.exec()
                            self.msg_box_2_shown = True  # Set the flag to True after showing the message box
                        return
                    gain_2 = self.lineEdit_gain_2.text()
                    if gain_2 == None or gain_2 == "":
                            msg_box_2 = QMessageBox()
                            msg_box_2.setWindowTitle("Missing Data")
                            msg_box_2.setText("Please enter all the required data before starting the recording")
                            msg_box_2.exec()
                            return

                    if gain_2.lower() in ("slow attack", "slowattack"):
                        gain_2 = 100
                        #self.lineEdit_gain_1.setText("Slow attack")
                    elif gain_2.lower() in ("fast attack", "fastattack"):
                        gain_2 = 200
                        #self.lineEdit_gain_1.setText("Fast attack")
                    elif gain_2.lower() == "hybrid":
                        gain_2 = 300
                    else:
                        try:
                            gain_2 = float(gain_2)
                        except ValueError:
                                msg_box_2 = QMessageBox()
                                msg_box_2.setWindowTitle("error")
                                msg_box_2.setText("please enter a valid Gain")
                                msg_box_2.exec() 
                                return 
                    if gain_2 == 100:
                        self.lineEdit_gain_2.setText("Slow attack")
                    elif gain_2 == 200:
                        self.lineEdit_gain_2.setText("Fast attack") 
                    elif gain_2 == 300:
                        self.lineEdit_gain_2.setText("Hybrid") 
                    
                    if (not (-10 <= gain_2 <= 73)) and gain_2 not in {100, 200, 300}:
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("Error!")
                        msg_box_2.setText("Gain should be between -10dB and 73dB, except 100, 200, 300")
                        msg_box_2.exec()
                        return
                    
                    if str(self.file_name) == "":
                        msg_box_2 = QMessageBox()
                        msg_box_2.setWindowTitle("missing file name")
                        msg_box_2.setText("please enter the file name")
                        msg_box_2.exec() 
                        return
                    duration_valid = validate_time(self.duration_value)
                    print(duration_valid)
                    if duration_valid == None:
                        msg_box_error = QMessageBox()
                        msg_box_error.setWindowTitle("Invalid Format")
                        msg_box_error.setText("Duration value is in a wrong format")
                        msg_box_error.exec()
                        return

                    try:
                        self.bandwidth_2 = float(self.bandwidth_2)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data Type")
                            msg_box_error_1.setText("Bandwidth must be numeric values")
                            msg_box_error_1.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    try:
                        self.selected_center_frequency2 = float(self.selected_center_frequency2)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error = QMessageBox()
                            msg_box_error.setWindowTitle("Invalid Data Type")
                            msg_box_error.setText("Center frequency must be numeric values")
                            msg_box_error.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    try:
                        self.samplingfreq_2 = float(self.samplingfreq_2)
                    except ValueError:
                        if not self.msg_box_error_shown:
                            msg_box_error = QMessageBox()
                            msg_box_error.setWindowTitle("Invalid Data Type")
                            msg_box_error.setText("Sampling Frequency must be numeric values")
                            msg_box_error.exec()
                            self.msg_box_error_shown = True
                        return
                    
                    

                    print(self.selected_adc_bits2)
                    if self.selected_adc_bits2 == "4":
                        if float(self.bandwidth_2) > (0.9*61.44):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {0.9*61.44}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_2) > (61.44):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {61.44}MHz")
                            msg_box_error_1.exec()
                            return

                    if self.selected_adc_bits2 == "8":
                        if float(self.bandwidth_2) > (0.9*48):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round(0.9*48, 2)}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_2) > (48):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {48}MHz")
                            msg_box_error_1.exec()
                            return

                    if self.selected_adc_bits2 == "16":
                        if float(self.bandwidth_2) > (0.9*24):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Bandwidth is greater than the maximum bandwidth: {round(0.9*24, 2)}MHz")
                            msg_box_error_1.exec()
                            return
                        if float(self.samplingfreq_2) > (24):
                            msg_box_error_1 = QMessageBox()
                            msg_box_error_1.setWindowTitle("Invalid Data")
                            msg_box_error_1.setText(f"Entered Sampling frequency is greater than the maximum Sampling frequency: {24}MHz")
                            msg_box_error_1.exec()
                            return

                    
                    lo_value_2 = check_value_lo(self.selected_center_frequency2)
                    if lo_value_2 == None:
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Invalid Data")
                        msg_box_error_1.setText(f"Central frequency should be greater than 70e6 and less than 6e9")
                        msg_box_error_1.exec()
                        return

                    get_the_length = f"{self.file_name}_YYYY_MM_DD_HH_MM_SS"
                    get_the_length = str(get_the_length).strip()
                    valid, message = validate_file_and_folder_name_linux(get_the_length)
                    if not valid:
                        msg_box_error_1 = QMessageBox()
                        msg_box_error_1.setWindowTitle("Error!")
                        msg_box_error_1.setText(f"{message}")
                        msg_box_error_1.exec()
                        return
                    
                    if file_name_starts_with_dot:
                        file_name_starts_with_dot = False
                        msg_box_compare = QMessageBox()
                        msg_box_compare.setWindowTitle("Warning")
                        msg_box_compare.setText("File name starts with a dot (.) and will be hidden")
                        msg_box_compare.setInformativeText("Hidden files are not visible during replay\nAre you sure you want to continue?")
                        msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                        msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                        msg_box_compare.addButton(QMessageBox.StandardButton.No)
                        msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                        reply_3 = msg_box_compare.exec()
                        if reply_3 == QMessageBox.StandardButton.No:
                            return
                        elif reply_3 == QMessageBox.StandardButton.Yes:
                            pass
                    
                    if self.samplingfreq_2 <= self.bandwidth_2:
                        msg_box_compare = QMessageBox()
                        msg_box_compare.setWindowTitle("Warning")
                        #msg_box_compare.setText("Memory available for only {}.".format(seconds_to_hhmmss(mem_avail_time)))
                        msg_box_compare.setInformativeText("Sampling frequency is not greater than bandwidth.\nDo you want to continue?")
                        msg_box_compare.setIcon(QMessageBox.Icon.Warning)
                        msg_box_compare.addButton(QMessageBox.StandardButton.Yes)
                        msg_box_compare.addButton(QMessageBox.StandardButton.No)
                        msg_box_compare.setDefaultButton(QMessageBox.StandardButton.Yes)
                        reply_3 = msg_box_compare.exec()
                        # Check the user's choice
                        if reply_3 == QMessageBox.StandardButton.Yes:
                            pass
                        else:
                            return

                    msg_box_1 = QMessageBox()
                    msg_box_1.setWindowTitle("Confirmation")
                    msg_box_1.setText("Are you sure you want to start the recording?")
                    msg_box_1.setIcon(QMessageBox.Icon.Question)
                    msg_box_1.addButton(QMessageBox.StandardButton.Yes)
                    msg_box_1.addButton(QMessageBox.StandardButton.No)
                    msg_box_1.setDefaultButton(QMessageBox.StandardButton.No) 
                    reply_2 = msg_box_1.exec()

                    if reply_2 == QMessageBox.StandardButton.Yes:
                    

                        available_memory  = SSD_free_space
                        mem_avail_time = memory_check_for_rx_log(available_memory, time_to_seconds(duration_valid), float(self.samplingfreq_2), int(self.selected_adc_bits2))
                        if mem_avail_time > 0:
                            self.comboBox.setEnabled(False)
                            self.comboBox_2.setEnabled(False)
                            self.lineEdit_gain_1.setEnabled(False)
                            self.lineEdit_gain_2.setEnabled(False)
                            self.lineEdit_bandwidth.setEnabled(False)
                            self.lineEdit_bandwidth_2.setEnabled(False)
                            self.lineEdit_2.setEnabled(False)
                            self.lineEdit.setEnabled(False)
                            self.lineEdit_samplingfreq.setEnabled(False)
                            self.lineEdit_samplingfreq_2.setEnabled(False)
                            self.lineEdit_3.setEnabled(False)
                            self.lineEdit_4.setEnabled(False)
                            self.radioButton_Rx_1.setEnabled(False)
                            if self.radioButton_gpiomode.isChecked():
                                self.radioButton_GPIO_Record.setEnabled(False)
                            self.radioButton_Rx_2.setEnabled(False)
                            recording_started = True
                            self.comboBox_number_of_files.setEnabled(False)
                            self.red_light_record.setVisible(False)
                            self.green_light_record.setVisible(True)
                            self.lineEdit_2.setText(duration_valid)
                            duration = second_to_hhmmss(mem_avail_time)
                            self.lineEdit_2.setText(duration)
                            self.worker.running = True  # Ensure the thread runs when started
                            self.worker.start()
                            # Start the timer only if memory is sufficient
                            
                            if self.selected_adc_bits2 is not None:
                                print("Selected ADC Bits of rx1:", self.selected_adc_bits2)
                            if self.file_name is not None:
                                print("Entered file name is:", self.file_name)
                            if self.selected_center_frequency2 is not None:
                                print("Entered center frequency of Rx1:", self.selected_center_frequency2)
                            if self.bandwidth_2 is not None:
                                print("Entered Bandwidth of Rx1:", self.bandwidth_2)
                            if self.duration_value is not None:
                                print("Entered Duration is:", self.duration_value)
                                ##print("Entered Duration in seconds is:", time_to_seconds(self.duration_value))
                            print("Duration to log in s is ",mem_avail_time)
                            mode = 4
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                            #gain = 60
                            #gain = abs(gain)
                            #gain_2 = abs(gain_2)
                            #gain_2 = 60
                            
                            final_string = (
                                f"{executable_rx} "                                # executable_rx
                                f"{mode} "           # Var1
                                f"{self.selected_center_frequency2}e6 "           # Var1
                                f"{self.selected_center_frequency2}e6 "           # Var2
                                f"{self.selected_adc_bits2} "                    # Var3
                                f"{self.selected_adc_bits2} "                    # Var3
                                f'"{Lg_path}"'                                    # Var3
                                f'"{self.file_name}_{current_time}.bin" '
                                f"{mem_avail_time} " 
                                f"{self.bandwidth_2}e6 "                               
                                f"{self.bandwidth_2}e6 " 
                                f"{self.samplingfreq_2}e6 "                              
                                f"{self.samplingfreq_2}e6 "                                                              
                                f"{gain_2} "                               
                                f"{gain_2} "
                                f"{self.reference_frequency} "                                                                 # Var3
                                f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log" \n'
                            )
                            print("the command is ",final_string)
                            if checked_both_without_HWUSB:
                                comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
                                if not comport_2_rtcm:
                                    msg_box_2 = QMessageBox()
                                    msg_box_2.setWindowTitle("Missing Data")
                                    msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                                    msg_box_2.exec()
                                    self.open_after_disconnection()
                                    return
                                try:
                                    rtcm_create_file = f'{rtcm_folder_path}/{self.file_name}_{current_time}.rtcm'
                                    with open(rtcm_create_file, 'w'):
                                        pass
                                except PermissionError as e:
                                                            self.comboBox.setEnabled(True)
                                                            self.comboBox_2.setEnabled(True)
                                                            self.lineEdit_gain_1.setEnabled(True)
                                                            self.lineEdit_gain_2.setEnabled(True)
                                                            self.lineEdit_bandwidth.setEnabled(True)
                                                            self.lineEdit_bandwidth_2.setEnabled(True)
                                                            self.lineEdit_2.setEnabled(True)
                                                            self.lineEdit.setEnabled(True)
                                                            self.lineEdit_samplingfreq.setEnabled(True)
                                                            self.lineEdit_samplingfreq_2.setEnabled(True)
                                                            self.lineEdit_3.setEnabled(True)
                                                            self.lineEdit_4.setEnabled(True)
                                                            self.radioButton_Rx_1.setEnabled(True)
                                                            if self.radioButton_gpiomode.isChecked():
                                                                self.radioButton_GPIO_Record.setEnabled(True)
                                                            self.radioButton_Rx_2.setEnabled(True)
                                                            recording_started = False
                                                            self.worker.stop()  # Tell the thread to stop
                                                            self.worker.wait()
                                                            self.worker.running = False
                                                            self.comboBox_number_of_files.setEnabled(True)
                                                            self.red_light_record.setVisible(True)
                                                            self.stop_GPIO_record_replay()
                                                            self.green_light_record.setVisible(False)
                                                            msg_box_11 = QMessageBox()
                                                            msg_box_11.setWindowTitle("Error!")
                                                            msg_box_11.setText(f"Permission denied! Recording not started!\nYou cannot select this folder for RTCM recording!")
                                                            msg_box_11.exec()     
                                                            return
                                
                            comport_is_active = interface_is_online(self.comport)
                            if HW_USB_in_use:
                                record_folder_path = f"{rtcm_folder_path}{self.file_name}_{current_time}"
                                self.rtcm_record_command(record_folder_path)
                            if comport_is_active: 
                                self.GPIO_record_replay(Lg_path, f"{self.file_name}_{current_time}.gpio", mem_avail_time, 0)
                                send_command(bytearray(final_string,'ascii')) 
                                recording_thread = threading.Thread(target=check_recording)
                                recording_thread.start() 
                                if Commands_file_user:
                                    with open(file_path, 'a') as file:
                                        file.write(f"\n{get_current_datetime()}   {final_string}")
                                lines = read_lines()
                                decoded_lines = [line.decode() for line in lines]
                            else:
                                self.comboBox.setEnabled(True)
                                self.comboBox_2.setEnabled(True)
                                self.lineEdit_gain_1.setEnabled(True)
                                self.lineEdit_gain_2.setEnabled(True)
                                self.lineEdit_bandwidth.setEnabled(True)
                                self.lineEdit_bandwidth_2.setEnabled(True)
                                self.lineEdit_2.setEnabled(True)
                                self.lineEdit.setEnabled(True)
                                self.lineEdit_samplingfreq.setEnabled(True)
                                self.lineEdit_samplingfreq_2.setEnabled(True)
                                self.lineEdit_3.setEnabled(True)
                                self.lineEdit_4.setEnabled(True)
                                self.radioButton_Rx_1.setEnabled(True)
                                if self.radioButton_gpiomode.isChecked():
                                    self.radioButton_GPIO_Record.setEnabled(True)
                                self.radioButton_Rx_2.setEnabled(True)
                                recording_started = False
                                self.worker.stop()  # Tell the thread to stop
                                self.worker.wait()
                                self.worker.running = False
                                self.comboBox_number_of_files.setEnabled(True)
                                self.red_light_record.setVisible(True)
                                self.green_light_record.setVisible(False)
                                msg_box_11 = QMessageBox()
                                msg_box_11.setWindowTitle("Error!")
                                msg_box_11.setText(f"COM port got disconnected!, could not start the Recording!")
                                msg_box_11.exec()
                                self.open_after_disconnection()
                                return

                            #print(decoded_lines)
                            for line in decoded_lines:
                                if "Recorded time:" in line:
                                    recorded_time = True
                                if "Destroying" in line:
                                    print(line)
                                    if not recorded_time:
                                        recorded_time = False
                                        print(line)
                                        self.comboBox.setEnabled(True)
                                        self.comboBox_2.setEnabled(True)
                                        self.lineEdit_gain_1.setEnabled(True)
                                        self.lineEdit_gain_2.setEnabled(True)
                                        self.lineEdit_bandwidth.setEnabled(True)
                                        self.lineEdit_bandwidth_2.setEnabled(True)
                                        self.lineEdit_2.setEnabled(True)
                                        self.lineEdit.setEnabled(True)
                                        self.lineEdit_samplingfreq.setEnabled(True)
                                        self.lineEdit_samplingfreq_2.setEnabled(True)
                                        self.lineEdit_3.setEnabled(True)
                                        self.lineEdit_4.setEnabled(True)
                                        self.radioButton_Rx_1.setEnabled(True)
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Record.setEnabled(True)
                                        self.radioButton_Rx_2.setEnabled(True)
                                        recording_started = False
                                        read_response = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        self.comboBox_number_of_files.setEnabled(True)
                                        self.red_light_record.setVisible(True)
                                        self.stop_GPIO_record_replay()
                                        self.green_light_record.setVisible(False)
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"Error occured! Recording not started!")
                                        msg_box_11.exec()     
                                        return
                            ############################################################
                            recording_dual_channel = False
                            recording_rx1_channel = False
                            recording_rx2_channel = True
                            
                            #time.sleep(1)
                            self.elapsed_time = QtCore.QTime(0, 0)
                            self.timer.start(1000)  # Update every 1 second
                            self.timer_started = True
                            self.lineEdit_2.setEnabled(False)  # Disable editing
                            self.update_timer()
                            self.label_current_file.setText("1")
                            self.label_current_file.setStyleSheet("color: #1ABC9C;") 
                    elif reply_2 == QMessageBox.StandardButton.No:
                        print("Selected No")
                        
        else:
            msg_box_error_1 = QMessageBox()
            msg_box_error_1.setWindowTitle("Invalid")
            msg_box_error_1.setText("You are already Recording!")
            msg_box_error_1.exec()
            return
        
##################################################################################################################################################
    def stop_timer(self):
        global ser, recording_started, count_one, read_response, file_count, duration_available_for_recording, SSD_free_space
        if recording_started:
            if not terminated:
                msg_box_stop_record = QMessageBox()
                msg_box_stop_record.setWindowTitle("Confirmation")
                msg_box_stop_record.setText("Do you want to stop the Recording?")
                msg_box_stop_record.setIcon(QMessageBox.Icon.Question)
                msg_box_stop_record.addButton(QMessageBox.StandardButton.Yes)
                msg_box_stop_record.addButton(QMessageBox.StandardButton.No)
                msg_box_stop_record.setDefaultButton(QMessageBox.StandardButton.No) 
                # Execute the message box
                reply = msg_box_stop_record.exec()
                if reply == QMessageBox.StandardButton.Yes:
                    if self.timer_started:
                        self.timer.stop()
                        
                        count_one = 0
                        file_count = 0
                        current_time = self.elapsed_time.toString("HH:mm:ss")
                        
                        duration = subtract_two_times(current_time, duration_available_for_recording)
                        self.label_available_Duration.setText(f"Max Duration: {duration}")
                     
                        #duration = duration_available_for_recording
                        duration_available_for_recording = duration
                        current_time = time_to_seconds(current_time)
                        print("current_time is ", current_time)
                        if record_tab:
                            if self.radioButton_GPIO_Record.isChecked():
                                GPIO_space = current_time
                            else:   GPIO_space = 0
                        elif replay_tab:
                            if self.radioButton_GPIO_Replay.isChecked():
                                GPIO_space = current_time
                            else: GPIO_space = 0
                        else:
                            GPIO_space = 0
                        print(GPIO_space)
                        if recording_dual_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 2,)
                        elif recording_rx1_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 1)
                        elif recording_rx2_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits2, self.samplingfreq_2, current_time,GPIO_space, 1)
                        
                        SSD_free_space = int(int(size1)-log_file_size)
                        size1 = convert_size(size1-log_file_size)
                        self.label_SSD_capacity.setText(f"Free SSD: {size1}")
                        print("size1 is ", size1)
                        self.comboBox.setEnabled(True)
                        self.comboBox_2.setEnabled(True)
                        self.lineEdit_gain_1.setEnabled(True)
                        self.lineEdit_gain_2.setEnabled(True)
                        self.lineEdit_bandwidth.setEnabled(True)
                        self.lineEdit_bandwidth_2.setEnabled(True)
                        self.lineEdit_2.setEnabled(True)
                        self.lineEdit.setEnabled(True)
                        self.lineEdit_samplingfreq.setEnabled(True)
                        self.lineEdit_samplingfreq_2.setEnabled(True)
                        self.lineEdit_3.setEnabled(True)
                        self.lineEdit_4.setEnabled(True)
                        self.radioButton_Rx_1.setEnabled(True)
                        if self.radioButton_gpiomode.isChecked():
                            self.radioButton_GPIO_Record.setEnabled(True)
                        self.radioButton_Rx_2.setEnabled(True)
                        self.green_light_record.setVisible(True)
                        self.red_light_record.setVisible(True)
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(b'\x03')
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                            file.write(f'\n{get_current_datetime()}   \x03')  
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"Comport got disconnected")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        if checked_both_without_HWUSB or HW_USB_in_use:
                            if (HW_USB_in_use):
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active: 
                                    send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                            else:
                                self.stop_reading()
                        self.stop_GPIO_record_replay()
                        #self.lineEdit_6.setStyleSheet("background-color: white;")
                        recording_started = False
                        read_response = False
                        self.worker.stop()  # Tell the thread to stop
                        self.worker.wait()
                        self.worker.running = False
                        self.comboBox_number_of_files.setEnabled(True)
                        self.timer_started = False
                        self.lineEdit_2.setEnabled(True)  # Enable editing
                        #print("Stopping the Rx Capture")
                        start_time = time.time()  # Record start time
                        
                        
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray('clear\n', 'ascii'))
                            if Commands_file_user:
                                with open(file_path, 'a') as file:
                                    file.write(f'\n{get_current_datetime()}   clear\n')
                        else:
                            msg_box_11 = QMessageBox()
                            msg_box_11.setWindowTitle("Error!")
                            msg_box_11.setText(f"Comport got disconnected")
                            msg_box_11.exec()
                            self.open_after_disconnection()
                            return
                        bs = read_lines()
                        ########################################################################
                        #self.label_current_file.setText(f"{file_count+1}")
                        #self.label_current_file.setStyleSheet("color: red;") 
                        ###############################################################################################
                        #send_command(bytearray("kill -SIGINT $(ps -uax | grep ad9361-ii | awk -F' ' '{ print $2 }')\n",'ascii'))
                        #self.ensure_interface_disconnection()
                        
        else:
            msg_box_9 = QMessageBox()
            msg_box_9.setWindowTitle("Error!")
            msg_box_9.setText("Recording is not yet started!")
            msg_box_9.exec()

    def update_timer(self):
        #print("hiii1234")
        global recording_started, match_timer, ser, file_count_variable, file_count, count_one, ser_rtcm, terminated, flag_raised_for_stop_Recording
        global disconnected_comport_while_recording_replaying, read_response, duration_available_for_recording, SSD_free_space
        if terminated:
                read_response = False
                #disconnected_comport_while_recording_replaying = False
                self.timer.stop()
                
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if HW_USB_in_use:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_reading()
                #send_command(b'\x03')  # Send Ctrl+C to stop the recording
                #print("terminated is true")
                current_time = self.elapsed_time.toString("HH:mm:ss")
                duration = subtract_two_times(current_time, duration_available_for_recording)
                self.label_available_Duration.setText(f"Max Duration: {duration}")
                #duration = duration_available_for_recording
                duration_available_for_recording = duration
                current_time = time_to_seconds(current_time)
                if record_tab:
                    if self.radioButton_GPIO_Record.isChecked():
                            GPIO_space = current_time
                    else:   GPIO_space = 0
                elif replay_tab:
                    if self.radioButton_GPIO_Replay.isChecked():
                            GPIO_space = current_time
                    else: GPIO_space = 0
                else:
                        GPIO_space = 0
                if recording_dual_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time, GPIO_space, 2)
                elif recording_rx1_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time, GPIO_space, 1)
                elif recording_rx2_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits2, self.samplingfreq_2, current_time, GPIO_space, 1)
                
                SSD_free_space = int(int(size1)-log_file_size)
                size1 = convert_size(size1-log_file_size)
                self.label_SSD_capacity.setText(f"Free SSD: {size1}")
                self.lineEdit_6.clear()
                self.comboBox.setEnabled(True)
                self.comboBox_2.setEnabled(True)
                self.lineEdit_gain_1.setEnabled(True)
                self.lineEdit_gain_2.setEnabled(True)
                self.lineEdit_bandwidth.setEnabled(True)
                self.lineEdit_bandwidth_2.setEnabled(True)
                self.lineEdit_2.setEnabled(True)
                self.lineEdit.setEnabled(True)
                self.lineEdit_samplingfreq.setEnabled(True)
                self.lineEdit_samplingfreq_2.setEnabled(True)
                self.lineEdit_3.setEnabled(True)
                self.lineEdit_4.setEnabled(True)
                self.radioButton_Rx_1.setEnabled(True)
                if self.radioButton_gpiomode.isChecked():
                    self.radioButton_GPIO_Record.setEnabled(True)
                self.radioButton_Rx_2.setEnabled(True)
                recording_started = False
                self.worker.stop()  # Tell the thread to stop
                self.worker.wait()
                self.worker.running = False
                self.comboBox_number_of_files.setEnabled(True)
                self.red_light_record.setVisible(True)
                self.stop_GPIO_record_replay()
                self.green_light_record.setVisible(False)
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if HW_USB_in_use:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_reading()
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Terminated!")
                msg_box_9.setText("Recording Terminated!")
                msg_box_9.exec()
                #self.open_after_disconnection()
                return

        if not terminated:
            if disconnected_comport_while_recording_replaying:
                read_response = False
                #print("disconnected_comport_while_recording_replaying is true")
                #disconnected_comport_while_recording_replaying = False
                self.timer.stop()
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if HW_USB_in_use:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_reading()
                current_time = self.elapsed_time.toString("HH:mm:ss")
                duration = subtract_two_times(current_time, duration_available_for_recording)
                self.label_available_Duration.setText(f"Max Duration: {duration}")
                duration_available_for_recording = duration
                current_time = time_to_seconds(current_time)
                if record_tab:
                    if self.radioButton_GPIO_Record.isChecked():
                            GPIO_space = current_time
                    else: GPIO_space = 0
                elif replay_tab:
                        if self.radioButton_GPIO_Replay.isChecked():
                            GPIO_space = current_time
                        else: GPIO_space = 0
                else:
                        GPIO_space = 0
                if recording_dual_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 2)
                elif recording_rx1_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 1)
                elif recording_rx2_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits2, self.samplingfreq_2, current_time,GPIO_space, 1)
                
                SSD_free_space = int(int(size1)-log_file_size)
                size1 = convert_size(size1-log_file_size)
                self.label_SSD_capacity.setText(f"Free SSD: {size1}")
                self.comboBox.setEnabled(True)
                self.comboBox_2.setEnabled(True)
                self.lineEdit_gain_1.setEnabled(True)
                self.lineEdit_gain_2.setEnabled(True)
                self.lineEdit_bandwidth.setEnabled(True)
                self.lineEdit_bandwidth_2.setEnabled(True)
                self.lineEdit_2.setEnabled(True)
                self.lineEdit.setEnabled(True)
                self.lineEdit_samplingfreq.setEnabled(True)
                self.lineEdit_samplingfreq_2.setEnabled(True)
                self.lineEdit_3.setEnabled(True)
                self.lineEdit_4.setEnabled(True)
                self.radioButton_Rx_1.setEnabled(True)
                if self.radioButton_gpiomode.isChecked():
                    self.radioButton_GPIO_Record.setEnabled(True)
                self.radioButton_Rx_2.setEnabled(True)
                recording_started = False
                self.worker.stop()  # Tell the thread to stop
                self.worker.wait()
                self.worker.running = False
                self.comboBox_number_of_files.setEnabled(True)
                self.red_light_record.setVisible(True)
                self.stop_GPIO_record_replay()
                self.green_light_record.setVisible(False)
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if HW_USB_in_use:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_reading()
                msg_box_9 = QMessageBox()
                msg_box_9.setWindowTitle("Error!")
                msg_box_9.setText("Comport disconnected!, recording stopped!")
                msg_box_9.exec()
                self.open_after_disconnection()
                return
            
            count_one += 1
            current_time = self.elapsed_time.toString("HH:mm:ss")
            if current_time == str(duration_valid):
                read_response = False
                self.timer.stop()
                if checked_both_without_HWUSB or HW_USB_in_use:
                    if HW_USB_in_use:
                        comport_is_active = interface_is_online(self.comport)
                        if comport_is_active: 
                            send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                            with open(file_path, 'a') as file:
                                file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                    else:
                        self.stop_reading()
                #print("time is equal")
                file_count += 1
                count_one = 0
                #send_command(b'\x03')  # Send Ctrl+C to stop the recording
                bs = read_lines()
                ########################################################################
                #print("yes")
                bs = read_lines()
                ########################################################################
                #print("yes2.5")   
                #print(current_time)
                current_time = self.elapsed_time.toString("HH:mm:ss")
                #print(duration_available_for_recording)
                duration = subtract_two_times(str(duration_valid), str(duration_available_for_recording))
                self.label_available_Duration.setText(f"Max Duration: {duration}")
                     
                duration_available_for_recording = duration
                current_time = time_to_seconds(str(duration_valid))
                if record_tab:
                    if self.radioButton_GPIO_Record.isChecked():
                            GPIO_space = current_time
                    else:   GPIO_space = 0
                elif replay_tab:
                    if self.radioButton_GPIO_Replay.isChecked():
                            GPIO_space = current_time
                    else: GPIO_space = 0
                else:
                        GPIO_space = 0
                if recording_dual_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 2)
                elif recording_rx1_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time,GPIO_space, 1)
                elif recording_rx2_channel:
                            size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits2, self.samplingfreq_2, current_time,GPIO_space, 1)
                #print("size1 is ", size1)
                
                SSD_free_space = int(int(size1)-log_file_size)
                size1 = convert_size(size1-log_file_size)
                self.label_SSD_capacity.setText(f"Free SSD: {size1}")
                #########################################################################
                #print(f"file count variable: {file_count_variable}")
                #print(f"{file_count} is file count")
                if file_count == file_count_variable:
                        #print("time is equal")
                        #print("file count is equal to file count variable")
                        if checked_both_without_HWUSB or HW_USB_in_use:
                            if HW_USB_in_use:
                                comport_is_active = interface_is_online(self.comport)
                                if comport_is_active: 
                                    send_command(bytearray(f'{disconnect_HW_USB_record_replay}\n', 'ascii'))
                                    with open(file_path, 'a') as file:
                                        file.write(f'\n{get_current_datetime()}   {disconnect_HW_USB_record_replay}\n')
                            else:
                                self.stop_reading()
                        self.label_current_file.setText(f"{file_count}") 
                        #self.label_current_file.setStyleSheet("color: red;") 
                        
                        self.comboBox.setEnabled(True)
                        self.comboBox_2.setEnabled(True)
                        self.lineEdit_gain_1.setEnabled(True)
                        self.lineEdit_gain_2.setEnabled(True)
                        self.lineEdit_bandwidth.setEnabled(True)
                        self.lineEdit_bandwidth_2.setEnabled(True)
                        self.lineEdit_2.setEnabled(True)
                        self.lineEdit.setEnabled(True)
                        self.lineEdit_samplingfreq.setEnabled(True)
                        self.lineEdit_samplingfreq_2.setEnabled(True)
                        self.lineEdit_3.setEnabled(True)
                        self.lineEdit_4.setEnabled(True)
                        self.radioButton_Rx_1.setEnabled(True)
                        if self.radioButton_gpiomode.isChecked():
                            self.radioButton_GPIO_Record.setEnabled(True)
                        self.radioButton_Rx_2.setEnabled(True)
                        self.green_light_record.setVisible(True)
                        self.red_light_record.setVisible(True)
                        self.stop_GPIO_record_replay()
                        self.green_light_record.setVisible(False)
                        self.red_light_record.setVisible(True)
                        recording_started = False
                        #read_response = False
                        self.worker.stop()  # Tell the thread to stop
                        self.worker.wait()
                        self.worker.running = False
                        #send_command(b'\x03')  # Send Ctrl+C to stop the recording
                        self.comboBox_number_of_files.setEnabled(True)
                        """if  file_count > 1:
                            current_time = self.elapsed_time.toString("HH:mm:ss")
                            duration = subtract_two_times(current_time, duration_available_for_recording)
                            self.label_available_Duration.setText(f"Max Duration: {duration}")
                            duration_available_for_recording = duration
                            current_time = time_to_seconds(current_time)
                            if recording_dual_channel:
                                size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time, 2)
                            elif recording_rx1_channel:
                                size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits1, self.samplingfreq_1, current_time, 1)
                            elif recording_rx2_channel:
                                size1 = self.size_after_minus_x(SSD_free_space, self.selected_adc_bits2, self.samplingfreq_2, current_time, 1)
                            if not file_count_variable == 1:
                                SSD_free_space = int(int(size1)-log_file_size)
                            size1 = convert_size(size1-log_file_size)
                            
                            self.label_SSD_capacity.setText(f"Free SSD: {size1}")"""
                        file_count = 0
                        return
                else:
                        time.sleep(1)
                        self.lineEdit_6.setText("")
                        self.multiple_files_recording()
                #############################################################################
            if recording_started:
                self.elapsed_time = self.elapsed_time.addSecs(1)
                self.lineEdit_6.setText(self.elapsed_time.toString("HH:mm:ss"))
            if count_one == 1:
                if checked_both_without_HWUSB:
                    #print("hii")
                    self.start_reading() 
            #self.lineEdit_6.setStyleSheet("color: black; font-weight: bold;")
            #self.lineEdit_6.setStyleSheet("background-color: white;")
            #print("1")
        #####################################################################################

        #####################################################################################
    def multiple_files_recording(self):
        global ser, rtcm_create_file, recording_started, read_response, terminated, flag_raised_for_stop_Recording
        def check_recording():
            global read_response, recording_started, terminated, flag_raised_for_stop_Recording
            while True:
                if read_response:
                    line = self.read_decoded_line()
                    if "Terminated before the full duration!" in line:
                        terminated = True
                        break
                else:
                    #flag_raised_for_stop_Recording = True
                    break
        send_command(bytearray('clear\n', 'ascii'))
        clear_lines = read_lines()
        print("clear lines are ", clear_lines)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        duration = time_to_seconds(self.duration_value)
        gain = self.lineEdit_gain_1.text()
        if gain == "Slow attack":
             gain = 100
        elif gain == "Fast attack":
             gain = 200
        elif gain == "Hybrid":
             gain = 300 
        gain_2 = self.lineEdit_gain_2.text()
        if gain_2 == "Slow attack":
             gain_2 = 100
        elif gain_2 == "Fast attack":
             gain_2 = 200
        elif gain_2 == "Hybrid":
             gain_2 = 300 
        read_response = True
        #####################################################################
        if recording_dual_channel:
            mode = 2
            final_string = (
                f"{executable_rx} "                                # executable_rx
                f"{mode} "           # Var1
                f"{self.selected_center_frequency1}e6 "           # Var1
                f"{self.selected_center_frequency2}e6 "           # Var2
                f"{self.selected_adc_bits1} "                    # Var3
                f"{self.selected_adc_bits2} "                    # Var3
                f'"{Lg_path}"'                                    # Var3
                f'"{self.file_name}_{current_time}.bin" '
                f"{duration} " 
                f"{self.bandwidth}e6 "                               
                f"{self.bandwidth_2}e6 " 
                f"{self.samplingfreq_1}e6 "                              
                f"{self.samplingfreq_2}e6 "                                                              
                f"{gain} "                               
                f"{gain_2} "                                                                 # Var3
                f"{self.reference_frequency} "
                f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log" \n'
                )
        elif recording_rx1_channel:
            mode = 0
            final_string = (
                f"{executable_rx} "                                # executable_rx
                f"{mode} "           # Var1
                f"{self.selected_center_frequency1}e6 "           # Var1
                f"{self.selected_center_frequency1}e6 "           # Var2
                f"{self.selected_adc_bits1} "                    # Var3
                f"{self.selected_adc_bits1} "                    # Var3
                f'"{Lg_path}"'                                    # Var3
                f'"{self.file_name}_{current_time}.bin" '
                f"{duration} " 
                f"{self.bandwidth}e6 "                               
                f"{self.bandwidth}e6 " 
                f"{self.samplingfreq_1}e6 "                              
                f"{self.samplingfreq_1}e6 "                                                              
                f"{gain} "                               
                f"{gain} "                                                                 # Var3
                f"{self.reference_frequency} "
                f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log" \n'
                )
        elif recording_rx2_channel:
            mode = 4
            final_string = (
                f"{executable_rx} "                                # executable_rx
                f"{mode} "           # Var1
                f"{self.selected_center_frequency2}e6 "           # Var1
                f"{self.selected_center_frequency2}e6 "           # Var2
                f"{self.selected_adc_bits2} "                    # Var3
                f"{self.selected_adc_bits2} "                    # Var3
                f'"{Lg_path}"'                                    # Var3
                f'"{self.file_name}_{current_time}.bin" '
                f"{duration} " 
                f"{self.bandwidth_2}e6 "                               
                f"{self.bandwidth_2}e6 " 
                f"{self.samplingfreq_2}e6 "                              
                f"{self.samplingfreq_2}e6 "                                                              
                f"{gain_2} "                               
                f"{gain_2} "                                                                 # Var3
                f"{self.reference_frequency} "
                f'| tee -i "{Lg_path}{self.file_name}_{current_time}.log" \n'
                ) 
        #######################################################################
            #print("the command is ",final_string)
        if checked_both_without_HWUSB:
            comport_2_rtcm = interface_is_onlineRTCM(self.comport_rtcm)
            if not comport_2_rtcm:
                msg_box_2 = QMessageBox()
                msg_box_2.setWindowTitle("Missing Data")
                msg_box_2.setText(f"{self.comport_rtcm} got disconnected!")
                msg_box_2.exec()
                self.open_after_disconnection()
                return            
            try:
                rtcm_create_file = f'{rtcm_folder_path}/{self.file_name}_{current_time}.rtcm'
                with open(rtcm_create_file, 'w'):
                    pass
            except PermissionError as e:
                                        self.comboBox.setEnabled(True)
                                        self.comboBox_2.setEnabled(True)
                                        self.lineEdit_gain_1.setEnabled(True)
                                        self.lineEdit_gain_2.setEnabled(True)
                                        self.lineEdit_bandwidth.setEnabled(True)
                                        self.lineEdit_bandwidth_2.setEnabled(True)
                                        self.lineEdit_2.setEnabled(True)
                                        self.lineEdit.setEnabled(True)
                                        self.lineEdit_samplingfreq.setEnabled(True)
                                        self.lineEdit_samplingfreq_2.setEnabled(True)
                                        self.lineEdit_3.setEnabled(True)
                                        self.lineEdit_4.setEnabled(True)
                                        self.radioButton_Rx_1.setEnabled(True)
                                        if self.radioButton_gpiomode.isChecked():
                                            self.radioButton_GPIO_Record.setEnabled(True)
                                        self.radioButton_Rx_2.setEnabled(True)
                                        recording_started = False
                                        read_response = False
                                        self.worker.stop()  # Tell the thread to stop
                                        self.worker.wait()
                                        self.worker.running = False
                                        self.comboBox_number_of_files.setEnabled(True)
                                        self.red_light_record.setVisible(True)
                                        self.stop_GPIO_record_replay()
                                        self.green_light_record.setVisible(False)
                                        msg_box_11 = QMessageBox()
                                        msg_box_11.setWindowTitle("Error!")
                                        msg_box_11.setText(f"Permission denied! Recording not started!\nYou cannot select this folder for RTCM recording!")
                                        msg_box_11.exec()     
                                        return
                                
        comport_is_active = interface_is_online(self.comport)
        if HW_USB_in_use:
            record_folder_path = f"{rtcm_folder_path}{self.file_name}_{current_time}"
            self.rtcm_record_command(record_folder_path)
        if comport_is_active: 
            self.GPIO_record_replay(Lg_path, f"{self.file_name}_{current_time}.gpio", duration, 0)
            send_command(bytearray(final_string,'ascii'))   
            recording_thread = threading.Thread(target=check_recording)
            recording_thread.start()
            if Commands_file_user:
                    with open(file_path, 'a') as file:
                        file.write(f"\n{get_current_datetime()}   {final_string}")
            lines = read_lines()
            decoded_lines = [line.decode() for line in lines]
        else:
            self.timer.stop()
            self.comboBox.setEnabled(True)
            self.comboBox_2.setEnabled(True)
            self.lineEdit_gain_1.setEnabled(True)
            self.lineEdit_gain_2.setEnabled(True)
            self.lineEdit_bandwidth.setEnabled(True)
            self.lineEdit_bandwidth_2.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit_samplingfreq.setEnabled(True)
            self.lineEdit_samplingfreq_2.setEnabled(True)
            self.lineEdit_3.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
            self.radioButton_Rx_1.setEnabled(True)
            if self.radioButton_gpiomode.isChecked():
                self.radioButton_GPIO_Record.setEnabled(True)
            self.radioButton_Rx_2.setEnabled(True)
            recording_started = False
            read_response = False
            self.worker.stop()  # Tell the thread to stop
            self.worker.wait()
            self.worker.running = False
            self.comboBox_number_of_files.setEnabled(True)
            self.red_light_record.setVisible(True)
            self.green_light_record.setVisible(False)
            msg_box_11 = QMessageBox()
            msg_box_11.setWindowTitle("Error!")
            msg_box_11.setText(f"COM port got disconnected!, Could not continue the Recording!")
            msg_box_11.exec()
            self.open_after_disconnection()
            return  
                            #print(decoded_lines)
        recorded_time = False
        for line in decoded_lines:
            #print(f"\n\nlines:{line}\n\n")
            if "Recorded time:" in line:
                recorded_time = True
            if "Destroying" in line:
                print(line)
                if not recorded_time:
                    recorded_time = False
                    self.comboBox.setEnabled(True)
                    self.comboBox_2.setEnabled(True)
                    self.lineEdit_gain_1.setEnabled(True)
                    self.lineEdit_gain_2.setEnabled(True)
                    self.lineEdit_bandwidth.setEnabled(True)
                    self.lineEdit_bandwidth_2.setEnabled(True)
                    self.lineEdit_2.setEnabled(True)
                    self.lineEdit.setEnabled(True)
                    self.lineEdit_samplingfreq.setEnabled(True)
                    self.lineEdit_samplingfreq_2.setEnabled(True)
                    self.lineEdit_3.setEnabled(True)
                    self.lineEdit_4.setEnabled(True)
                    self.radioButton_Rx_1.setEnabled(True)
                    if self.radioButton_gpiomode.isChecked():
                        self.radioButton_GPIO_Record.setEnabled(True)
                    self.radioButton_Rx_2.setEnabled(True)
                    recording_started = False
                    read_response = False
                    self.worker.stop()  # Tell the thread to stop
                    self.worker.wait()
                    self.worker.running = False
                    self.comboBox_number_of_files.setEnabled(True)
                    self.red_light_record.setVisible(True)
                    self.stop_GPIO_record_replay()
                    self.green_light_record.setVisible(False)
                    msg_box_11 = QMessageBox()
                    msg_box_11.setWindowTitle("Error!")
                    msg_box_11.setText(f"Error occured! Recording not started!")
                    msg_box_11.exec()     
                    return
     #   time.sleep(1)
        # Start the timer only if memory is sufficient
        self.elapsed_time = QtCore.QTime(0, 0)
        self.timer.start(1000)  # Update every 1 second
        self.timer_started = True
        self.lineEdit_2.setEnabled(False)  # Disable editing
        self.label_current_file.setText(f"{file_count+1}")
        self.update_timer()
        ##############################################################################
    ##################################################################################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GNSS Record and Replay"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "  Enter the file name"))
        self.label.setText(_translate("MainWindow", "File Name"))
        self.label_2.setText(_translate("MainWindow", "Duration"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "  HH:MM:SS"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_3.setText(_translate("MainWindow", "Stop"))
        self.pushButton_login.setText(_translate("MainWindow", "Connect"))
        self.pushButton_2.setText(_translate("MainWindow", "Record"))
        self.pushButton_4.setText(_translate("MainWindow", "Replay"))
        self.pushButton_5.setText(_translate("MainWindow", "About"))
        self.label_3.setText(_translate("MainWindow", "Rx 1"))
        self.label_4.setText(_translate("MainWindow", "Rx 2"))
        self.label_8.setText(_translate("MainWindow", "#ADC Bits"))
        self.label_10.setText(_translate("MainWindow", "LO frequency"))
        self.label_9.setText(_translate("MainWindow", "Center"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Select"))
        self.comboBox.setItemText(1, _translate("MainWindow", "4"))
        self.comboBox.setItemText(2, _translate("MainWindow", "8"))
        self.comboBox.setItemText(3, _translate("MainWindow", "16"))
        """self.comboBox.setItemText(4, _translate("MainWindow", "4"))
        self.comboBox.setItemText(5, _translate("MainWindow", "5"))
        self.comboBox.setItemText(6, _translate("MainWindow", "6"))
        self.comboBox.setItemText(7, _translate("MainWindow", "7"))
        self.comboBox.setItemText(8, _translate("MainWindow", "8"))
        self.comboBox.setItemText(9, _translate("MainWindow", "9"))
        self.comboBox.setItemText(10, _translate("MainWindow", "10"))
        self.comboBox.setItemText(11, _translate("MainWindow", "11"))
        self.comboBox.setItemText(12, _translate("MainWindow", "12"))"""
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Select"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "4"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "8"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "16"))
        """self.comboBox_2.setItemText(4, _translate("MainWindow", "4"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "5"))
        self.comboBox_2.setItemText(6, _translate("MainWindow", "6"))
        self.comboBox_2.setItemText(7, _translate("MainWindow", "7"))
        self.comboBox_2.setItemText(8, _translate("MainWindow", "8"))
        self.comboBox_2.setItemText(9, _translate("MainWindow", "9"))
        self.comboBox_2.setItemText(10, _translate("MainWindow", "10"))
        self.comboBox_2.setItemText(11, _translate("MainWindow", "11"))
        self.comboBox_2.setItemText(12, _translate("MainWindow", "12"))"""
        self.label_5.setText(_translate("MainWindow", "Progress"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "  HH:MM:SS"))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_started = False
        self.elapsed_time = QtCore.QTime(0, 0)

        # Connect the start button to start the timer
        self.pushButton.clicked.connect(self.start_timer)
        # Connect the stop button to stop the timer
        self.pushButton_3.clicked.connect(self.stop_timer)

    def open_second_window(self):
        global delete_gui, root_removing
        delete_gui = True
        self.pushButton_browse_config.setEnabled(False)

        import tkinter as tk
        from tkinter import ttk

        # Create the main application window
        root_removing = tk.Tk()
        root_removing.title("Please wait!")
        root_removing.geometry("200x100")
        root_removing.attributes("-toolwindow", 1)
        root_removing.attributes("-fullscreen", 0)


        # Add a label to display "Removing"
        label = ttk.Label(root_removing, text="Removing", font=("Arial", 16, "bold"))
        label.pack(expand=True)

        # Function to close the GUI after 5 seconds
        def close_gui():
            global delete_gui
            delete_gui = False
            root_removing.destroy()
            self.pushButton_browse_config.setEnabled(True)

        # Schedule the GUI to close after 5000 milliseconds (5 seconds)
        root_removing.after(5000, close_gui)
        def disable_close():
            pass  # Do nothing when the close button is clicked
        # Override the close behavior
        root_removing.protocol("WM_DELETE_WINDOW", disable_close)

        try:
            # Main loop for the application
            root_removing.mainloop()
        except tk.TclError:
            print("The application has been closed or destroyed.")


        """if self.second_window is None:
            self.second_window = QtWidgets.QMainWindow()
            self.ui = Ui_SecondWindow()
            self.ui.setupUi(self.second_window)
            self.second_window.show()

            # Set up a QTimer to close the second window after 5 seconds
            QtCore.QTimer.singleShot(1000, self.close_second_window)"""

    def close_second_window(self):
        global delete_gui, root_removing
        delete_gui = False
        if self.second_window is not None:
            root_removing.destroy()
            self.second_window.close()
            self.second_window = None

#print("Last selected item:", last_selected_item_data)
"""class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setMaximumSize(600, 400)"""

class MainWindowWithCloseEvent(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowWithCloseEvent, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # Override the closeEvent method to print "terminate" when the window is closed
    def closeEvent(self, event):
        global ser, root, check_comport
        check_comport = False
        if not ser == None:
                comport_is_active = interface_is_online(active_comport_used)
                if comport_is_active and comport_connected: 
                    send_command(bytearray(f'nice --20 /home/root/adc4bits/libiio/build/examples/switches\n', 'ascii'))
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'nice --20 /home/root/adc4bits/libiio/build/examples/switches\n')
                comport_is_active = interface_is_online(active_comport_used)
                if comport_is_active and comport_connected: 
                    send_command(b'\x03')
                    if Commands_file_user:
                        with open(file_path, 'a') as file:
                            file.write(f'\n{get_current_datetime()}   \x03')
                else:
                    return
                print("terminate")
                if gui_opened:
                    root_gui.destroy()
                event.accept()  # Ensure the window closes

if __name__ == "__main__":
    import sys

    def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        """Avoid crashing the GUI on KeyboardInterrupt from callback execution."""
        if issubclass(exc_type, KeyboardInterrupt):
            print("KeyboardInterrupt received inside GUI event callback; ignoring it.")
            return
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_uncaught_exception

    app = QtWidgets.QApplication(sys.argv)
    # Use the subclass that handles the close event
    MainWindow = MainWindowWithCloseEvent()
    MainWindow.show()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("KeyboardInterrupt received while the Qt event loop was running; closing cleanly.")

