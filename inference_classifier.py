import os
import cv2
import mediapipe as mp
import pickle
import numpy as np
from collections import Counter
import time
from flask import Flask, jsonify, render_template
import threading

# Flask app setup
app = Flask(__name__)
output_word = []  # Stores letters to construct words

@app.route('/get_output_word', methods=['GET'])
def get_output_word():
    return jsonify({'word': "".join(output_word)})

@app.route('/')
def index():
    return render_template('index.html')  # Serve the webpage

# Run Flask in a separate thread
def run_flask():
    app.run(debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Universal path to the model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)
gesture_list = []
previous_letter = None
last_time = time.time()

# Mediapipe initialization
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

labels_dict = {
    'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I',
    'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T',
    'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z'
}

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
                    output_word.append(most_frequent_gesture)
                    previous_letter = most_frequent_gesture
                    last_time = current_time

            gesture_list.pop(0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()

print("\nConstructed Word:", "".join(output_word))
