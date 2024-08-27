import cv2
import numpy as np
import mediapipe as mp

def initialize_face_mesh():
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    return mp_face_mesh.FaceMesh()

def estimate_gaze(face_mesh, face_region):
    if face_region is None or face_region.size == 0:
        return None  # Return None if face_region is empty or not valid

    face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(face_region_rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(lm.x * face_region.shape[1], lm.y * face_region.shape[0]) for lm in face_landmarks.landmark]
            return landmarks
    return None

def draw_gaze(frame, landmarks, bbox):
    # Calculate gaze direction based on eye landmarks
    if landmarks is None:
        return

    # Example points for left and right eyes
    left_eye = np.array([landmarks[33], landmarks[133]])
    right_eye = np.array([landmarks[362], landmarks[263]])
    gaze_direction = np.mean(left_eye - right_eye, axis=0)

    # Draw an arrow showing gaze direction
    start_point = (int((bbox[0] + bbox[2]) / 2), int((bbox[1] + bbox[3]) / 2))
    end_point = (int(start_point[0] + gaze_direction[0] * 10), int(start_point[1] + gaze_direction[1] * 10))
    cv2.arrowedLine(frame, start_point, end_point, (0, 255, 0), 2)
