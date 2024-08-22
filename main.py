from pathlib import Path

import cv2

from tracker import Tracker
from yolo_car_detector import CarDetector

HERE = Path(__file__).parent


detector = CarDetector()
tracker = Tracker()
cap = cv2.VideoCapture(filename=HERE / 'data' / 'cars.mp4')

while cap.isOpened:
    ret, frame = cap.read()
    if not ret:
        break
    cars = detector.detect(frame)
    tracker.update(cars)
    for car in cars:
        car.draw(frame)
    tracker.draw(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break
