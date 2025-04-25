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

# Download NLTK word corpus
nltk.download('words')
word_dict = set(word.upper() for word in words.words())

cap = cv2.VideoCapture(0)
gesture_list = []
current_input = ""
detected_words = []
previous_letter = None
last_time = time.time()
last_detected_time = time.time()

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

labels = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
labels_dict = {label : label.upper() for label in labels}
# This is at least slightly better than doing it manually. Why do we actually need this?

def drawLandmarks(img, hand_landmarks):
    mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

def get_most_frequent_gesture(gesture_list, threshold=0.9):
    counts = Counter(gesture_list)
    total_gestures = len(gesture_list)
    for gesture, count in counts.items():
        if count / total_gestures >= threshold:
            return gesture
    return None

def get_word_suggestions(fragment, dictionary, num=3):
    return difflib.get_close_matches(fragment, dictionary, n=num, cutoff=0.6)

# Universal path to the model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

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

        x1 = int(min(x_coords) * W) - 10
        y1 = int(min(y_coords) * H) - 10
        x2 = int(max(x_coords) * W) + 10
        y2 = int(max(y_coords) * H) + 10

        data_aux_np = np.array(data_aux).reshape(1, -1)
        prediction = model.predict(data_aux_np)
        predicted_character = labels_dict.get(prediction[0], "Unknown")

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

    suggestions = get_word_suggestions(current_input, word_dict)

    if time.time() - last_detected_time > 4 and current_input:
        finalized_word = suggestions[0] if suggestions else current_input
        detected_words.append(finalized_word)
        print("Finalized Word:", finalized_word)
        current_input = ""
        last_detected_time = time.time()

        # Write locally
        final_sentence = " ".join(detected_words)
        with open("output.txt", "w") as file:
            file.write(final_sentence)

        # Upload securely via HTTP POST
        url = "http://localhost:8000/upload_output.php"
        try:
            response = requests.post(url, data={"output": final_sentence})
            if response.status_code == 200:
                print("Uploaded successfully via HTTP:", response.text)
            else:
                print("Upload failed with status code:", response.status_code)
        except Exception as e:
            print("Upload failed:", e)

    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
