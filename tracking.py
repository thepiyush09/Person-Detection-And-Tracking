from deep_sort_realtime.deepsort_tracker import DeepSort

def initialize_tracker():
    # Initialize DeepSORT
    tracker = DeepSort(max_age=30, nms_max_overlap=1.0, max_cosine_distance=0.4)
    return tracker

def track_objects(tracker, detections, frame):
    # Update the tracker with detected objects
    tracked_objects = tracker.update_tracks(detections, frame=frame)
    return tracked_objects
