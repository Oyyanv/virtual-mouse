Requirement :
- Python 3.12
- venv gesture 
py -m venv gesture.env
- install Libraries (requirement.txt)
    - opencv-python
    - pyautogui
    - numpy
    - mediapipe
py -m pip install -r requirement.txt or pip install -r requirement.txt
______________________________________________________________________
Gesture :
- Index Finger = Controlling Cursor

- Thumb + Index Finger = Left Click

- Thumb + Middle Finger = Right Click

- Index + Middle Finger = Scrolling

Note : 
- If FPS drops, Comment out the line mp_drawing.draw_landmarks() in the code.
- Adjust camera resolution for performance and more accurate detection.
- Press Q button to exit the program.