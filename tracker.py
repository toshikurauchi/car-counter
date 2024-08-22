import cv2


class Tracker:
    def __init__(self):
        self.tracker = cv2.MultiTracker_create()

    def add(self, frame, cars):
        self.tracker = cv2.TrackerCSRT_create()
