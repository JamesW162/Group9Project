import os
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import pickle

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

def drawLandmarks(img_rgb, hand_landmarks):
    # Draw hand landmarks on the image
    mp_drawing.draw_landmarks(
        img_rgb,  # image to draw
        hand_landmarks,  # model output
        mp_hands.HAND_CONNECTIONS,  # hand connections
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image into RGB for Mediapipe
        
        # Process the image and find hands
        result = hands.process(img_rgb)
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # create an array for each image
                for i in range(len(hand_landmarks.landmark)):
                    # collect the x and y landmarks to create a long array to train our classifier
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)

            data.append(data_aux)  # the array will represent the image
            labels.append(dir_)  # the name of the directory of each one of these images

        # Uncomment if you want to visualize the images with landmarks drawn
        #drawLandmarks(img_rgb, hand_landmarks)
        #plt.figure()
        #plt.imshow(img_rgb)

#plt.show()

with open('data.pickle', 'wb') as f:  # pickle is a Python library used to save datasets
    pickle.dump({'data': data, 'labels': labels}, f)
