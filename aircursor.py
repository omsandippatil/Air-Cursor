import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Screen resolution (you may need to adjust this based on your screen resolution)
screen_width, screen_height = pyautogui.size()

# Initialize variables for tracking hand state
last_gesture_time = time.time()
last_click_time = time.time()
dragging = False

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

        # Get coordinates of thumb tip
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_x = int(thumb_tip.x * screen_width)
        thumb_y = int(thumb_tip.y * screen_height)

        # Move cursor to index finger tip position
        pyautogui.moveTo(index_finger_x, index_finger_y, duration=0.1)

        # Check for gesture actions
        if time.time() - last_gesture_time > 1:
            # Right click if thumb is close to index finger
            if abs(index_finger_x - thumb_x) < 20 and abs(index_finger_y - thumb_y) < 20:
                pyautogui.rightClick()
                last_gesture_time = time.time()

            # Double click if finger is steady
            elif time.time() - last_click_time > 0.3:
                pyautogui.click(clicks=2)
                last_click_time = time.time()
                last_gesture_time = time.time()

            # Click if finger is steady
            elif abs(index_finger_x - thumb_x) > 20 or abs(index_finger_y - thumb_y) > 20:
                pyautogui.click()
                last_click_time = time.time()
                last_gesture_time = time.time()

            # Drag and drop if finger is dragging
            if dragging:
                pyautogui.dragTo(index_finger_x, index_finger_y, duration=0.2)

    # Display frame with hand landmarks
    cv2.imshow('Hand Tracking', frame)q

    # Exit on 'Esc' key
    if cv2.waitKey(30) & 0xff == 27:  
            break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
