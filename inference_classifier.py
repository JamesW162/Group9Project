import os
import cv2
import mediapipe as mp
import pickle
import numpy as np

# Build a universal path to the model file located in the same directory as this script.
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.p')
model_dict = pickle.load(open(model_path, 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)  # Use 0 for default camera, or adjust the index if needed.

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)
labels_dict = {0: 'A', 1: 'B', 2: 'C'}

def drawLandmarks(img, hand_landmarks):
    mp_drawing.draw_landmarks(
        img,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

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
        # Draw landmarks for up to 2 hands.
        for hand_landmarks in result.multi_hand_landmarks[:2]:
            drawLandmarks(frame, hand_landmarks)
        
        # Process landmarks: if one hand detected, pad with zeros.
        if len(result.multi_hand_landmarks) == 1:
            hand = result.multi_hand_landmarks[0]
            for landmark in hand.landmark:
                data_aux.extend([landmark.x, landmark.y])
                x_coords.append(landmark.x)
                y_coords.append(landmark.y)
            data_aux.extend([0.0] * 42)  # Pad for the missing hand.
        else:
            # Process the first 2 hands.
            for hand in result.multi_hand_landmarks[:2]:
                for landmark in hand.landmark:
                    data_aux.extend([landmark.x, landmark.y])
                    x_coords.append(landmark.x)
                    y_coords.append(landmark.y)

        # Calculate bounding box over all landmarks.
        x1 = int(min(x_coords) * W) - 10
        y1 = int(min(y_coords) * H) - 10
        x2 = int(max(x_coords) * W) + 10
        y2 = int(max(y_coords) * H) + 10 

        data_aux_np = np.array(data_aux).reshape(1, -1)  # Ensure array shape is [1,84]
        prediction = model.predict(data_aux_np)
        predicted_character = labels_dict[int(prediction[0])]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()