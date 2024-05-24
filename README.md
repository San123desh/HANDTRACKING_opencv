# Hand Tracking with OpenCV and MediaPipe

This project demonstrates real-time hand tracking using OpenCV and MediaPipe. It captures video from your webcam, detects hands, and draws landmarks on them.


## Features:

- Real-time hand detection
- Hand landmarks visualization
- Optional finger counting functionality (can be implemented)

## Prerequisites:

- Python 3.6 or later
- OpenCV library
- MediaPipe library


## Installation

- pip install opencv-python

- pip install mediapipe

- pip install pycaw (control volume)
* https://github.com/AndreMiras/pycaw


## Usage
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)



## Clone the repository

git clone https://github.com/San123desh/HANDTRACKING_opencv.git


















