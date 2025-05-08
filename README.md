# SIGN LANGUAGE TRANSLATOR

This project uses Mediapipe for hand detection and ML model to classify gestures. The system uses real-time video input from a camera to detect hand landmarks and predict what letter the hand gesture relates to. It is built using version 3.11.9 of Python.

![Logo](https://github.com/JamesW162/Group9Project/blob/main/project/server/website/logo.png)

## Installation

### Installation on a laptop/pc

```
git clone https://github.com/JamesW162/Group9Project
cd Group9Project
```

Open VS code in the Group9Project and run these commands in the terminal:

```
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
cd project
cd server
npm install
npm install firebase
npm install express body-parser cors
```

You then need to add `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json` from Firebase.

#### Steps to Download Your Firebase Admin SDK JSON File
- Go to Firebase Console: Visit Firebase Console and log in.
- Select Your Project: Click on the project associated with bsltranslator-93f00.
- Open Project Settings:
  - Click on the ⚙️ gear icon in the left sidebar.
  - Choose Project settings.
- Navigate to Service Accounts:
  - In the Project settings, select the Service accounts tab.
  - Scroll down and find Firebase Admin SDK.
- Generate a New Private Key:
  - Click Generate new private key.
  - This will download a JSON file (firebase-adminsdk-xxxxx.json).

**Important Notes**
- Handle with care! This file contains sensitive credentials. Do not expose it publicly.
- Use in your backend: Place it in a secure location where only authorized applications can access it.
- **MAKE SURE** to save it as `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json`
- **MAKE SURE** IT IS SAVED IN `Group9Project/project/server`

To make sure everything is installed, run:

```
python fix.py
```

If there are any missing dependencies, type `y` to fix them. OpenCV sometimes has issues, so you may need to run `pip install opencv-python`. Similarly, scikit-learn can be problematic, so try `pip install scikit-learn` if needed.

To start running the server:
```
node server.js
```

### Installation on the Raspberry Pi

First, set up the Pi as shown below:
- Camera plugged into the Raspberry Pi camera pins
- Red LED button connected to port D2
- Grove-LCD RGB Backlight connected to port I2C

![Raspberry Pi Setup](https://github.com/user-attachments/assets/61e809d4-83b1-43b0-ab5d-4606c24fc7a9)

The only files you need from the repository are in the **`/RaspberryPi`** folder:
- `live_stream_pi_code.py`
- `on_off_button_pi_code.py`
- `requirements.txt`

```
pip install -r requirements.txt
```

Open and run `on_off_button_pi_code.py`

**NOTE: PLEASE PUT THE `index.html` AND `logo.png` INTO A FOLDER CALLED `templates`**

## How Everything Works

### Server.js
The website backend runs using Express.js to handle communication between the BSL interpreter Python scripts and the front-end website. It manages API endpoints that read and update the translation data and provide error messages when problems occur.

### BSL_bridge_integration.py
This Python script implements real-time British Sign Language gesture recognition using OpenCV, MediaPipe, and a pre-trained ML model. It detects hand landmarks (21 points per hand) and predicts hand gestures, converting them to text through these steps:
1. Hand detection using MediaPipe
2. Landmark extraction and classification
3. Gesture stabilization to prevent duplicate predictions
4. Auto-correction to improve word prediction

### Firebase_stream_handler.py
This script handles the conversion of base64-encoded images back to actual images for display on the website and processing by the BSL translator. It manages two-way communication between the client computer and Firebase.

### Raspberry Pi Implementation
The Raspberry Pi runs two main scripts:
- `on_off_button_pi_code.py`: Controls the LCD and camera based on button presses
- `live_stream_pi_code.py`: Captures and streams video frames to Firebase

Configuration parameters:
```python
FRAME_RATE = 3  # Do not exceed 5 FPS due to storage limitations
RESOLUTION = (320, 240)  # Lower resolution for better performance
QUALITY = 20  # JPEG compression quality
MAX_STREAM_TIME = 300  # Maximum streaming time (5 minutes)
```

### Website Interface
The web application includes:
- Authentication pages (login, signup)
- Main translator interface (webpage.html)
- Stream connection and management
- Real-time translation display

### BSL Letter Chart
![BSL Fingerspelling Chart](https://imgs.search.brave.com/DKomfn_cPKzVi7KigGeY5d0Jdn0WK72m8gxgMzOFH6M/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9hY2Nl/c3Nic2wuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDIyLzEx/LzIuYWNjZXNzYnNs/LUZpbmdlcnNwZWxs/aW5nLXJpZ2h0LWhh/bmQtMS5qcGc)

## Training Your Own Model

To train your own model:
1. Run `collect_images.py` to capture hand gestures
   - Configure `number_of_classes` for the number of letters (currently 3)
   - Update `data_dict` path to your computer
2. Run `process_data_for_training.py` to prepare the data
3. Run `train_classifier.py` to create the model.p file
4. Run `inference_classifier.py` to test the model
   - Update `labels_dict` to match your classes (currently `{0: 'A', 1: 'B', 2: 'L'}`)

## System Architecture

The data flows from the Raspberry Pi to Firebase, then to a PC/Laptop where the BSL is translated to text. The processed data is sent to:

1. The University's Cloud Webserver (backend for website and mobile interface)
2. ThingsBoard for output on the Raspberry Pi's speaker

![System Architecture](https://github.com/user-attachments/assets/803f0839-40de-431e-8479-3a3a09b21124)

## Firebase Integration

The system uses Firebase for real-time data storage and synchronization:
![Firebase Structure](https://github.com/user-attachments/assets/f8e41ac4-51ef-4f1f-825d-01f8e867b1da)

## Web Interface

The current web interface looks like this:
![Web Interface](https://github.com/user-attachments/assets/9ce45291-fea6-4419-8a29-9f95c9cedc46)

Server structure:
![Server Structure](https://github.com/user-attachments/assets/54ef874d-4d4b-492b-90f5-ad7d237ea908)

## Video Tutorial for Reference

[![Watch the tutorial on YouTube](https://img.youtube.com/vi/MJCSjXepaAM/0.jpg)](https://www.youtube.com/watch?v=MJCSjXepaAM)

## Future Development

- Improve the AI model
- Faster connection speeds
- Expand supported gestures
- Implement sentence construction
