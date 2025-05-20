from ultralytics import YOLO

class BallDetector:
    def __init__(self, model_path="yolov8m.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        return [r for r in results.boxes.data if int(r[-1]) == 32 and float(r[4]) > 0.05]