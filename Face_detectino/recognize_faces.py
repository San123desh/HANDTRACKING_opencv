import cv2
import face_recognition
import numpy as np
import pandas as pd
from datetime import datetime
import os

# Load known face encodings and names
known_face_encodings = np.load('known_face_encodings.npy', allow_pickle=True)
known_face_names = np.load('known_face_names.npy', allow_pickle=True)

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Create or load the attendance log
attendance_file = 'attendance.csv'
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=['Name', 'Time'])
    df.to_csv(attendance_file, index=False)
else:
    df = pd.read_csv(attendance_file)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame of video
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Process every other frame for efficiency
    if process_this_frame:
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the closest known face if a match was found
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # Log attendance if recognized
            if name != "Unknown":
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                if not ((df['Name'] == name) & (df['Time'].str[:10] == current_time[:10])).any():
                    new_entry = {'Name': name, 'Time': current_time}
                    df = df.append(new_entry, ignore_index=True)
                    df.to_csv(attendance_file, index=False)

    process_this_frame = not process_this_frame

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw bounding box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw label with name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
video_capture.release()
cv2.destroyAllWindows()
