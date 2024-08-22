import cv2


class DetectedObject:
    def __init__(self, x, y, width, height, track_id=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.track_id = track_id

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 255, 0), 1)
        return frame
