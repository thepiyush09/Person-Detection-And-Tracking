def convert_bbox_format(bbox):
    x_center, y_center, width, height = bbox
    x1, y1, x2, y2 = x_center - width / 2, y_center - height / 2, x_center + width / 2, y_center + height / 2
    return [x1, y1, x2, y2]

def save_video_frame(frame, output_path):
    # Function to save video frame, if required
    pass
