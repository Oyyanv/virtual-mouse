import cv2
import time
import mediapipe as mp
import pyautogui
import math

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0)

cam = cv2.VideoCapture(0)
cam.set(3, 1200) # width
cam.set(4, 900)  # height
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

#gesture time
click_start_time = None
click_time = []
click_cd = 0.5
scroll_mode = False
freeze_mode = False
screen_w, screen_h = pyautogui.size()
last_click_time = 0

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
            #kalo mau matiinn mp_drawingnya, non-aktifin aja line di 57 terus dibagian finger tipnya
            #tambahin tab atau indent supaya masuk ke loopnya
             mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) 
    
        #tanda di ujung setiap jari
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        # ring_tip = qhand_landmarks.landmark[16]
        # pinky_tip = hand_landmarks.landmark[20]
        finger = [
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y else 0
            for tip in [4, 8, 12]
        ]
    
        #distance index and thumb
        distance = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
        if distance < 0.06:
            if not freeze_mode:
                freeze_mode = True
                click_time.append(time.time())
                last_click_time = time.time()
            
            #2x click and 1x click
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

        #moving cursor with index finger
        if not freeze_mode:
            screen_x = int(index_tip.x * screen_w)
            screen_y = int(index_tip.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y, duration=0)
            previous_screen_x, previous_screen_y = screen_x, screen_y

    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    cv2.imshow('Live Cam', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()