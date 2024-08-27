import torch

def load_yolo_model():
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = 0.5  # Set confidence threshold
    model.classes = [0]  # Person class only
    return model

def detect_objects(model, frame):
    results = model(frame)
    detections = []
    for result in results.xywh[0].cpu().numpy():
        x_center, y_center, width, height, conf, cls = result
        x1, y1, x2, y2 = x_center - width / 2, y_center - height / 2, x_center + width / 2, y_center + height / 2
        detections.append(([x1, y1, x2, y2], conf, 'person'))
    return detections
