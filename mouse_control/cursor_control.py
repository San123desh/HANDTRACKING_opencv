import cv2
import numpy as np
import handTrack as htm
import pyautogui
import time

# Camera setup
wCam, hCam = 700, 500
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Screen size
screenW, screenH = pyautogui.size()

# Initialize hand detector
detector = htm.HandDetector(detectionCon=0.75)

# Smoothing factor
smooth_factor = 7
smoothening = 0.2
prevX, prevY = 0, 0
currX, currY = 0, 0

# Variables for click and drag
drag = False
click_time = 0

while True:
    # Read the camera feed
    success, img = cap.read()
    if not success:
        break

    # Find hand and landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        # Get the tip of the index finger and thumb
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[4][1], lmList[4][2]

        # Convert coordinates
        screenX = np.interp(x1, (0, wCam), (0, screenW))
        screenY = np.interp(y1, (0, hCam), (0, screenH))

        # Smoothen the values
        # currX = prevX + (screenX - prevX) / smoothening
        # currY = prevY + (screenY - prevY) / smoothening

        currX = prevX + smoothening * (screenX - prevX)
        currY = prevY + smoothening * (screenY - prevY)

        # Move the mouse
        pyautogui.moveTo(screenW - currX, currY)
        prevX, prevY = currX, currY

        # Calculate the distance between index finger and thumb
        distance = np.hypot(x2 - x1, y2 - y1)

        # Click action
        if distance < 40:
            if not drag:
                pyautogui.mouseDown()
                drag = True
        else:
            if drag:
                pyautogui.mouseUp()
                drag = False

    # Display the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
