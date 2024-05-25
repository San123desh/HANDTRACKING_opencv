import face_recognition
import os
import numpy as np

# Directory containing images of known individuals
known_faces_dir = 'known_faces'
known_face_encodings = []
known_face_names = []

# Loop through each person in the known_faces directory
for name in os.listdir(known_faces_dir):
    person_dir = os.path.join(known_faces_dir, name)
    for filename in os.listdir(person_dir):
        image_path = os.path.join(person_dir, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            encoding = encodings[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

# Save the encodings
np.save('known_face_encodings.npy', known_face_encodings)
np.save('known_face_names.npy', known_face_names)
