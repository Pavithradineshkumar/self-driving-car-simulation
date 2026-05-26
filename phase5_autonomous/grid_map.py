import numpy as np
from phase5_autonomous.constants import GRID_COLS, GRID_ROWS


class OccupancyGrid:
    """
    A 2D grid representing free/occupied space ahead of the car.

    Built each frame from ObjectDetector results.
    Used by A* to plan around detected obstacles.

    Grid orientation:
        Row 0    = top of frame (far ahead)
        Row N-1  = bottom of frame (right in front of car)
        Col 0    = left edge of road
        Col N-1  = right edge of road
    """

    def __init__(self, frame_width, frame_height):
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.fw   = frame_width
        self.fh   = frame_height

        # 0 = free, 1 = occupied
        self.grid = np.zeros((self.rows, self.cols), dtype=np.uint8)

    def update(self, detections):
        """
        Rebuild the grid from fresh detection list.
        Each detection's bounding box is mapped to grid cells and marked.
        """
        # Reset every frame
        self.grid[:] = 0

        cell_w = self.fw / self.cols
        cell_h = self.fh / self.rows

        for det in detections:
            if not det["in_danger"] and det["distance_m"] and det["distance_m"] > 25:
                # Far objects — don't block grid
                continue

            x1, y1, x2, y2 = det["box"]

            # Convert pixel bbox to grid cell range
            col_start = max(0,          int(x1 / cell_w))
            col_end   = min(self.cols,  int(x2 / cell_w) + 1)
            row_start = max(0,          int(y1 / cell_h))
            row_end   = min(self.rows,  int(y2 / cell_h) + 1)

            self.grid[row_start:row_end, col_start:col_end] = 1

        return self.grid

    def is_blocked(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row, col] == 1
        return True   # Out of bounds = treat as blocked

    def pixel_to_cell(self, px, py):
        col = int(px / (self.fw / self.cols))
        row = int(py / (self.fh / self.rows))
        return (row, col)

    def cell_to_pixel(self, row, col):
        px = int((col + 0.5) * (self.fw / self.cols))
        py = int((row + 0.5) * (self.fh / self.rows))
        return (px, py)