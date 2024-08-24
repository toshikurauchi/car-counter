import cv2


class DetectedObject:
    def __init__(self, x, y, width, height, track_id, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.track_id = track_id
        self.label = label
        self.valid = False  # Flag to indicate if the object has passed through the ROI
        self.track = []  # List of points to draw the object's trajectory

    def draw(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 255, 0), 1)
        return frame
