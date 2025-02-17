import cv2
import mediapipe as mp
import pickle
import numpy as np

model_dict = pickle.load(open('C:/Users/LMACE/OneDrive/Documents/UNIVERSITY/year_2/Group IOT/model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)  # Use 0 for default camera, or 2 if that's the correct index for your camera

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)
labels_dict = {0: 'A', 1: 'B', 2: 'L'}

def drawLandmarks(img_rgb, hand_landmarks):
    # Draw hand landmarks on the image
    mp_drawing.draw_landmarks(
        img_rgb,  # image to draw
        hand_landmarks,  # model output
        mp_hands.HAND_CONNECTIONS,  # hand connections
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    if not ret:
        break

    H, W, _ = frame.shape  # Use frame.shape without parentheses

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert image into RGB for Mediapipe
    result = hands.process(frame_rgb)
    
    predicted_character = ""  # Initialize the variable

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            drawLandmarks(frame, hand_landmarks)

        for hand_landmarks in result.multi_hand_landmarks:
            # create an array for each image
            for i in range(len(hand_landmarks.landmark)):
                # collect the x and y landmarks to create a long array to train our classifier
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
                x_.append(x)
                y_.append(y)
        
        x1 = int(min(x_) * W) -10
        y1 = int(min(y_) * H) -10
        x2 = int(max(x_) * W)- 10
        y2 = int(max(y_) * H)- 10 
    
        data_aux = np.array(data_aux).reshape(1, -1)  # Reshape data_aux before prediction
        prediction = model.predict(data_aux)
        predicted_character = labels_dict[int(prediction[0])]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
