BSL Bridge Integration - Code Explanation
This document explains the functionality of bsl_bridge_integration.py, which processes sign language gestures from video streams and converts them to text by integrating with Firebase and a machine learning model.

Imports and Setup
python
import os
import cv2
import mediapipe as mp
import pickle
import numpy as np
from collections import Counter
import time
import nltk
from nltk.corpus import words
import difflib
import requests
import base64
import json
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
This code imports necessary libraries:

os and sys for system operations
cv2 (OpenCV) for image processing
mediapipe for hand landmark detection
pickle for loading the ML model
numpy for numerical operations
Counter for tracking gesture frequencies
time for timing operations
nltk for word suggestions
requests and base64 for HTTP communication and encoding
json for data serialization
firebase_admin for Firebase database integration
Stream ID Configuration
python
if len(sys.argv) > 1:
    input_stream_id = sys.argv[1]
    print(f"Using stream ID from command line: {input_stream_id}")
else:
    try:
        with open('active_stream.txt', 'r') as f:
            input_stream_id = f.read().strip()
            print(f"Using stream ID from file: {input_stream_id}")
    except FileNotFoundError:
        print("No stream ID provided and active_stream.txt not found. Please specify a stream ID.")
        sys.exit(1)
This section determines which video stream to process:

First checks for a stream ID from command-line arguments
Otherwise tries to read from an 'active_stream.txt' file
Exits if no stream ID is found
Word Dictionary Setup
python
try:
    nltk.download('words', quiet=True)
    word_dict = set(word.upper() for word in words.words())
    print("NLTK words downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK words: {e}")
    # Create a fallback dictionary with common words if NLTK fails
    word_dict = set(['HELLO', 'THANK', 'YOU', 'PLEASE', 'HELP', 'GOOD', 'BAD', 
                     'YES', 'NO', 'MAYBE', 'HOW', 'WHAT', 'WHERE', 'WHEN', 'WHO'])
This code:

Downloads NLTK's word corpus for word suggestions
Creates a set of uppercase words for matching detected gestures
Provides a fallback dictionary with common words if NLTK fails
Firebase Configuration
python
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    
    credential_paths = [
        'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json',
        os.path.join(script_dir, 'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json'),
        os.path.join(current_dir, 'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json'),
        os.path.join(os.path.dirname(current_dir), 'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json')
    ]
    
    cred_found = False
    for cred_path in credential_paths:
        if os.path.exists(cred_path):
            print(f"Found credentials at: {cred_path}")
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app/'
                })
                print(f"Firebase initialized with credentials from {cred_path}")
                cred_found = True
                break
            except Exception as e:
                continue
This code:

Searches for Firebase credentials in multiple locations
Initializes Firebase when valid credentials are found
Exits if no credentials can be found
MediaPipe and Model Setup
python
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    
    model_paths = [
        'model.p',
        os.path.join(script_dir, 'model.p'),
        os.path.join(current_dir, 'model.p'),
        os.path.join(os.path.dirname(current_dir), 'model.p')
    ]
    
    model_loaded = False
    for model_path in model_paths:
        if os.path.exists(model_path):
            print(f"Found model at: {model_path}")
            try:
                with open(model_path, 'rb') as f:
                    model_dict = pickle.load(f)
                    if 'model' in model_dict:
                        model = model_dict['model']
                        print(f"Model loaded from {model_path}")
                        model_loaded = True
                        break
            except Exception as e:
                continue
This code:

Initializes MediaPipe for hand tracking with specific settings
Searches for the trained model file in multiple locations
Loads the model when found
Gesture Detection Setup
python
gesture_list = []
current_input = ""
detected_words = []
previous_letter = None
last_time = time.time()
last_detected_time = time.time()
translation_data_file = "translation_data.json"
This code initializes variables for gesture detection:

