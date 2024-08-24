from pathlib import Path

import cv2
import numpy as np

from draw_utils import CountPlotter, draw_panel, draw_text
from tracker import Tracker
from yolo_detector import ObjectDetector

HERE = Path(__file__).parent

WIN_TITLE = 'Contador de veiculos'
IMG_HEIGHT = 540
PANEL_WIDTH = 300


detector = ObjectDetector()
tracker = Tracker()
plotter = CountPlotter(tracker)
cap = cv2.VideoCapture(filename=HERE / 'data' / 'cars.mp4')
roi = None

while cap.isOpened:
    ret, frame = cap.read()
    if not ret:
        break

    scale = IMG_HEIGHT / frame.shape[0]
    frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    frame_height, frame_width, _ = frame.shape
    full_win = np.ones((frame_height, frame_width + PANEL_WIDTH, 3), dtype=frame.dtype) * 255

    objects = detector.detect(frame)

    if not roi:
        full_win[:frame_height, :frame_width] = frame
        cv2.rectangle(full_win, (frame_width, 0), (full_win.shape[1], full_win.shape[0]), (0, 0, 0), -1)
        draw_text(full_win, 'Selecione a regiao de interesse\ne pressione [Enter]', frame_width + 10, 20, bg_cfg={'alpha': 0}, font_cfg={'color': (255, 255, 255)})
        roi = cv2.selectROI(WIN_TITLE, full_win, False)
    if roi == (0, 0, 0, 0):
        roi = (0, 0, frame_width, frame_height)

    objects = tracker.update(objects, roi)
    for obj in objects:
        obj.draw(frame)
    tracker.draw(frame, objects)

    full_win[:frame_height, :frame_width] = frame
    plotter.plot(full_win, frame_width)
    draw_panel(full_win, PANEL_WIDTH, tracker)

    cv2.imshow(WIN_TITLE, full_win)
    if cv2.waitKey(1) == 27:
        break
