import cv2
import numpy as np


def draw_text(frame, text, x, y, font_cfg=None, bg_cfg=None):
    if font_cfg is None:
        font_cfg = {}
    if bg_cfg is None:
        bg_cfg = {}

    bg_alpha = bg_cfg.get('alpha', 0.8)
    bg_color = bg_cfg.get('color', (255, 255, 255))
    padding = bg_cfg.get('padding', 5)

    font_family = font_cfg.get('family', cv2.FONT_HERSHEY_SIMPLEX)
    font_color = font_cfg.get('color', (0, 0, 0))
    font_scale = font_cfg.get('scale', 0.5)
    thickness = font_cfg.get('thickness', 1)
    line_height = font_cfg.get('line_height', 1.5)

    lines = text.split('\n')
    text_width = 0
    text_height = 0
    for line in lines:
        (lw, lh), _ = cv2.getTextSize(line, font_family, font_scale, thickness)
        text_width = max(text_width, lw)
        text_height += int(lh * line_height)

    sub_img = frame[y-lh-padding:y-lh+text_height+padding, x-padding:x+text_width+padding]
    bg_rect = np.ones_like(sub_img)
    bg_rect[:] = bg_color

    res = cv2.addWeighted(sub_img, 1 - bg_alpha, bg_rect, bg_alpha, 0)
    frame[y-lh-padding:y-lh+text_height+padding, x-padding:x+text_width+padding] = res

    for i, line in enumerate(lines):
        y_offset = y + i * int(lh * line_height)
        cv2.putText(frame, line, (x, y_offset), font_family, font_scale, font_color, thickness)


def draw_panel(frame, panel_width, tracker):
    panel_x = frame.shape[1] - panel_width
    cv2.rectangle(frame, (panel_x, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)

    total = 0
    for i, (label, color) in enumerate(tracker.labels.items()):
        count = tracker.count_valid(label)
        total += count
        y = 70 + i * 30
        draw_text(frame, f'{tracker.translate[label]}: {count}', panel_x + 10, y, bg_cfg={'alpha': 0}, font_cfg={'color': color})
    draw_text(frame, f'Total: {total}', panel_x + 10, 20, bg_cfg={'alpha': 0}, font_cfg={'color': (255, 255, 255)})

    return frame


class CountPlotter:
    def __init__(self, tracker):
        self.max_x = 5
        self.max_value = 2
        self.tracker = tracker
        self.count_lists = {label: [] for label in tracker.labels}

    def plot(self, frame, plot_width):
        self.max_x = min(self.max_x + 5, plot_width)

        for label, count_list in self.count_lists.items():
            count_list.append(self.tracker.count_valid_alive(label))
            self.max_value = max(self.max_value, count_list[-1])

        ready_to_plot = all(len(counts) > 1 for counts in self.count_lists.values())
        if ready_to_plot:
            for label, counts in self.count_lists.items():
                self._plot(frame, counts, self.tracker.labels[label], True)
            for label, counts in self.count_lists.items():
                self._plot(frame, counts, self.tracker.labels[label], False)

        return frame

    def _plot(self, frame, values, color, fill):
        frame_height = frame.shape[0]
        plot_height = frame_height // 3

        dx = self.max_x / max(len(values) - 1, 1)
        dy = plot_height / (self.max_value - 1)

        pts = [
            [int((i - 1) * dx), frame_height - int(value * dy)]
            for i, value in enumerate(values)
        ]
        pts[-1][0] = self.max_x

        if fill:
            pts.append((self.max_x, frame_height))
            pts.append((0, frame_height))
        pts = np.array(pts, np.int32)
        pts = pts.reshape((-1, 1, 2))

        if len(pts) > (3 if fill else 1):
            if fill:
                poly = np.zeros_like(frame)
                alpha = 0.5
                cv2.fillPoly(poly, [pts], color)
                frame[:] = cv2.addWeighted(frame, 1, poly, alpha, 0)
            else:
                cv2.polylines(frame, [pts], False, color, 3)
