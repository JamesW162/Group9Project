# BSL Bridge Implementation Guide

This guide explains how to set up and run the BSL Bridge system, which integrates a sign language interpreter with a Firebase-powered livestream solution.

## Overview

The system consists of these components:

1. **Firebase Realtime Database** - Hosts the video streams
2. **Web Interface** - Displays the livestream and translation results
3. **BSL Interpreter** - Processes video frames to detect sign language
4. **Integration Layer** - Connects all components together

## Setup Instructions

### 1. Firebase Setup

1. Create a Firebase project at [firebase.google.com](https://firebase.google.com)
2. Enable the Realtime Database
3. Download the service account credentials JSON file
4. Place the credentials file in your project directory as `firebase-credentials.json`

### 2. Install Dependencies

```bash
# Python dependencies
pip install opencv-python mediapipe numpy firebase-admin nltk pillow

# Web server (if needed)
# You can use XAMPP, Apache, or PHP's built-in server
```

### 3. File Organization

Place the files in the following structure:

```
project/
├── bsl_bridge_integration.py        # Main BSL integration script
├── firebase_stream_handler.py       # Helper for testing Firebase streams
├── firebase-credentials.json        # Your Firebase credentials
├── model.p                          # Your existing BSL model
├── website/
│   ├── index.html                   # Updated webpage
│   ├── update_translation.php       # Handles translation updates
│   ├── start_interpreter.php        # Starts the BSL interpreter
│   ├── translation_data.json        # Stores current translation
│   └── ... (other website files)
```

### 4. Running the System

#### Step 1: Start your web server
Make sure your web server is running and can serve the website files.

```bash
# If using PHP's built-in server
cd website
php -S localhost:8000
```

#### Step 2: Test Firebase connectivity
Test that you can connect to Firebase and list or create streams:

```bash
python firebase_stream_handler.py --list
# Or create a test stream from your webcam
python firebase_stream_handler.py --create
```

#### Step 3: Access the web interface
Open your browser and navigate to `http://localhost:8000` (or your server's URL)

#### Step 4: Connect to a stream and start the interpreter
1. Use the web interface to select and connect to a stream
2. Click "Start Interpreter" to begin processing the stream for sign language

## How It Works

1. **Video Stream Capture**:
   - Video frames are streamed from a source to Firebase
   - The web interface displays these frames

2. **BSL Interpreter**:
   - When activated, the BSL interpreter script processes frames from the selected stream
   - It uses MediaPipe to detect hands and your trained model to identify signs

3. **Translation Process**:
   - The interpreter detects hand gestures
   - It collects gestures into letters
   - Letters form words based on your existing detection logic
   - Words are combined into sentences

4. **Web Integration**:
   - Translation results are written to a JSON file
   - The webpage periodically checks for updates
   - Translations appear in the designated text box

## Troubleshooting

### Common Issues:

1. **Firebase Connection Errors**:
   - Verify your credentials file is correct
   - Check network connectivity
   - Ensure database rules allow read/write

2. **Interpreter Not Starting**:
   - Check PHP error logs
   - Verify Python path in `start_interpreter.php`
   - Make sure all dependencies are installed

3. **No Translations Appearing**:
   - Check write permissions for the translation_data.json file
   - Verify the correct stream is selected
   - Check if the interpreter is actively running

4. **Model Not Found**:
   - Ensure model.p is in the correct location
   - Check paths in the integration script

## Advanced Configuration

The `bsl_bridge_integration.py` script contains several parameters you can adjust:

- Change detection thresholds
- Adjust word formation timing
- Modify gesture recognition parameters

## Security Notes

- This implementation is for development/local use
- For production, add proper authentication and secure the Firebase rules
- Consider encrypting sensitive data

## Next Steps

To enhance this system, consider:
1. Adding user accounts with preferences
2. Implementing a more robust stream management system
3. Improving the sign language detection model
4. Adding translation history
5. Supporting multiple languages or dialects