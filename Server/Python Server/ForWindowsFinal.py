import socket
import re, uuid
import winapps
import json
import sys
import psutil
import windows_tools.product_key
import windows_tools.registry
import winreg

import os
import subprocess
import ctypes
import time

import requests

soft_count=0
auth_count=0
unauth_count=0

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# #connecting to key in registry
# access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
# access_key = winreg.OpenKey(access_registry,r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\")
# #accessing the key to open the registry directories under

import winreg

# Specify the registry path and key name
key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
key_name = "ProductId"

# Open the registry key
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
    # Retrieve the value of the key
    value, regtype = winreg.QueryValueEx(key, key_name)
    
    # Print the value
    print(f"Windows Product Key is: {value}")
    if len(value) == 0:
        print("Windows is not Activated")
    else:
        print("Windows is Licensed")


print("")
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

# --------------------------------------------------------------------

print ("The MAC address of this PC is ", end="")
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
# print (':'.join(re.findall('..', '%012x' % uuid.getnode())))
print(mac)
print("")

# --------------------------------------------------------------------
 
# get each application with list_installed()
sf=list()
# sfd=list()

# --- dig sig ---

# Function to search for a file in a directory and its subdirectories
def search_exe_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe"):
                if(file != "uninstall.exe"):
                    return os.path.join(root, file)
    return None

# checking if digsig present
def extract_digital_signature(exe_file_path):
    try:
        # Run sigcheck command with the /a option to display file information,
        # including digital signatures, in CSV format
        result = subprocess.run(['sigcheck', '-a', '-nobanner', exe_file_path], capture_output=True, text=True)
        # print(result)
        if result.returncode == 0:
            # Extract the digital signature information from the command output
            output_lines = result.stdout.splitlines()
            # print(output_lines)
            for line in output_lines:
                if line:
                    return line.strip().split(":")[1].strip()
        else:
            # print("Failed to extract digital signature:", result.stderr)
            stat="Failed to extract digital signature"
    except Exception as e:
        # print("Error:", e)
        # print(None)
        error = e
        # stat="Error : " + e
    return None


software_list = []
sftstring = str("")

for item in winapps.list_installed():

    soft_count = soft_count+1
    signature=""
    strstr=""
    var = ".exe"
    if(item.install_location):
        # # Example usage:
        # path = "C:/Program Files/Android/Android Studio"  # Replace with the path you want to search in
        found_file = search_exe_file(item.install_location)
        signature = extract_digital_signature(found_file)
        if(not signature):
            # for p in item.uninstall_string:
            if(item.uninstall_string):
                strstr = item.uninstall_string.split(".exe")[0]+var
                # print(item.uninstall_string.split(".exe")[0]+var)
                # strstr.replace( '"', '')
                if(item.uninstall_string[0] == '"'):   
                    strstr = strstr.split('"')[1]
                # print(strstr)
                signature = extract_digital_signature(strstr)
    else:
        if(item.uninstall_string):
                strstr = item.uninstall_string.split(".exe")[0]+var
                # print(item.uninstall_string.split(".exe")[0]+var)
                # strstr.replace( '"', '')
                if(item.uninstall_string[0] == '"'):   
                    strstr = strstr.split('"')[1]
                # print(strstr)
                signature = extract_digital_signature(strstr)
         

# --------------------- extracting digital signatures ---------------------
    
    isAuthenticate=False
    if signature:
        # print("Digital signature:", signature)
        stat="Digital Signature Found"
        isAuthenticate=True
        auth_count = auth_count+1
    else:
        # print("Digital Signature: Not found.")
        stat="Digital Signature Not Found"
        
    # else:
    #     print("File not found.")

    if(strstr == "MsiExec.exe"):
        isAuthenticate=True
        auth_count = auth_count+1
        stat="Digital Signature Found"

# --------------------- extracting digital signatures ---------------------
    if(isAuthenticate):
        authstring = str(item.name+" (Authentic), ")
    else:
        authstring = str(item.name+" (Not Authentic), ")

    software = {}
    software['Name'] = str(item.name)
    software['Version'] = str(item.version)
    software['Install Date'] = str(item.install_date)
    software['Install Location'] = str(item.install_location)
    software['Install Source'] = str(item.install_source)
    software['Modify Path'] = str(item.modify_path)
    software['Publisher'] = str(item.publisher)
    software['Uninstall String'] = str(item.uninstall_string)
    software['DigSig Status'] = str(stat)
    software['Is Authenticate'] = str(isAuthenticate)
    software_list.append(software)

    sftstring = sftstring + authstring

unauth_count = soft_count - auth_count

X = {
    "username": 11910447,
    "computer_name": str(hostname),
    "product_key": str(value),
    "hostname": str(hostname),
    "ip_address": str(ip_address),
    "mac_address": str(mac),
    "softwares_installed": str(sftstring),
    "software_count": soft_count,
    "authentic_software_count": auth_count,
    "unauthentic_software_count": unauth_count
}
sfdata= json.dumps(X)
print(sfdata)

url = "https://nexus-api-vit.herokuapp.com/os_windows/"

json_data = json.dumps(X)

# set the headers for the request
headers = {
    'Content-Type': 'application/json'
}

# send the request to the API endpoint
response = requests.post(url, data=json_data, headers=headers)

# check the response status code
if response.status_code == 201:
    # data was successfully pushed to the API
    print('Data was successfully pushed to the API!')
else:
    # there was an error pushing data to the API
    print(f'Error pushing data to the API: {response.status_code}')

#--------------------------------------------------------

    