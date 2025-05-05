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
            if len(result.multi_hand_landmarks) == 1:
                # If only one hand, get its landmarks and pad with zeros for the missing hand.
                hand = result.multi_hand_landmarks[0]
                for landmark in hand.landmark:
                    data_aux.extend([landmark.x, landmark.y])
                data_aux.extend([0.0] * 42)
            else:
                # Process only the first two detected hands.
                for hand in result.multi_hand_landmarks[:2]:
                    for landmark in hand.landmark:
                        data_aux.extend([landmark.x, landmark.y])
        
            data.append(data_aux)  # the array now represents the image (84 datapoints)
            labels.append(dir_)  # the directory name becomes the label

        # Uncomment to visualize images with drawn landmarks:
        # drawLandmarks(img_rgb, hand_landmarks)
        # plt.figure()
        # plt.imshow(img_rgb)

# Uncomment if you want to display all images
# plt.show()

with open('data.pickle', 'wb') as f:  # Save datasets using pickle
    pickle.dump({'data': data, 'labels': labels}, f)