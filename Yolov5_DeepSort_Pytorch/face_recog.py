import face_recognition
import numpy as np
import os

# get face data of all employees
known_face_encodings = []
known_face_names = []
for file in os.listdir("./employees_faces"):
    if file.endswith(".npy"):
        with open(os.path.join('./employees_faces/',file), 'rb') as f:
            known_face_encodings.append(np.load(f)[0])
            known_face_names.append(os.path.splitext(file)[0])

def identify(frame, id):
    # return "No Face"
    rgb_frame = frame[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_frame)
    if(len(face_encodings) > 0):
        face_encoding = face_encodings[0]
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = (id + " - Unknown")
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        return (id + " - " + name)
    else:
        return "No Face"
