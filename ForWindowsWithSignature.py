import socket
import re
import uuid
import winapps
import json
import sys
import psutil
import windows_tools.product_key
import windows_tools.registry
import winreg
from pathlib import Path

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# get Windows Product Key
key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
key_name = "ProductId"
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
    value, regtype = winreg.QueryValueEx(key, key_name)
    print(f"Windows Product Key is: {value}")
    if len(value) == 0:
        print("Windows is not Activated")
    else:
        print("Windows is Licensed")

print("")
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

# get MAC address
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
print(f"The MAC address of this PC is {mac}\n")

# get list of installed software and check if each one is digitally signed
software_list = []
for item in winapps.list_installed():
    software = {}
    software['Name'] = str(item.name)
    software['Version'] = str(item.version)
    software['Install Date'] = str(item.install_date)
    software['Install Location'] = str(item.install_location)
    software['Install Source'] = str(item.install_source)
    software['Modify Path'] = str(item.modify_path)
    software['Publisher'] = str(item.publisher)
    software['Uninstall String'] = str(item.uninstall_string)
    try:
        exe_path = Path(item.install_location) / item.modify_path
        is_signed = windows_tools.product_key.is_signed(exe_path)
        software['Digitally Signed'] = str(is_signed)
    except Exception as e:
        print(f"Error checking digital signature for {item.name}: {e}")
        software['Digitally Signed'] = 'Unknown'
    software_list.append(software)

# create dictionary of system info
system_info = {
    "Hostname": hostname,
    "IP Address": ip_address,
    "MAC Address": mac,
    "Windows Product Key": value,
    "Software Installed": software_list
}

print(system_info)

# convert dictionary to JSON string
system_info_str = json.dumps(system_info)

# send data to server over socket
host = "localhost"
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(system_info_str.encode())
    data = s.recv(10000)

print(f"Received from server: {data.decode()}")