gesture_list: Recent gestures to identify consistent patterns
current_input: Current word being built from gestures
detected_words: List of completed words
Time variables to track gesture timings
Path for saving translation output
Helper Functions
Update Translation Data
python
def update_translation_data(translation):
    """Update the translation data file used by the Express server."""
    try:
        data = {
            "translation": translation,
            "timestamp": int(time.time())
        }
        
        with open(translation_data_file, 'w') as f:
            json.dump(data, f)
            
        # Also try to update via HTTP endpoint (as a backup)
        try:
            requests.post('http://localhost:3000/update-translation', 
                         json={"translation": translation},
                         timeout=1)
        except Exception as e:
            print(f"HTTP update failed (continuing): {e}")
            pass
            
        print(f"Translation updated: {translation}")
        return True
    except Exception as e:
        print(f"Error updating translation data: {e}")
        return False
This function:

Updates the translation output to a local file
Attempts to send the translation via HTTP to a local server
Provides redundancy by using both file and HTTP methods
Drawing Hand Landmarks
python
def drawLandmarks(img, hand_landmarks):
    mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )
This function draws hand landmarks on the image for visualization.

Gesture Identification
python
def get_most_frequent_gesture(gesture_list, threshold=0.7):
    counts = Counter(gesture_list)
    total_gestures = len(gesture_list)
    for gesture, count in counts.items():
        if count / total_gestures >= threshold:
            return gesture
    return None
This function:

Counts occurrences of each gesture in the list
Returns a gesture if it appears consistently (above threshold)
Returns None if no gesture is consistent enough
Word Suggestions
python
def get_word_suggestions(fragment, dictionary, num=3):
    if not fragment:
        return []
    return difflib.get_close_matches(fragment, dictionary, n=num, cutoff=0.6)
This function finds potential matching words based on the current input fragment.

Base64 to Image Conversion
python
def base64_to_image(base64_string):
    """Convert base64 string to an OpenCV image."""
    try:
        img_data = base64.b64decode(base64_string)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("Warning: Decoded image is None")
            return None
        return img
    except Exception as e:
        print(f"Error converting base64 to image: {e}")
        return None
This function converts a base64-encoded image string to an OpenCV image for processing.

Stream Management Functions
Get Available Streams
python
def get_available_streams(piid=None):
    """Get list of active streams from Firebase, optionally filtered by PIID."""
    try:
        streams_ref = db.reference('/streams')
        streams = streams_ref.get()
        active_streams = {}
        
        if streams:
            for stream_id, stream_data in streams.items():
                status = stream_data.get('status', 'unknown')
                # Only include streams for the specified PIID if provided
                if piid:
                    stream_piid = stream_data.get('piid', None)
                    if stream_piid != piid:
                        continue
                
                if status == 'active':
                    active_streams[stream_id] = stream_data
        
        return active_streams
    except Exception as e:
        print(f"Error getting available streams: {e}")
        return {}
This function:

Queries Firebase for available video streams
Optionally filters streams by Raspberry Pi ID (PIID)
Returns a dictionary of active streams
Process Frame
python
def process_frame(frame):
    """Process a single frame using the BSL model."""
    global gesture_list, current_input, detected_words, previous_letter, last_time, last_detected_time
    
    if frame is None:
        print("Warning: Received None frame in process_frame")
        return None, {
            "current_input": current_input,
            "suggestions": [],
            "detected_words": detected_words
        }
    
    data_aux = []
    x_coords = []
    y_coords = []
    
    try:
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)
        
        predicted_character = ""
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks[:2]:
                drawLandmarks(frame, hand_landmarks)
            
            if len(result.multi_hand_landmarks) == 1:
                hand = result.multi_hand_landmarks[0]
                for landmark in hand.landmark:
                    data_aux.extend([landmark.x, landmark.y])
                    x_coords.append(landmark.x)
                    y_coords.append(landmark.y)
                data_aux.extend([0.0] * 42)  # Padding for second hand
            else:
                for hand in result.multi_hand_landmarks[:2]:
                    for landmark in hand.landmark:
                        data_aux.extend([landmark.x, landmark.y])
                        x_coords.append(landmark.x)
                        y_coords.append(landmark.y)
This code processes each frame by:

