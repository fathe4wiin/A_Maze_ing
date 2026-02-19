from cell import Cell
from maze_algo import MazeAlgo

class MazeGen():
    def __init__(self):
        pass

    def create_cell_layout(self, width: int, height: int) -> list[list[Cell]]:
        layout = [[None for _ in range(width)] for _ in range(height)]
        visited = [[False for _ in range(width)] for _ in range(height)]

        def in_bounds(x, y):
            return 0 <= x < width and 0 <= y < height

        # Directions table : (dx, dy, direction, opposite)
        directions = [
            (0, -1, 'N', 'S'),
            (1, 0, 'E', 'W'),
            (0, 1, 'S', 'N'),
            (-1, 0, 'W', 'E')
        ]

        def flood_fill(start_x, start_y):
            stack = [(start_x, start_y)]
            while stack:
                x, y = stack.pop()
                if visited[y][x]:
                    continue
                
                if layout[y][x] is None:
                    layout[y][x] = Cell(x, y)
                cell = layout[y][x]
                visited[y][x] = True
                
                for dx, dy, dirn, opp in directions:
                    nx, ny = x + dx, y + dy
                    if in_bounds(nx, ny):
                        if not visited[ny][nx]:
                            if layout[ny][nx] is None:
                                layout[ny][nx] = Cell(nx, ny)
                            stack.append((nx, ny))
                        
                        neighbor = layout[ny][nx]
                        if neighbor:
                            cell.neighbors[dirn] = neighbor
                            neighbor.neighbors[opp] = cell

        flood_fill(0, 0)
        return layout
    
    def generate_maze(self, layout: list[list[Cell]], perfect: bool):
        return MazeAlgo.generate_maze(layout, 0, 0, perfect)
    