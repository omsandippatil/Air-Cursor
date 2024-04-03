import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Screen resolution (you may need to adjust this based on your screen resolution)
screen_width, screen_height = pyautogui.size()

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Flip frame horizontally for intuitive movement (mirror effect)
    rgb_frame = cv2.flip(rgb_frame, 1)

    # Detect hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # Get hand landmarks
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get coordinates of index finger tip (assuming right hand)
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_finger_x = int(index_finger_tip.x * screen_width)
        index_finger_y = int(index_finger_tip.y * screen_height)

        # Move cursor to index finger tip position
        pyautogui.moveTo(index_finger_x, index_finger_y, duration=0.1)

    # Display frame with hand landmarks
    cv2.imshow('Hand Tracking', frame)

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
