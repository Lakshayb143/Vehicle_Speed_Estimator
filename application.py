import logging


from utils.logging_util import initialize_logging
from utils.points_utils import get_points


"""Intializing logging """
initialize_logging()
logger = logging.getLogger(__name__)


import cv2
import numpy as np
import collections
from ultralytics import YOLO


from src.config import settings
from src.steps.ViewTransformer import ViewTransformer
from src.steps.VehicleTracker import VehicleTracker




VIDEO_PATH = str(settings.SOURCE_VIDEO)
OUTPUT_PATH = str(settings.OUTPUT_PATH)

# SOURCE_POINTS = np.float32([[500,207], [694,193], [928,309], [527,339]])
SOURCE_POINTS = np.float32([[546,330], [654,318], [732,441], [592,460]])


DESTINATION_POINTS = np.float32([
    [0, 0],
    [settings.REAL_WORLD_WIDTH_M, 0],
    [settings.REAL_WORLD_WIDTH_M, settings.REAL_WORLD_HEIGHT_M],
    [0, settings.REAL_WORLD_HEIGHT_M]
])


def main():


    logger.info(f"\n\n\n\n")
    logger.info("-------------------------Starting application------------------------------------")


    transformer = ViewTransformer(SOURCE_POINTS, DESTINATION_POINTS)
    tracker = VehicleTracker()
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)

    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, settings.VIDEO_FPS, (int(cap.get(3)), int(cap.get(4))))

    vehicle_history = collections.defaultdict(list)
    vehicle_speeds = collections.defaultdict(lambda: collections.deque(maxlen=5)) 

    frame_index = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            detections = tracker.get_detections(frame)
            
            for det in detections:
                box = det['box']
                track_id = det['track_id']
                
                pos_pixel = ((box[0] + box[2]) / 2, box[3])
                pos_meters = transformer.transform_point(pos_pixel)
                
                vehicle_history[track_id].append((pos_meters, frame_index))
                
                if len(vehicle_history[track_id]) >= 2:
                    history_point_index = max(0, len(vehicle_history[track_id]) - 5)
                    last_pos, last_frame = vehicle_history[track_id][-1]
                    prev_pos, prev_frame = vehicle_history[track_id][history_point_index]

                    distance_meters = np.linalg.norm(last_pos - prev_pos)
                    time_seconds = (last_frame - prev_frame) / settings.VIDEO_FPS
                    
                    if time_seconds > 0:
                        speed_ms = distance_meters / time_seconds
                        speed_kmh = speed_ms * settings.KMH_CONVERSION_FACTOR
                        vehicle_speeds[track_id].append(speed_kmh)
                
                avg_speed = np.mean(vehicle_speeds[track_id]) if vehicle_speeds[track_id] else 0
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id}: {avg_speed:.1f} km/h", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                out.write(frame)
            cv2.imshow("Speed_Estimator", frame) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_index += 1

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        logger.info(f"Processing complete. Output video saved to {OUTPUT_PATH}")
        logger.info("-------------------------Application completed------------------------------------")
        logger.info(f"\n\n\n\n")

if __name__ == "__main__":
    main()