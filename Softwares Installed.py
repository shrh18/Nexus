import winapps
 
# get each application with list_installed()
for item in winapps.list_installed():
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
    