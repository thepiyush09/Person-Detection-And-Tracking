import cv2
from detection import load_yolo_model, detect_objects
from tracking import initialize_tracker, track_objects
from gaze_estimation import initialize_face_mesh, estimate_gaze, draw_gaze

def process_video(input_video_path, output_video_path):
    # Load models
    yolo_model = load_yolo_model()
    tracker = initialize_tracker()
    face_mesh = initialize_face_mesh()

    cap = cv2.VideoCapture(input_video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run object detection
        detections = detect_objects(yolo_model, frame)

        # Update tracker
        tracked_objects = track_objects(tracker, detections, frame)

        # Draw bounding boxes, IDs, and gaze estimation
        for track in tracked_objects:
            if track.is_confirmed():
                bbox = track.to_tlbr()
                track_id = track.track_id
                cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
                cv2.putText(frame, f'ID: {track_id}', (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # Gaze estimation
                face_region = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
                face_landmarks = estimate_gaze(face_mesh, face_region)
                if face_landmarks:
                    draw_gaze(frame, face_landmarks, bbox)

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video('input_video.mp4', 'output_video.mp4')