Converting the frame to RGB for MediaPipe
Detecting hand landmarks
Extracting landmark coordinates
Adding padding when only one hand is detected
Making Predictions
python
            data_aux_np = np.array(data_aux).reshape(1, -1)
            
            # Check if the model input shape matches
            expected_features = model.n_features_in_ if hasattr(model, 'n_features_in_') else None
            actual_features = data_aux_np.shape[1]
            
            if expected_features is not None and expected_features != actual_features:
                print(f"Input shape mismatch: model expects {expected_features} features, but got {actual_features}")
                # Try to fix by padding or truncating
                if actual_features < expected_features:
                    padding = np.zeros((1, expected_features - actual_features))
                    data_aux_np = np.hstack((data_aux_np, padding))
                else:
                    data_aux_np = data_aux_np[:, :expected_features]
            
            prediction = model.predict(data_aux_np)
            predicted_character = prediction[0].upper()
            
            gesture_list.append(predicted_character)
            if len(gesture_list) > 10:
                gesture_list.pop(0)
            
            most_frequent_gesture = get_most_frequent_gesture(gesture_list)
            if most_frequent_gesture:
                current_time = time.time()
                if most_frequent_gesture != previous_letter or (current_time - last_time) > 1:
                    current_input += most_frequent_gesture.upper()
                    print("Current Input Buffer:", current_input)
                    previous_letter = most_frequent_gesture
                    last_time = current_time
                    last_detected_time = current_time
This code:

Reshapes the landmark data for model input
Handles input shape mismatches by padding or truncating
Predicts the gesture using the model
Maintains a sliding window of recent gestures
Adds a new letter to the current input when:
The gesture is detected consistently
The gesture is different from the previous one or enough time has passed
Word Completion and Saving
python
        suggestions = get_word_suggestions(current_input, word_dict)
        
        if time.time() - last_detected_time > 3.5 and current_input:
            finalized_word = suggestions[0] if suggestions else current_input
            detected_words.append(finalized_word)
            print("Finalized Word:", finalized_word)
            current_input = ""
            last_detected_time = time.time()
            
            # Create final sentence and update outputs
            final_sentence = " ".join(detected_words)
            
            # Update translation data
            update_translation_data(final_sentence)
This code:

