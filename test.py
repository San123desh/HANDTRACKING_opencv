import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm  # Assuming you have a separate module for hand tracking
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Set camera width and height
wCam, hCam = 640, 480

# Initialize Pycaw for audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get the volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Variables for volume control
vol = 0
volBar = 400
volPer = 0
setVolume = False

# Initialize hand detector
detector = htm.HandDetector(detectionCon=0.75)

# Create a Tkinter window
root = tk.Tk()
root.title("Hand Gesture Volume Control")

# Create a frame for video
video_frame = ttk.Label(root)
video_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a volume slider
volume_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', length=300)
volume_slider.set(50)
volume_slider.grid(row=1, column=0, padx=10, pady=10)

# Create a button to start setting volume
set_volume_button = ttk.Button(root, text="Set Volume", command=lambda: toggle_set_volume())
set_volume_button.grid(row=2, column=0, padx=10, pady=10)

def toggle_set_volume():
    global setVolume
    setVolume = not setVolume
    set_volume_button.config(text="Stop Setting Volume" if setVolume else "Set Volume")

# Function to update the video feed
def update_video():
    global vol, volBar, volPer

    success, img = cap.read()
    if not success:
        root.quit()
        return

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        # Get positions of thumb tip and index finger tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw landmarks and line
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculate the length between thumb and index finger
        length = math.hypot(x2 - x1, y2 - y1)

        # Adjust the range for easier volume control
        minDistance = 30  # Minimum distance between thumb and index finger
        maxDistance = 200

        # Map the length to volume range
        vol = np.interp(length, [minDistance, maxDistance], [minVol, maxVol])
        volBar = np.interp(length, [minDistance, maxDistance], [400, 150])
        volPer = np.interp(length, [minDistance, maxDistance], [0, 100])

        # Set the volume
        if setVolume:
            volume.SetMasterVolumeLevel(vol, None)

        # Change color if volume is at minimum level
        if length < minDistance:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Draw volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Convert the image to RGB and display it in the Tkinter window
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgPIL = Image.fromarray(imgRGB)
    imgTK = ImageTk.PhotoImage(image=imgPIL)
    video_frame.imgTK = imgTK  # Keep a reference to avoid garbage collection
    video_frame.config(image=imgTK)

    # Schedule the next update
    root.after(10, update_video)

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Start the video update loop
update_video()

# Run the Tkinter event loop
root.mainloop()

# Release resources
cap.release()
cv2.destroyAllWindows()
