import os
import subprocess
import ctypes
import time



# Function to search for a file in a directory and its subdirectories
def search_exe_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe"):
                return os.path.join(root, file)
    return None


def extract_digital_signature(exe_file_path):
    try:
        # Run sigcheck command with the /a option to display file information,
        # including digital signatures, in CSV format
        result = subprocess.run(['sigcheck', '-a', '-nobanner', exe_file_path], capture_output=True, text=True)
        print(result)
        if result.returncode == 0:
            # Extract the digital signature information from the command output
            output_lines = result.stdout.splitlines()
            print(output_lines)
            for line in output_lines:
                if line:
                    return line.strip().split(":")[1].strip()
        else:
            print("Failed to extract digital signature:", result.stderr)
    except Exception as e:
        print("Error:", e)
    return None

# Example usage:
path = "C:/Program Files/Android/Android Studio"  # Replace with the path you want to search in
found_file = search_exe_file(path)

if found_file:
    print("File found at: ", found_file)
    exe_file_path = C:\Program Files\Android\Android Studio\uninstall.exe
    signature = extract_digital_signature(exe_file_path)
    if signature:
        print("Digital signature:", signature)
    else:
        print("No digital signature found.")
    
else:
    print("File not found.")