Gets word suggestions based on the current input
If no new gesture has been detected for 3.5 seconds and there's input:
Finalizes the word (uses the top suggestion if available)
Adds the word to the detected words list
Resets the current input buffer
Creates a sentence from all detected words
Updates the translation output
Stream Processing Functions
Display Debug Information
python
def display_debug_info(frame, translation_info):
    """Add debug info to the displayed frame."""
    try:
        H, W, _ = frame.shape
        
        # Add current input buffer
        cv2.putText(frame, f"Input: {translation_info['current_input']}", 
                    (10, H - 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add word suggestions
        if translation_info['suggestions']:
            suggestions_str = ", ".join(translation_info['suggestions'][:3])
            cv2.putText(frame, f"Suggestions: {suggestions_str}", 
                        (10, H - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add detected words
        detected_str = " ".join(translation_info['detected_words'][-3:])
        cv2.putText(frame, f"Detected: {detected_str}", 
                    (10, H - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    except Exception as e:
        print(f"Error in display_debug_info: {e}")
        return frame
This function adds debug information to the displayed frame:

The current input buffer
Word suggestions based on the current input
Recently detected words
Start Stream Processing
python
def start_stream_processing(stream_id):
    """Start processing frames from the selected stream."""
    print(f"Starting to process stream: {stream_id}")
    
    # Get stream info to verify PIID
    stream_ref = db.reference(f'/streams/{stream_id}')
    stream_data = stream_ref.get()
    
    if stream_data and 'piid' in stream_data:
        print(f"Stream PIID: {stream_data['piid']}")
    
    # Get reference to the latest frame
    latest_frame_ref = db.reference(f'/streams/{stream_id}/latest_frame')
    
    # For displaying frames locally (optional)
    debug_window_enabled = True
    try:
        cv2.namedWindow("BSL Processing", cv2.WINDOW_NORMAL)
        print("Debug window created successfully")
    except Exception as e:
        print(f"Warning: Could not create debug window: {e}")
        print("Continuing without visual debug output")
        debug_window_enabled = False
This code sets up stream processing:

Verifies the stream exists in Firebase
Gets a reference to the latest frame in the stream
Creates a debug window if possible
Stream Processing Loop
python
    last_frame_number = -1
    running = True
    last_status_check = time.time()
    error_count = 0
    max_errors = 10
    
    # Initialize with empty translation
    update_translation_data("BSL Translation will appear here...")
    
    while running:
        try:
            # Periodically check if the stream is still active
            current_time = time.time()
            if current_time - last_status_check > 30:  # Check every 30 seconds
                stream_ref = db.reference(f'/streams/{stream_id}')
                stream_data = stream_ref.get()
                if not stream_data or stream_data.get('status') != 'active':
                    print(f"Stream {stream_id} is no longer active.")
                    running = False
                    break
                last_status_check = current_time
            
            # Get the latest frame data
            frame_data = latest_frame_ref.get()
            
            if not frame_data or 'data' not in frame_data:
                print("No frame data available")
                time.sleep(0.5)
                continue
            
            # Check if this is a new frame
            if 'frame_number' in frame_data and frame_data['frame_number'] == last_frame_number:
                time.sleep(0.1)  # Short sleep to avoid excessive polling
                continue
            
            # Convert base64 to image
            frame = base64_to_image(frame_data['data'])
            if frame is None:
                print("Failed to decode frame")
                error_count += 1
                if error_count >= max_errors:
                    print(f"Too many errors ({error_count}). Restarting...")
                    time.sleep(5)
                    error_count = 0
                time.sleep(0.5)
                continue
            
            # Process the frame
            processed_frame, translation_info = process_frame(frame)
This code manages the continuous stream processing:

Periodically checks if the stream is still active
Retrieves the latest frame data from Firebase
Skips processing if the frame hasn't changed
Converts the base64-encoded frame to an image
Processes the frame and gets translation information
Handles errors by implementing a retry mechanism
Device Identification and Main Functions
Get Device PIID
python
def get_device_piid():
    """Get the PIID (Raspberry Pi ID) of the current device."""
    try:
        # First try to read from a config file
        config_paths = [
            'device_config.json',
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_config.json'),
            os.path.join(os.getcwd(), 'device_config.json')
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        if 'piid' in config:
                            print(f"PIID loaded from config file: {config_path}")
                            return config['piid']
                except Exception as e:
                    print(f"Error reading config from {config_path}: {e}")
                    continue
This function identifies the current device:

Attempts to read a device ID from configuration files
Falls back to creating an ID based on hardware information
Saves the ID to a config file for future use
Main Function
python
def main():
    """Main function to start the BSL interpreter."""
    print("BSL Bridge Integration Starting...")
    
    # Get the device PIID
    device_piid = get_device_piid()
    if device_piid:
        print(f"Device PIID: {device_piid}")
    else:
        print("Warning: Could not determine device PIID")
        device_piid = "1"  # Default fallback
    
    # Use the stream ID from command line or file
    stream_id = input_stream_id
The main function orchestrates the application:

Gets the device ID
Verifies the stream exists and is active
Presents options for stream selection if needed
Handles stream ownership and PIID assignments
Starts processing the selected stream
Application Flow
The script starts by identifying a stream ID and device ID
It initializes libraries, loads the model, and connects to Firebase
It continuously processes frames from the stream:
Detects hand landmarks
Predicts gestures from landmarks
Accumulates consistent gestures into letters
Assembles letters into words
Displays debug information and translation results
The translation is continuously updated to both a local file and web server
The script handles errors gracefully and can recover from most issues
The application provides real-time sign language translation by combining:

Computer vision (OpenCV and MediaPipe)
Machine learning (the pre-trained gesture model)
Word prediction (NLTK)
Cloud integration (Firebase)
