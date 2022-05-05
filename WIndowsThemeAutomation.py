import subprocess
import winreg
import calendar
from time import sleep, strptime
from datetime import datetime, timedelta


change_theme_to_dark_time = "23:59:60"
change_theme_to_light_time = "7:00:00"

# Function to run powershell scripts
def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

# Function to change the windows theme
def changeTheme(theme="d"):
    if theme == "d":
        Ax = 0
    elif theme == "w":
        Ax = 1
    else:
        print("what?")
        return
    powershell_cmd = f"Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value {Ax}" # Registry key of the theme for the current user
    run(powershell_cmd)

# Compare the current time with the given time
def compareTime(changeTime):
    now = datetime.now()
    my_time_string = changeTime # leap second, must be in HH:mm:ss
    my_time_string = now.strftime("%Y-%m-%d") + " " + my_time_string # I am supposing the date must be the same as now
    my_time = strptime(my_time_string, "%Y-%m-%d %H:%M:%S")
    my_datetime = datetime(1970, 1, 1) + timedelta(seconds=calendar.timegm(my_time))

    if now > my_datetime:
        return True
    else:
        return False

# Check if dark mode is currently on
def darkmode_is_enabled(): 
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False

# if __name__ == "__main__" because obviously
if __name__ == "__main__":
    while True:
        if compareTime(change_theme_to_dark_time) == True:
            if darkmode_is_enabled():
                pass
            else:
                changeTheme("d")
                print("turned on dark mode")

        if compareTime(change_theme_to_light_time) == True:
            if darkmode_is_enabled():
                changeTheme("w")
                print("turned on light mode")
            else:
                pass
        
        sleep(59)
