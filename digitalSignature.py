import os
import sys
import win32api
import win32con
import win32security

def get_digital_signature(filepath):
    try:
        # Get file version info
        info = win32api.GetFileVersionInfo(filepath, "\\")
        # Get digital signature info
        ms = info['StringFileInfo']['Microsoft Corporation']['DigitalSignature']
        # Convert to dictionary
        return eval(ms)
    except KeyError:
        # No digital signature found
        return None
    except:
        # Other error occurred
        return "Error"

def main():
    try:
        # Get list of installed programs from registry
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall", 0, win32con.KEY_READ)
        programs = []
        for i in range(0, win32api.RegQueryInfoKey(key)[0]):
            programs.append(win32api.RegEnumKey(key, i))
        win32api.RegCloseKey(key)
        # Iterate over installed programs and print digital signature info
        for program in programs:
            try:
                # Get program display name
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\{}".format(program), 0, win32con.KEY_READ)
                name = win32api.RegQueryValueEx(key, "DisplayName")[0]
                win32api.RegCloseKey(key)
                # Get program installation directory
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\{}".format(program), 0, win32con.KEY_READ)
                directory = win32api.RegQueryValueEx(key, "InstallLocation")[0]
                win32api.RegCloseKey(key)
                # Get program executable path
                path = os.path.join(directory, "{}.exe".format(program))
                if os.path.exists(path):
                    # Get digital signature info for executable
                    sig = get_digital_signature(path)
                    if sig is not None:
                        print("Digital signature info for {}: {}".format(name, sig))
                    else:
                        print("No digital signature found for {}".format(name))
                else:
                    print("Executable not found for {}".format(name))
            except:
                print("Error processing program {}".format(program))
    except:
        print("Error retrieving list of installed programs")

if __name__ == '__main__':
    main()