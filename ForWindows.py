import socket
import re, uuid
import winapps
import json
import sys
import psutil
import windows_tools.product_key
import windows_tools.registry
import winreg

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
sfd=list()

for item in winapps.list_installed():
    # Sfd = [item.name, item.version, item.install_date, item.install_location, item.install_source, item.install_source, item.modify_path, item.publisher, item.uninstall_string]
    sfd=list()
    sfd.append(str(item.name))
    sfd.append(str(item.version))
    sfd.append(str(item.install_date))
    sfd.append(str(item.install_location))
    sfd.append(str(item.install_source))
    sfd.append(str(item.modify_path))
    sfd.append(str(item.publisher))
    sfd.append(str(item.uninstall_string))
    sf.append(sfd)
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
    print("\n")
    sfd.clear


X = {
    "Hostname": hostname,
    "IP Address": ip_address,
    "MAC Address": mac,
    "Windows Product Key": value,
    "Softwares Installed": sf
}
sfdata= json.dumps(X)
print(X)

#--------------------------------------------------------

host = "localhost"
port = 12345

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket()
sock.connect((host,port))
sfdata = bytes(sfdata,'utf-8')
sock.sendall(sfdata)
data = sock.recv(100000)
print("-------------------------------------")
print(data)

print("----------------------------------------")
print("Sent:     {}".format(sfdata))
print("----------------------------------------")
print("Received: {}".format(data))


sock.close()
    