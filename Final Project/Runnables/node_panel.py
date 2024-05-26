import platform
import sys
import os
# Get the system's platform
system = platform.system()

# Check if the platform is macOS or Windows
if system == "Darwin":
    cmd = 'python ForMac2.py ' + sys.argv[1]
    os.system(cmd)
elif system == "Windows":
    cmd = 'python ForWindowsFinal.py ' + sys.argv[1]
    os.system(cmd)
else:
    print("This device is not running macOS or Windows.")
