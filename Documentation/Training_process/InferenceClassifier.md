# Gesture-to-Text Inference Script - Code Explanation

This document explains the functionality of `inference_classifier.py`, which performs real-time hand gesture recognition to convert sign language gestures into text, with direct quotes from the code.

## Imports and Setup

```python
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
```

This code imports all necessary libraries:
- `os` for file path operations
- `cv2` (OpenCV) for camera access and image processing
- `mediapipe` for hand landmark detection
- `pickle` for loading the trained model
- `numpy` for numerical operations
- `Counter` for counting gesture occurrences
- `time` for timing operations between gestures
- `nltk` and its `words` corpus for word suggestions
- `difflib` for finding similar words
- `requests` for HTTP communication

## Setting Up the Word Dictionary

```python
# Download NLTK word corpus
nltk.download('words')
word_dict = set(word.upper() for word in words.words())
```

This code:
1. Downloads the NLTK words corpus if not already present
2. Creates a set of uppercase words to compare against the detected gestures

## Initializations

```python
# Initialise camera input into 'cap'. 
cap = cv2.VideoCapture(0)
gesture_list = []
current_input = ""
detected_words = []
previous_letter = None
last_time = time.time()
last_detected_time = time.time()
```

This code initializes:
- The webcam capture
- A list to store recent gestures
- A string to build the current word
- A list to store completed words
- A variable to track the previously detected letter
- Time variables to manage gesture detection timing

## Setting Up MediaPipe

```python
# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Specifies two hands and detection confidence 
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.3)
```

This code sets up MediaPipe's hand tracking:
1. Imports the necessary MediaPipe components
2. Configures the hand detector to track up to two hands with a confidence threshold of 0.3

## Helper Functions

### Drawing Hand Landmarks

```python
def drawLandmarks(img, hand_landmarks):
    mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )
```

This function draws the hand landmarks and connections on the image for visualization.

### Identifying Consistent Gestures

```python
def get_most_frequent_gesture(gesture_list, threshold=0.9):
    counts = Counter(gesture_list)
    total_gestures = len(gesture_list)
    for gesture, count in counts.items():
        if count / total_gestures >= threshold:
            return gesture
    return None
```

This function:
1. Counts occurrences of each gesture in the recent gesture list
2. Returns a gesture if it appears in at least 90% of recent frames
3. Returns `None` if no gesture is consistent enough

### Finding Word Suggestions

```python
def get_word_suggestions(fragment, dictionary, num=3):
    return difflib.get_close_matches(fragment, dictionary, n=num, cutoff=0.6)
```

This function finds up to three words in the dictionary that closely match the current input fragment.

## Loading the Model

```python
# Universal path to the model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']
```

This code loads the previously trained Random Forest Classifier model that will recognize hand gestures.

## Main Processing Loop

The main loop captures frames from the webcam and processes them to detect hand gestures:

```python
while True:
    data_aux = []
    x_coords = []
    y_coords = []

    ret, frame = cap.read()
    if not ret:
        break

    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)
```

This section:
1. Initializes lists for the current frame's data
2. Captures a frame from the webcam
3. Gets the frame dimensions
4. Converts the frame to RGB for MediaPipe
5. Processes the frame to detect hands

## Hand Landmark Extraction

```python
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
            data_aux.extend([0.0] * 42)
        else:
            for hand in result.multi_hand_landmarks[:2]:
                for landmark in hand.landmark:
                    data_aux.extend([landmark.x, landmark.y])
                    x_coords.append(landmark.x)
                    y_coords.append(landmark.y)
```

This code:
1. Draws the detected hand landmarks on the frame
2. Extracts the landmark coordinates
3. If only one hand is detected, it extracts its landmarks and pads with zeros
4. If two hands are detected, it extracts landmarks from both hands

## Gesture Prediction

```python
        x1 = int(min(x_coords) * W) - 10
        y1 = int(min(y_coords) * H) - 10
        x2 = int(max(x_coords) * W) + 10
        y2 = int(max(y_coords) * H) + 10

        data_aux_np = np.array(data_aux).reshape(1, -1)
        prediction = model.predict(data_aux_np)
        predicted_character = prediction[0].upper()

        gesture_list.append(predicted_character)
        if len(gesture_list) == 10:
            most_frequent_gesture = get_most_frequent_gesture(gesture_list)
            if most_frequent_gesture:
                current_time = time.time()
                if most_frequent_gesture != previous_letter or (current_time - last_time) > 1:
                    current_input += most_frequent_gesture.upper()
                    print("Current Input Buffer:", current_input)
                    previous_letter = most_frequent_gesture
                    last_time = current_time
                    last_detected_time = current_time
            gesture_list.pop(0)
```

This code:
1. Calculates a bounding box around the hand(s)
2. Reshapes the landmark data for model input
3. Uses the model to predict the gesture
4. Adds the prediction to a sliding window of recent gestures
5. If the gesture list is full (10 frames):
   - Checks if there's a consistent gesture
   - Only adds the letter if it's different from the previous one or more than 1 second has passed
   - Updates the current input string with the detected letter
   - Removes the oldest gesture from the list

## Word Completion and Saving

```python
    suggestions = get_word_suggestions(current_input, word_dict)

    if time.time() - last_detected_time > 4 and current_input:
        finalized_word = suggestions[0] if suggestions else current_input
        detected_words.append(finalized_word)
        print("Finalized Word:", finalized_word)
        current_input = ""
        last_detected_time = time.time()

        # Write locally
        final_sentence = " ".join(detected_words)
        with open("website/output.txt", "w") as file:
            file.write(final_sentence)

        # Upload securely via HTTP POST
        url = "http://localhost:8000/website/upload_output.php"
        try:
            response = requests.post(url, data={"output": final_sentence})
            if response.status_code == 200:
                print("Uploaded successfully via HTTP:", response.text)
            else:
                print("Upload failed with status code:", response.status_code)
        except Exception as e:
            print("Upload failed:", e)
```

This code:
1. Gets word suggestions based on the current input
2. If no new gesture has been detected for 4 seconds and there's current input:
   - Finalizes the word (uses the top suggestion if available)
   - Adds the word to the detected words list
   - Resets the current input buffer
   - Creates a sentence from all detected words
   - Saves the sentence to a local file
   - Uploads the sentence to a local web server via HTTP POST

## Display and Exit

```python
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('e'):
        url = "http://localhost:8000/website/logout.php"
        with open("website/output.txt", "w") as file:
            file.write("")
        break

cap.release()
cv2.destroyAllWindows()
```

This final section:
1. Displays the processed frame with hand landmarks
2. Checks if the user pressed 'e' to exit
3. Clears the output file and performs logout on exit
4. Releases the camera and closes all windows when done
