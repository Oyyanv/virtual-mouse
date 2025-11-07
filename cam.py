import cv2
import time
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)


cam = cv2.VideoCapture(0)

#gesture time
click_start_time = None
click_time = []
click_cd = 0.5
scroll_mode = False
freeze_mode = False


screen_w, screen_h = pyautogui.size()
print('/n Hand Finger Virtual Mouse /n')
previous_screen_x, previous_screen_y = 0, 0

if not cam.isOpened():
    print("Cannot open camera")
    exit()

previous_time = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
             mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #finger tip
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
    
        finger = [
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0
            for tip in [4, 8, 12, 16, 20]
        ]
    
        #distance index and thumb
        distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
        if distance < 0.04:
            if not freeze_mode:
                freeze_mode = True
                click_time.append(time.time())
            
            #2x click
            if len(click_time) >= 2 and click_time[-1] - click_time[-2]<0.4:
                pyautogui.doubleClick()
                cv2.putText(frame, 'Double Click', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                click_time = []
            else:
                pyautogui.click()
                cv2.putText(frame, 'Click', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            freeze_mode = False
                

    cv2.imshow('Live Cam', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
