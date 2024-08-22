from collections import defaultdict

import cv2
import numpy as np


class Tracker:
    def __init__(self):
        self.colors = defaultdict(lambda: tuple(int(v) for v in np.random.randint(0, 255, 3)))
        self.track_history = defaultdict(lambda: [])

    def update(self, objects):
        for obj in objects:
            self.track_history[obj.track_id].append((obj.x + obj.width / 2, obj.y + obj.height / 2))

    def draw(self, frame):
        for track_id, track in self.track_history.items():
            if len(track) < 2:
                continue
            points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
            color = self.colors[track_id]
            cv2.polylines(frame, [points], isClosed=False, color=color, thickness=3)
        return frame
