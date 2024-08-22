from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from obj_detection import DetectedObject

MODELS = Path(__file__).parent / 'models'


class CarDetector:
    def __init__(self, fast=False) -> None:
        model = MODELS / 'efficientdet_lite2.tflite'
        if fast:
            model = MODELS / 'efficientdet.tflite'
        base_options = python.BaseOptions(model_asset_path=model)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            score_threshold=0.5
        )
        self.detector = vision.ObjectDetector.create_from_options(options)

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.detector.detect(mp_image)
        cars = [
            DetectedObject(
                detection.bounding_box.origin_x,
                detection.bounding_box.origin_y,
                detection.bounding_box.width,
                detection.bounding_box.height
            )
            for detection in detection_result.detections
            if any(category.category_name == 'car' for category in detection.categories)
        ]
        return cars
