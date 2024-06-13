# Face Detection Attendance System

This project implements a face detection-based attendance system using OpenCV and `face_recognition`. The system captures video from a webcam, recognizes faces of known individuals, and logs their attendance with timestamps into a CSV file.

## Table of Contents

- [Requirements](#requirements)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Requirements

- Python 3.7+
- OpenCV
- face_recognition
- pandas
- numpy

## Installation

- pip install cmake

- If this error came{
ERROR: Failed building wheel for dlib
Failed to build dlib
ERROR: Could not build wheels for dlib, which is required to install pyproject.toml-based projects
}



- pip install dlib-19.22.99-cp39-cp39-win_amd64.whl


### Run the encoding script to generate face encodings:

~ python encode_faces.py

### Run the face recognition script:
~ python recognize_faces.py


##### The attendance will be logged in attendance.csv with columns Name and Time.