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

# Check if a stream ID was provided as a command-line argument
if len(sys.argv) > 1:
    input_stream_id = sys.argv[1]
    print(f"Using stream ID from command line: {input_stream_id}")
else:
    # Otherwise, try to read from the active_stream.txt file
    try:
        with open('active_stream.txt', 'r') as f:
            input_stream_id = f.read().strip()
            print(f"Using stream ID from file: {input_stream_id}")
    except FileNotFoundError:
        print("No stream ID provided and active_stream.txt not found. Please specify a stream ID.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading stream ID file: {e}")
        sys.exit(1)

# Download NLTK word corpus
try:
    nltk.download('words', quiet=True)
    word_dict = set(word.upper() for word in words.words())
    print("NLTK words downloaded successfully")
except Exception as e:
    print(f"Error downloading NLTK words: {e}")
    # Create a fallback dictionary with common words if NLTK fails
    word_dict = set(['HELLO', 'THANK', 'YOU', 'PLEASE', 'HELP', 'GOOD', 'BAD', 
                     'YES', 'NO', 'MAYBE', 'HOW', 'WHAT', 'WHERE', 'WHEN', 'WHO'])

# Firebase configuration - try to load credentials
try:
    # Look for the credentials file in common locations
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    
    credential_paths = [
        'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json',
        os.path.join(script_dir, 'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json'),
        os.path.join(current_dir, 'bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json'),
        # Add parent directory as another possible location
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
                print(f"Failed to initialize Firebase with {cred_path}: {e}")
                continue
    
    if not cred_found:
        print("Firebase credentials file not found. Please ensure it exists in one of these locations:")
        for path in credential_paths:
            print(f"  - {path}")
        sys.exit(1)
        
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    sys.exit(1)

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Fixed: Changed static_image_mode to False for video stream processing
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.3)

# Load model
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()
    
    model_paths = [
        'model.p',
        os.path.join(script_dir, 'model.p'),
        os.path.join(current_dir, 'model.p'),
        # Add parent directory as another possible location
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
                    else:
                        print(f"Model file at {model_path} doesn't contain 'model' key")
            except Exception as e:
                print(f"Failed to load model from {model_path}: {e}")
                continue
    
    if not model_loaded:
        print("Model file not found. Please ensure model.p exists in one of these locations:")
        for path in model_paths:
            print(f"  - {path}")
        sys.exit(1)
        
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

# Variables for gesture detection
gesture_list = []
current_input = ""
detected_words = []
previous_letter = None
last_time = time.time()
last_detected_time = time.time()
translation_data_file = "translation_data.json"

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
                         timeout=1)  # Short timeout to prevent blocking
        except Exception as e:
            # If HTTP request fails, we still have the file update
            print(f"HTTP update failed (continuing): {e}")
            pass
            
        print(f"Translation updated: {translation}")
        return True
    except Exception as e:
        print(f"Error updating translation data: {e}")
        return False

def drawLandmarks(img, hand_landmarks):
    mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

def get_most_frequent_gesture(gesture_list, threshold=0.7):
    counts = Counter(gesture_list)
    total_gestures = len(gesture_list)
    for gesture, count in counts.items():
        if count / total_gestures >= threshold:
            return gesture
    return None

def get_word_suggestions(fragment, dictionary, num=3):
    if not fragment:
        return []
    return difflib.get_close_matches(fragment, dictionary, n=num, cutoff=0.6)

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

def get_available_streams():
    """Get list of active streams from Firebase."""
    try:
        streams_ref = db.reference('/streams')
        streams = streams_ref.get()
        active_streams = {}
        
        if streams:
            for stream_id, stream_data in streams.items():
                status = stream_data.get('status', 'unknown')
                if status == 'active':
                    active_streams[stream_id] = stream_data
        
        return active_streams
    except Exception as e:
        print(f"Error getting available streams: {e}")
        return {}

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
            
            # Skip if no landmarks were collected
            if not x_coords or not y_coords:
                return frame, {
                    "current_input": current_input,
                    "suggestions": get_word_suggestions(current_input, word_dict),
                    "detected_words": detected_words
                }
            
            x1 = int(min(x_coords) * W) - 10
            y1 = int(min(y_coords) * H) - 10
            x2 = int(max(x_coords) * W) + 10
            y2 = int(max(y_coords) * H) + 10
            
            try:
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
            except Exception as e:
                print(f"Error in prediction: {e}")
        
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
        
        # Return the processed frame and current translation
        return frame, {
            "current_input": current_input,
            "suggestions": suggestions,
            "detected_words": detected_words
        }
    except Exception as e:
        print(f"Exception in process_frame: {e}")
        return frame, {
            "current_input": current_input,
            "suggestions": get_word_suggestions(current_input, word_dict),
            "detected_words": detected_words
        }

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

def start_stream_processing(stream_id):
    """Start processing frames from the selected stream."""
    print(f"Starting to process stream: {stream_id}")
    
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
            
            # Reset error count on successful processing
            error_count = 0
            
            # Display debug info on frame if we have a valid processed frame
            if processed_frame is not None and debug_window_enabled:
                try:
                    display_frame = display_debug_info(processed_frame.copy(), translation_info)
                    
                    # Display the frame locally
                    cv2.imshow("BSL Processing", display_frame)
                    
                    # Check for exit key
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):  # ESC or 'q'
                        running = False
                except Exception as e:
                    print(f"Error in display: {e}")
            
            # Update last frame number
            last_frame_number = frame_data.get('frame_number', -1)
            
        except Exception as e:
            print(f"Error in main processing loop: {e}")
            error_count += 1
            if error_count >= max_errors:
                print(f"Too many errors ({error_count}). Restarting...")
                time.sleep(5)
                error_count = 0
            time.sleep(1)  # Wait a bit before retrying
    
    try:
        if debug_window_enabled:
            cv2.destroyAllWindows()
    except:
        pass
    
    print("Stream processing ended")

def main():
    """Main function to start the BSL interpreter."""
    print("BSL Bridge Integration Starting...")
    
    # Use the stream ID from command line or file
    stream_id = input_stream_id
    
    # Verify the stream exists and is active
    print(f"Checking if stream {stream_id} is active...")
    
    try:
        stream_ref = db.reference(f'/streams/{stream_id}')
        stream_data = stream_ref.get()
        
        if not stream_data:
            print(f"Stream {stream_id} not found!")
            available_streams = get_available_streams()
            if available_streams:
                print("\nAvailable active streams:")
                for i, (available_id, stream_data) in enumerate(available_streams.items(), 1):
                    print(f"{i}. {available_id}")
                # Let user select a stream
                selection = input("\nSelect a stream by number (or press Enter to exit): ")
                if selection.strip():
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(available_streams):
                            stream_id = list(available_streams.keys())[index]
                        else:
                            print("Invalid selection, exiting.")
                            return
                    except ValueError:
                        print("Invalid input, exiting.")
                        return
                else:
                    print("No selection made, exiting.")
                    return
            else:
                print("No active streams available. Please start a stream first.")
                return
    except Exception as e:
        print(f"Error checking stream: {e}")
        return
    
    print(f"Starting processing for stream: {stream_id}")
    
    # Start processing the selected stream
    start_stream_processing(stream_id)

if __name__ == "__main__":
    main()