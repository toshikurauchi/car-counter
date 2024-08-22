from pathlib import Path

import cv2

from yolo_car_detector import CarDetector

HERE = Path(__file__).parent


detector = CarDetector()
cap = cv2.VideoCapture(filename=HERE / 'data' / 'cars.mp4')

while cap.isOpened:
    ret, frame = cap.read()
    if not ret:
        break
    cars = detector.detect(frame)
    for car in cars:
        car.draw(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == 27:
        break
