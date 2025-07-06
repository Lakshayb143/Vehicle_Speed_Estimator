import cv2
import logging
import numpy as np
from ultralytics import YOLO



logger = logging.getLogger(__name__)


class ViewTransformer:
    def __init__(self, source, destination):
        self.homography_matrix, status = cv2.findHomography(source, destination)

    def transform_point(self, point):
        p = np.array([[[point[0], point[1]]]], dtype=np.float32)
        transformed_p = cv2.perspectiveTransform(p, self.homography_matrix)
        return transformed_p[0][0]

