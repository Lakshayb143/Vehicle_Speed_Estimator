from ultralytics import YOLO




class VehicleTracker:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.vehicle_classes = [2, 3, 5, 7] 
    
    
    def get_detections(self, frame):
        results = self.model.track(frame, persist=True)
        detections = []
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)

            for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
                if cls_id in self.vehicle_classes:
                    detections.append({'box': box, 'track_id': track_id})
        return detections