import winreg
import winapps

def fetch_executable_path(app_name):
    # Fetch the InstallLocation registry value for the software from multiple locations
    registry_locations = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for loc in registry_locations:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fr"{loc}\{app_name}")
            install_location = winreg.QueryValueEx(key, "InstallLocation")[0]
            winreg.CloseKey(key)
            return install_location
        except FileNotFoundError:
            pass
    return None

# Get list of all installed software
apps = winapps.list_installed()

# Iterate through the list of installed software
for app in apps:
    # Get the main executable file path for the software
    app_name = app.name
    app_path = fetch_executable_path(app_name)
    if app_path:
        print(f"Software: {app_name}")
        print(f"Executable path: {app_path}")
        print("---")
