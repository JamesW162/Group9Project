import cv2
import mediapipe as mp

# Initialize MediaPipe Hands and FaceMesh
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
hands = mp_hands.Hands()
face_mesh = mp_face_mesh.FaceMesh()
mp_draw = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define eye and mouth landmark indices
eye_indices = [33, 133, 362, 263]   # One point for each eye
mouth_indices = [13, 14, 308, 78]  # Four points for the mouth

while cap.isOpened():
    # Exit program if camera data not found
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and detect hands and face
    hand_results = hands.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    # Draw hand landmarks on the frame
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Draw eye and mouth landmarks on the frame
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            landmark_points = []
            for idx, landmark in enumerate(face_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                # Draw one point for each eye
                if idx in eye_indices:
                    cv2.circle(frame, (cx, cy), 2, (255, 0, 0), cv2.FILLED)  # Blue for eyes
                # Draw four points for the mouth
                elif idx in mouth_indices:
                    cv2.circle(frame, (cx, cy), 2, (0, 255, 0), cv2.FILLED)  # Green for mouth
                    landmark_points.append((cx, cy))
            
            # Connect the mouth points
            for i in range(len(landmark_points)):
                for j in range(i + 1, len(landmark_points)):
                    cv2.line(frame, landmark_points[i], landmark_points[j], (0, 255, 0), 1)
    
    # Display the frame
    cv2.imshow('Hand, Eye, and Mouth Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
