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

# checking and verfiying if digsig present
# def extract_digital_signature(exe_file_path):
#     try:
#         # Run sigcheck command with the /a option to display file information,
#         # including digital signatures, in CSV format
#         result = subprocess.run(['sigcheck', '-a', '-nobanner', exe_file_path], capture_output=True, text=True)
#         if result.returncode == 0:
#             # Extract the digital signature information from the command output
#             output_lines = result.stdout.splitlines()
#             for line in output_lines:
#                 # if line.startswith('Signer'):
#                 if line:
#                     print('in signer part')
#                     # Extract the signer information
#                     signer = line.split(':')[1].strip()
#                     # Run signtool command with the /verify option to verify the digital signature
#                     print('in verify part')
#                     verify_result = subprocess.run(['C:/Program Files (x86)/Windows Kits/10/bin/10.0.22000.0/x64/signtool.exe', 'verify', '/pa', exe_file_path], capture_output=True, text=True)
#                     print('after verify result')
#                     if verify_result.returncode == 0:
#                         # Check if the digital signature is valid
#                         if 'Succeeded' in verify_result.stdout:
#                             print(signer + ' - Valid digital certificate')
#                             return signer + ' - Valid digital certificate'
#                         else:
#                             print(signer + ' - Invalid digital certificate')
#                             return signer + ' - Invalid digital certificate'
#                     else:
#                         print('Failed to verify digital certificate: ' + verify_result.stderr)
#                         return 'Failed to verify digital certificate: ' + verify_result.stderr
#             print('Digital signature not found in the file')
#             return None
#         else:
#             print('Failed to extract digital signature: ' + result.stderr)
#             return None
#     except Exception as e:
#         print('Error: ' + str(e))
#     return None

# --- dig sig ---

software_list = []
for item in winapps.list_installed():
    # Sfd = [item.name, item.version, item.install_date, item.install_location, item.install_source, item.install_source, item.modify_path, item.publisher, item.uninstall_string]
    # sfd=list()
    # sfd.append(str(item.name))
    # sfd.append(str(item.version))
    # sfd.append(str(item.install_date))
    # sfd.append(str(item.install_location))
    # sfd.append(str(item.install_source))
    # sfd.append(str(item.modify_path))
    # sfd.append(str(item.publisher))
    # sfd.append(str(item.uninstall_string))
    # sf.append(sfd)

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

    

    # if found_file:
    #     print("File found at: ", found_file)
    # exe_file_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"  # Replace with the path to your .exe file
    
    isAuthenticate=False
    if signature:
        # print("Digital signature:", signature)
        stat="Digital Signature Found"
        isAuthenticate=True
    else:
        # print("Digital Signature: Not found.")
        stat="Digital Signature Not Found"
        
    # else:
    #     print("File not found.")

    if(strstr == "MsiExec.exe"):
        isAuthenticate=True
        stat="Digital Signature Found"

# --------------------- extracting digital signatures ---------------------
    
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

    print("Software Name : "+item.name)
    print("Version : ", end="")
    print(item.version)
    print("Install Date : ", end="")
    print(item.install_date)

    print("Install Location : ", end="")
    print(item.install_location)

    print("Install Source : ", end="")
    print(item.install_source)
    print("Modify Path : ", end="")
    print(item.modify_path)
    print("Publisher Name : ", end="")
    print(item.publisher)
    print("Uninstall Path : ", end="")
    print(item.uninstall_string)
    print("DigSig Status : ", end="")
    print(stat)
    print("Is Authenticate : ", end="")
    print(isAuthenticate)
    
    print("\n")
    # sfd.clear




X = {
    "Hostname": hostname,
    "IP Address": ip_address,
    "MAC Address": mac,
    "Windows Product Key": value,
    "Softwares Installed": software_list
}
sfdata= json.dumps(X)
print(X)

# set the headers for the request
headers = {
    'Content-Type': 'application/json'
}


#--------------------------------------------------------

host = "https://nexus-api-vit.herokuapp.com/"
url = 'https://nexus-api-vit.herokuapp.com/'
port = 12345

# Create a socket (SOCK_STREAM means a TCP socket)
# sock = socket.socket()
# sock.connect((host,port))
# sfdata = bytes(sfdata,'utf-8')
# sock.sendall(sfdata)

# send the request to the API endpoint
response = requests.post(url, data=sfdata, headers=headers)
# check the response status code
if response.status_code == 200:
    # data was successfully pushed to the API
    print('Data was successfully pushed to the API!')
else:
    # there was an error pushing data to the API
    print(f'Error pushing data to the API: {response.status_code}')


# data = sock.recv(100000)
# print("-------------------------------------")
# print(data)

# print("----------------------------------------")
# print("Sent:     {}".format(sfdata))
# print("----------------------------------------")
# print("Received: {}".format(data))


# sock.close()
    