BSL Bridge Integration Documentation
Overview
bsl_bridge_integration.py is a Python script that processes British Sign Language (BSL) gestures from a video stream and translates them into text in real-time. The script connects to a Firebase database to retrieve video frames from active streams, processes these frames using a pre-trained machine learning model to recognize hand gestures, and outputs the translated text.
Features

Real-time BSL gesture recognition and translation
Integration with Firebase Realtime Database for retrieving video frames
Device identification via PIID (Raspberry Pi ID)
Support for multiple active video streams
Word prediction and suggestions based on detected gestures
Visual debugging window showing hand landmarks and detection results
Automatic translation output via local file and HTTP endpoint

Requirements
Hardware

Recommended: Raspberry Pi 4 (or newer) with camera module
Alternative: Any computer with webcam access

Software Dependencies

Python 3.7+
OpenCV (cv2)
MediaPipe
NumPy
NLTK
Firebase Admin SDK
Requests
Other Python standard libraries

Installation

Clone the repository or download the script file:

bashgit clone [repository-url]
cd [repository-directory]

Install required Python packages:

bashpip install opencv-python mediapipe numpy nltk requests firebase-admin

Download NLTK words corpus:

bashpython -c "import nltk; nltk.download('words')"

Place the required files in the same directory as the script:

model.p - Trained machine learning model for BSL recognition
bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json - Firebase credentials file



Configuration
Firebase Setup

Create a Firebase project (if you don't have one)
Generate a private key file for your service account
Place the downloaded JSON credentials file in the script directory

Device Configuration
The script automatically generates a device_config.json file with a unique PIID (Raspberry Pi ID) for your device. This helps in identifying which streams belong to which device.
Usage
Basic Usage
bashpython bsl_bridge_integration.py [stream_id]
If stream_id is not provided as a command-line argument, the script will check for an active_stream.txt file or prompt you to select an available stream.
Stream Selection
When starting the script without specifying a stream ID:

The script will check for active streams associated with your device
If no streams are found for your device, it will display all active streams
You can:

Select a stream from another device
Assign an existing stream to your device
Exit the program



Running as a Service
To run the script as a background service on startup:

Create a systemd service file (on Linux/Raspberry Pi):

bashsudo nano /etc/systemd/system/bsl_bridge.service

Add the following content:

[Unit]
Description=BSL Bridge Integration Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/bsl_bridge_integration.py
WorkingDirectory=/path/to/script/directory
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

Enable and start the service:

bashsudo systemctl enable bsl_bridge.service
sudo systemctl start bsl_bridge.service
How It Works

Stream Connection: The script connects to Firebase and retrieves information about active video streams.
Frame Processing:

Retrieves the latest frame from the selected stream
Processes the frame using MediaPipe to detect hand landmarks
Applies the machine learning model to classify the hand gesture


Gesture Recognition:

Maintains a buffer of recent gesture detections
Uses a voting mechanism to determine the most likely letter being signed
Detects when a user has finished signing a letter


Word Formation:

Combines detected letters into words
Uses NLTK's word corpus to suggest complete words
Detects pauses to indicate word completion


Translation Output:

Writes the translated text to a local file (translation_data.json)
Optionally sends the translation to a local HTTP endpoint
Displays detected words and suggestions in the debug window



Debugging
The script includes a visual debugging window that shows:

Hand landmarks and connections
Current input buffer (detected letters)
Word suggestions
Recently detected words

To disable the debug window, set debug_window_enabled = False in the start_stream_processing function.
Troubleshooting
Common Issues

Model not found

Ensure model.p is in the script directory or one of the paths checked by the script
The model file should contain a dictionary with a 'model' key


Firebase credentials not found

Check that the Firebase JSON credentials file is in the script directory
Verify the filename matches what the script is looking for


No streams available

Make sure streams are active in your Firebase database
Check the structure of your Firebase database matches what the script expects


Gesture recognition not working properly

Ensure good lighting conditions
Position hands clearly in the camera's field of view
The model might need retraining for better accuracy



Data Structure
Firebase Database Structure
/streams
    /[stream_id]
        /status: "active" or "inactive"
        /piid: "device_identifier"
        /latest_frame
            /data: "base64_encoded_image"
            /frame_number: 123
            /timestamp: 1620000000
Translation Data File Structure
json{
    "translation": "HELLO WORLD",
    "timestamp": 1620000000
}
License
[Your license information here]
Contributors
[List of contributors]
Contact
For support or questions about this script, please contact:
[Your contact information]
