# Raspberry Pi On/Off Button Control for BSL translator
## Hardware Components

The script interfaces with:
- Grove RGB LCD Display (v4.0)
- Grove Button (connected to digital port D3)

```python
#!/usr/bin/env python
# BSL Bridge translation device with LCD display and button control
# Uses Grove LCD RGB Backlight v4.0 and Grove Button
import time
import subprocess
import signal
from grovepi import *
import grove_rgb_lcd

# Set up the Grove button on digital port D3
button_port = 3
# Set the pin mode for the button as INPUT
pinMode(button_port, "INPUT")
```

## Button State Tracking

The script keeps track of the button state to detect presses and implements a debounce mechanism to avoid multiple triggers from a single press.

```python
# Variables for button state tracking
previous_state = 0
stream_process = None
is_running = True  # Start with the stream already running
debounce_time = 0.2  # Longer debounce time for script control
```

## Livestream Script Management

The script manages the execution of the livestreaming Python script as a subprocess.

```python
# Path to the live stream script
LIVE_STREAM_PATH = "/home/pi/Desktop/codes/CodeWorks/live_stream.py"
```

## LCD Initialization and Welcome Sequence

The LCD display is initialized with a welcome sequence that shows the BSL Bridge name and the device ID.

```python
# Initialize LCD
try:
    # Display initial message
    grove_rgb_lcd.setRGB(0, 0, 255)  # Blue color
    grove_rgb_lcd.setText("Welcome to BSL\nBridge")
    time.sleep(5)
    # Display device ID
    grove_rgb_lcd.setText("This device ID\nis 1")
    time.sleep(5)
    # Set to standby state initially
    grove_rgb_lcd.setRGB(255, 165, 0)  # Orange for standby
    grove_rgb_lcd.setText("ON STANDBY...\nCAMERA OFF")
```

## Auto-Starting the Livestream

The script automatically starts the livestream service when it first runs.

```python
# Auto-start the stream at launch
print("Hi")
stream_process = subprocess.Popen(["python3", LIVE_STREAM_PATH])
# Update LCD to show running state
grove_rgb_lcd.setRGB(0, 255, 0)  # Green for active
grove_rgb_lcd.setText("SENDING TRANSLATION\nCAMERA ON")
```

## Main Button Control Loop

The main loop continuously monitors the button state and toggles the livestream service on/off when the button is pressed.

```python
try:
    while True:
        try:
            # Read the current button state
            current_state = digitalRead(button_port)
            # Check if button was pressed (transition from 0 to 1)
            if previous_state == 0 and current_state == 1:
                # Button was just pressed
                if is_running:
                    # Stop the script
                    print("Bye")
                    if stream_process:
                        stream_process.send_signal(signal.SIGTERM)
                        stream_process.wait()  # Wait for process to terminate
                        stream_process = None
                    is_running = False
                    # Update LCD for standby state
                    grove_rgb_lcd.setRGB(255, 165, 0)  # Orange for standby
                    grove_rgb_lcd.setText("ON STANDBY...\nCAMERA OFF")
                else:
                    # Start the script - using python3 explicitly
                    print("Hi")
                    stream_process = subprocess.Popen(["python3", LIVE_STREAM_PATH])
                    is_running = True
                    # Update LCD for active state
                    grove_rgb_lcd.setRGB(0, 255, 0)  # Green for active
                    grove_rgb_lcd.setText("SENDING TRANSLATION\nCAMERA ON")
                time.sleep(debounce_time)  # Prevent multiple triggers
            previous_state = current_state
            time.sleep(0.01)  # Small delay to reduce CPU usage
        except IOError as e:
            print("Error reading from button:", e)
            time.sleep(0.1)
```

## Visual Feedback System

The LCD display provides visual feedback about the system status through both text and color:

1. **Blue** - Welcome and initialization messages
2. **Orange** - Standby mode (camera off)
3. **Green** - Active translation mode (camera on)

```python
# Example for active state
grove_rgb_lcd.setRGB(0, 255, 0)  # Green for active
grove_rgb_lcd.setText("SENDING TRANSLATION\nCAMERA ON")

# Example for standby state
grove_rgb_lcd.setRGB(255, 165, 0)  # Orange for standby
grove_rgb_lcd.setText("ON STANDBY...\nCAMERA OFF")
```

## Error Handling and Cleanup

The script includes error handling for both button reading errors and graceful cleanup when the program is interrupted.

```python
except KeyboardInterrupt:
    print("\nProgram stopped by user")
    # Make sure to clean up the subprocess if it's running
    if stream_process and is_running:
        print("Stopping live stream script...")
        stream_process.send_signal(signal.SIGTERM)
        stream_process.wait()
    # Clear LCD before exiting
    grove_rgb_lcd.setRGB(0, 0, 0)
    grove_rgb_lcd.setText("")
except Exception as e:
    print("Error initializing LCD:", str(e))
    print("Make sure your LCD is connected to an I2C port, not D5")
```
