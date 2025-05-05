# Hand Gesture Dataset Creator Documentation

## Overview

`create_dataset.py` is a Python script that processes images of hand gestures to create a machine learning dataset. It uses the MediaPipe library to detect hand landmarks in images and converts these landmarks into feature vectors that can be used for training machine learning models for hand gesture recognition.

## Dependencies

- OpenCV (`cv2`): For image loading and processing
- MediaPipe (`mediapipe`): For hand landmark detection 
- Matplotlib (`pyplot`): For visualization (optional)
- Pickle: For saving the processed dataset

## Directory Structure

The script expects the following directory structure:
```
./
├── create_dataset.py
└── data/
    ├── gesture1/
    │   ├── img1.jpg
    │   ├── img2.jpg
    │   └── ...
    ├── gesture2/
    │   ├── img1.jpg
    │   └── ...
    └── ...
```

Each subdirectory in the `data` directory represents a class/label (gesture type), and contains images of that particular hand gesture.

## Functionality

### Hand Landmark Detection

The script uses MediaPipe's Hands solution to detect hand landmarks in images. Each hand is represented by 21 landmarks, with each landmark having x and y coordinates. The script can process up to two hands in each image.

### Data Processing

For each image:
1. The image is loaded and converted from BGR to RGB color space
2. Hand landmarks are detected using MediaPipe
3. The x, y coordinates of each landmark are extracted and stored in a flat array
4. If only one hand is detected, zeros are padded for the second hand to maintain consistent feature vector length
5. The resulting feature vector and corresponding label are added to the dataset

### Dataset Creation

The script creates two lists:
- `data`: Contains feature vectors (84 values per image - 2 coordinates × 21 landmarks × up to 2 hands)
- `labels`: Contains the corresponding class labels (derived from directory names)

### Output

The processed dataset is saved as a pickle file named `data.pickle`, which contains a dictionary with keys:
- `'data'`: The feature vectors
- `'labels'`: The corresponding labels

## Usage

1. Organize hand gesture images in subdirectories under `./data/`
2. Run the script:
   ```
   python create_dataset.py
   ```
3. The resulting dataset will be saved as `data.pickle`

## Visualization (Optional)

The script includes a `drawLandmarks` function and commented code for visualizing the detected hand landmarks. To enable visualization:
1. Uncomment the visualization code sections
2. Run the script

## Configuration Options

The script uses MediaPipe Hands with the following configuration:
- `static_image_mode=True`: Optimized for processing individual images
- `max_num_hands=2`: Detects up to 2 hands in each image
- `min_detection_confidence=0.3`: Confidence threshold for hand detection

## Notes

- If an image contains more than two hands, only the first two detected hands will be processed
- Each feature vector contains 84 values (21 landmarks × 2 coordinates × 2 hands)
- For images with one hand, zeros are used to pad the feature vector to maintain consistent dimensions
