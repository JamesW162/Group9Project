import os
import cv2

# Get user input for folder name
folder_name = input("Enter the folder name for data collection: ")
DATA_DIR = os.path.join('./data', folder_name)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Number of images to collect
dataset_size = 100

cap = cv2.VideoCapture(0)  # Use 0 for the default camera
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

print(f'Collecting data in folder: {folder_name}')

# Displays Camera in frame with text prompting the user to start. Exits if camera not found or 'f' pressed.
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    cv2.putText(frame, 'Press F to start', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(25) == ord('f'):
        break

# Takes number of pictures specified by dataset_size. stores in data/{label}
for counter in range(dataset_size):
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    cv2.imshow('frame', frame)
    cv2.waitKey(25)
    cv2.imwrite(os.path.join(DATA_DIR, f'{counter}.jpg'), frame)

    print(f"Captured image {counter}/{dataset_size}")

print("Image collection complete.")
cap.release()
cv2.destroyAllWindows()
