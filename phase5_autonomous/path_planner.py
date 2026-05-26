import heapq
import math
from phase5_autonomous.constants import GRID_COLS, GRID_ROWS


class AStarPlanner:
    """
    A* path planner on the OccupancyGrid.

    Finds the shortest path from the car's current grid cell
    to a goal cell (typically the top-center = road ahead).

    Returns a list of (row, col) cells forming the path,
    or an empty list if no path exists.
    """

    # 8-directional movement: up, down, left, right + diagonals
    DIRECTIONS = [
        (-1,  0, 1.0),   # up
        ( 1,  0, 1.0),   # down
        ( 0, -1, 1.0),   # left
        ( 0,  1, 1.0),   # right
        (-1, -1, 1.414), # diagonal
        (-1,  1, 1.414),
        ( 1, -1, 1.414),
        ( 1,  1, 1.414),
    ]

    def find_path(self, grid, start, goal):
        """
        grid  : 2D numpy array (0=free, 1=blocked)
        start : (row, col) — car's current cell
        goal  : (row, col) — target cell

        Returns list of (row, col) from start to goal (inclusive),
        or [] if no path found.
        """
        rows, cols = grid.shape

        # Priority queue: (f_score, (row, col))
        open_set = []
        heapq.heappush(open_set, (0.0, start))

        # Track which cell each cell was reached from
        came_from = {}

        # g_score[cell] = best known cost from start to cell
        g_score = {start: 0.0}

        # f_score[cell] = g_score + heuristic
        f_score = {start: self._heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            # Goal reached — reconstruct path
            if current == goal:
                return self._reconstruct(came_from, current)

            for dr, dc, cost in self.DIRECTIONS:
                neighbor = (current[0] + dr, current[1] + dc)
                nr, nc   = neighbor

                # Skip out-of-bounds or blocked cells
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if grid[nr, nc] == 1:
                    continue

                tentative_g = g_score[current] + cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    # Found a better path to this neighbor
                    came_from[neighbor] = current
                    g_score[neighbor]   = tentative_g
                    f_score[neighbor]   = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # No path found
        return []

    def _heuristic(self, a, b):
        """
        Euclidean distance heuristic.
        Admissible for 8-directional grids with diagonal cost √2.
        """
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def _reconstruct(self, came_from, current):
        """Trace back through came_from to build the full path."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path