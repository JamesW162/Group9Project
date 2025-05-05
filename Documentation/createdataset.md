# Hand Gesture Dataset Creator - Code Explanation

This document explains the functionality of `create_dataset.py`, which processes hand gesture images to create a machine learning dataset, with direct quotes from the code.

## Setup and Initialization

The script begins by importing the necessary libraries:

```python
import os
import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import pickle
```

Then it initializes the MediaPipe Hands solution:

```python
# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)
```

This configuration:
- Uses `static_image_mode=True` because we're processing individual images, not video
- Sets `max_num_hands=2` to detect up to two hands per image
- Uses a relatively low `min_detection_confidence=0.3` to increase detection rate

## Data Storage Setup

The script sets up data structures to store the processed information:

```python
DATA_DIR = './data'

data = []
labels = []
```

- `DATA_DIR` points to the directory containing the gesture image classes
- `data` will store the feature vectors extracted from each image
- `labels` will store the corresponding class labels

## Landmark Visualization Function

A helper function is defined to visualize the detected hand landmarks:

```python
def drawLandmarks(img_rgb, hand_landmarks):
    # Draw hand landmarks on the image
    mp_drawing.draw_landmarks(
        img_rgb,  # image to draw
        hand_landmarks,  # model output
        mp_hands.HAND_CONNECTIONS,  # hand connections
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )
```

This function uses MediaPipe's drawing utilities to render the hand landmarks and connections on the image.

## Processing Image Data

The main processing loop iterates through the data directory structure:

```python
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image into RGB for Mediapipe
        
        # Process the image and find hands
        result = hands.process(img_rgb)
```

For each image, the script:
1. Creates a temporary list `data_aux` to store the current image's feature vector
2. Loads the image using OpenCV
3. Converts it from BGR to RGB color space (required by MediaPipe)
4. Processes the image with MediaPipe's Hands solution

## Extracting Hand Landmarks

The script then extracts and processes the detected hand landmarks:

```python
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
```

This section:
1. Checks if any hands were detected
2. If exactly one hand was detected:
   - Extracts the x, y coordinates of each landmark (21 landmarks × 2 coordinates = 42 values)
   - Adds 42 zeros to pad for the missing second hand
3. If two or more hands were detected:
   - Processes the first two hands (21 landmarks × 2 coordinates × 2 hands = 84 values)
4. Adds the complete feature vector to the `data` list
5. Adds the corresponding label (directory name) to the `labels` list

## Visualization (Commented Out)

The script includes commented code for visualization:

```python
# Uncomment to visualize images with drawn landmarks:
# drawLandmarks(img_rgb, hand_landmarks)
# plt.figure()
# plt.imshow(img_rgb)

# Uncomment if you want to display all images
# plt.show()
```

When uncommented, this code would:
1. Draw the detected landmarks on each image
2. Display the images with landmarks using matplotlib

## Saving the Dataset

Finally, the script saves the processed dataset using pickle:

```python
with open('data.pickle', 'wb') as f:  # Save datasets using pickle
    pickle.dump({'data': data, 'labels': labels}, f)
```

The dataset is saved as a pickle file named `data.pickle`, containing a dictionary with:
- `'data'`: List of feature vectors (84 values per image)
- `'labels'`: List of corresponding class labels

This format makes it easy to load the dataset for training machine learning models for hand gesture recognition.
