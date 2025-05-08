# BSL Bridge
<img src="https://github.com/JamesW162/Group9Project/blob/main/project/server/website/logo.png" alt="BSL Translator Logo" width="300">
A real-time British Sign Language (BSL) translation system using machine learning, computer vision, and cloud integration. This project uses MediaPipe for hand detection and a custom ML model to classify hand gestures, converting them into text through real-time video processing.
Built with Python 3.11.9
Demo
Show Image
System Architecture
Our translation system follows this process flow:

Capture: Raspberry Pi camera captures hand gestures
Transmit: Video frames are sent to Firebase in real-time
Process: ML model processes frames to detect and classify gestures
Translate: Signs are converted to text with auto-correction
Display: Results appear on web interface and can be sent back to the Pi

For detailed architecture information, see our System Design Documentation.
Project Contents

/project/server - Main server implementation

Express.js backend
API endpoints for BSL translation
Firebase integration


/project/server/BSL_bridge_integration.py - Core ML processing script
/project/server/website - Frontend website files
/RaspberryPi - Raspberry Pi implementation scripts
/documentation - Project documentation

User Guide - How to use the system
Technical Overview - Technical details
Installation Guide - Detailed setup instructions
API Documentation - API reference



Installation
Prerequisites

Python 3.11.9
Node.js & npm
Git
Firebase account

PC/Laptop Setup

Clone the repository:

bashgit clone https://github.com/JamesW162/Group9Project
cd Group9Project

Set up the Python environment:

bashpython -m venv myenv
myenv\Scripts\activate  # On Windows
source myenv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

Set up the server:

bashcd project/server
npm install
npm install firebase express body-parser cors

Add Firebase credentials:

Download bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json following instructions below
Place it in the Group9Project/project/server directory


Verify installation:

bashpython fix.py

Start the server:

bashnode server.js
Firebase Credentials Setup

Go to Firebase Console and log in
Select the project associated with bsltranslator-93f00
Click the ⚙️ gear icon → Project settings
Navigate to the Service accounts tab
Under Firebase Admin SDK, click "Generate new private key"
Save the downloaded JSON file as bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json
Place this file in Group9Project/project/server


IMPORTANT: This file contains sensitive credentials. Do not expose it publicly.

Raspberry Pi Setup

Set up the hardware:

Connect camera to Raspberry Pi camera pins
Connect red LED button to port D2
Connect Grove-LCD RGB Backlight to port I2C

Show Image
Copy required files from repository:

/RaspberryPi/live_stream_pi_code.py
/RaspberryPi/on_off_button_pi_code.py
/RaspberryPi/requirements.txt


Install dependencies:

bashpip install -r requirements.txt

Run the control script:

bashpython on_off_button_pi_code.py
NOTE: Please create a folder called templates and place index.html and logo.png inside it.
How Everything Works
1. Data Collection & Model Training
To build your own model:

Run collect_images.py:

Captures hand gestures for training the ML model
Currently configured for 3 letters (A, B, L)
Customize number_of_classes and data_dict path as needed


Run process_data_for_training.py:

Processes collected data for ML model training


Run train_classifier.py:

Creates model.p file needed for inference



For more details, see our Machine Learning Documentation.
2. BSL Translation Process
The translation involves these key components:
Server-side Processing
The BSL_bridge_integration.py script:

Uses MediaPipe to detect hand landmarks (21 points per hand)
Applies our trained model to classify gestures
Implements gesture stabilization for accurate readings
Provides auto-correction for better text prediction
Synchronizes with Firebase for real-time updates

Cloud Integration
Our Firebase implementation:

Stores video frames from the Raspberry Pi
Maintains stream metadata and status information
Secures access with unique device IDs (PIIDs)
Supports real-time data synchronization

Show Image
Web Interface
The web application:

Authenticates users securely
Displays live video streams
Shows translated text in real-time
Provides controls for stream management
Includes loading animations and error handling

Show Image
3. Raspberry Pi Implementation
The Raspberry Pi runs two main scripts:

on_off_button_pi_code.py: Controls the hardware interface

Initializes the LCD display
Monitors button presses
Starts/stops the livestream


live_stream_pi_code.py: Handles video streaming

Captures frames from the camera
Compresses and encodes frames to base64
Uploads frames to Firebase
Manages stream lifetime and resources



Configuration parameters:
pythonFRAME_RATE = 3  # Frames per second (do not exceed 5)
RESOLUTION = (320, 240)  # Video resolution
QUALITY = 20  # JPEG compression quality
MAX_STREAM_TIME = 300  # Maximum streaming time (5 minutes)
4. System Architecture Diagrams
Data flow through our system:
Show Image
Alternative cloud processing model:
Show Image
Server structure:
Show Image
BSL Reference
Use this BSL fingerspelling chart for reference:
Show Image
Video Tutorial
For additional help, watch our reference tutorial:
Show Image
Current Features

✅ Real-time hand gesture detection
✅ Translation of BSL fingerspelling to text
✅ Auto-correction for improved accuracy
✅ Cloud-based video streaming
✅ Web interface for viewing translations
✅ Raspberry Pi integration with hardware feedback

Future Development

Improve the AI model accuracy
Optimize connection speed
Expand gesture vocabulary beyond fingerspelling
Implement sentence construction
Add mobile application support

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

MediaPipe team for their hand tracking technology
Firebase for cloud infrastructure
All contributors to the BSL translation project


For questions or support, please open an issue on this repository.
