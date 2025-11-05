import cv2
import time

cam = cv2.VideoCapture(0)

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
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Live Cam', frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
