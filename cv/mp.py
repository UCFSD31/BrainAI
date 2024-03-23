import cv2
import mediapipe as mp
import numpy as np
import math
import os

# Enable specific CPU instructions
os.environ['TF_ENABLE_SSE'] = '1'   # SSE4.1 and SSE4.2
os.environ['TF_ENABLE_AVX'] = '1'   # AVX
os.environ['TF_ENABLE_AVX2'] = '1'  # AVX2
os.environ['TF_ENABLE_FMA'] = '1'   # FMA

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define a custom function to draw only specific landmarks
def draw_specific_landmarks(image, landmarks, indices):
    for idx in indices:
        if idx < len(landmarks):
            landmark_px = mp_draw._normalized_to_pixel_coordinates(landmarks[idx].x, landmarks[idx].y, image.shape[1], image.shape[0])
            if landmark_px:  # Check if conversion is successful
                cv2.circle(image, landmark_px, 5, (0, 255, 0), -1)

def calculate_angle(x1, y1, x2, y2):
    # Handling division by zero for vertical lines
    if x2 - x1 == 0:
        return 90 if y2 > y1 else -90
    angle = math.degrees(math.atan((y2 - y1) / (x2 - x1)))
    return angle

def calculate_angle_not_right(x1, y1, x2, y2, x3, y3):
    c = math.hypot(x3 - x1, y3 - y1)
    b = math.hypot(x3 - x2, y3 - y2)
    a = math.hypot(x2 - x1, y2 - y1)
    
    cosc = (pow(a, 2) + pow(b, 2) - pow(c, 2)) / (2 * a * b)
    cosc = max(min(cosc, 1), -1)
    angleC = math.degrees(math.acos(cosc))
    
    return angleC
    

# For webcam input, initialize the camera.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the frame with MediaPipe Hands.
    hand_results = hands.process(image_rgb)

    if hand_results.multi_hand_landmarks:
        for hand_landmark in hand_results.multi_hand_landmarks:
            # Indices for the middle finger: MCP (9), PIP (10), DIP (11), TIP (12)
            middle_finger_indices = [9, 10, 11, 12]
            thumb_indices = [2, 3, 4, 0]
            index_finger_indices = [5, 6, 7, 8, 20]
            draw_specific_landmarks(image, hand_landmark.landmark, thumb_indices)
            draw_specific_landmarks(image, hand_landmark.landmark, middle_finger_indices)
            draw_specific_landmarks(image, hand_landmark.landmark, index_finger_indices)
            
            # Calculate the angle between MCP and PIP
            mcp = hand_landmark.landmark[9]
            pip = hand_landmark.landmark[10]
            thumb_tip = hand_landmark.landmark[4]
            thumb_knuckle = hand_landmark.landmark[2]
            wrist = hand_landmark.landmark[0]
            index_tip = hand_landmark.landmark[8]
            index_knuckle = hand_landmark.landmark[6]
            pinky_knuckle = hand_landmark.landmark[20]

            width, height, _ = image.shape
            mcp_position = (int(mcp.x * width), int(mcp.y * height))
            pip_position = (int(pip.x * width), int(pip.y * height))
            thumb_knuckle_position = (int(thumb_knuckle.x * width), int(thumb_knuckle.y * height))
            thumb_tip_position = (int(thumb_tip.x * width), int(thumb_tip.y * height))
            wrist_position = (int(wrist.x * width), int(wrist.y * height))
            index_tip_pos = (int(index_tip.x * width), int(index_tip.y * height))
            index_knuckle_pos = (int(index_knuckle.x * width), int(index_knuckle.y * height))
            pinky_knuckle_pos = (int(pinky_knuckle.x * width), int(pinky_knuckle.y * height))

            angle_m = calculate_angle(mcp_position[0], mcp_position[1], pip_position[0], pip_position[1])
            angle_thumb = calculate_angle_not_right(wrist_position[0], wrist_position[1], thumb_knuckle_position[0], 
                                                    thumb_knuckle_position[1], thumb_tip_position[0], thumb_tip_position[1])
            angle_index = calculate_angle_not_right(pinky_knuckle_pos[0], pinky_knuckle_pos[1], mcp_position[0], mcp_position[1],
                                                    index_tip_pos[0], index_tip_pos[1])
            

            if(angle_m < 0 and mcp_position[0] - pip_position[0] > 0):
                angle_m = 0
            if(angle_m < 0 and mcp_position[0] - pip_position[0] < 0):
                angle_m += 180
            elif(angle_m >= 0 and mcp_position[0] - pip_position[0] <= 0):
                angle_m = 180
            if(angle_m == -90):
                angle_m = 90
            if(angle_m == -0):
                angle_m = 0
            
            angle_thumb = min(180, max(0, ((angle_thumb - 130) * 4.6)))
            angle_index = min(180, max(0, ((angle_index - 30) * 4.7)))
            

            text_position = (10, 40)
            line_height = 40
            cv2.putText(image, f"Angle Middle: {angle_m:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            text_position = (text_position[0], text_position[1] + line_height)
            cv2.putText(image, f"Angle Wrist: {angle_thumb:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            text_position = (text_position[0], text_position[1] + line_height)
            cv2.putText(image, f"Angle Index: {angle_index:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)



    # Display the image.
    cv2.imshow('MediaPipe Hands', image)

    # Check if 'q' is hit to break the loop and exit.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
