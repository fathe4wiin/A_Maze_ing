from cell import Cell

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

        def flood_fill(x, y):
            if not in_bounds(x, y) or visited[y][x]:
                return
            cell = Cell(x, y)
            layout[y][x] = cell
            visited[y][x] = True
            for dx, dy, dirn, opp in directions:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny):
                    if layout[ny][nx] is None:
                        flood_fill(nx, ny)
                    neighbor = layout[ny][nx]
                    cell.neighbors[dirn] = neighbor
                    if neighbor:
                        neighbor.neighbors[opp] = cell

        flood_fill(0, 0)
        return layout
    
    def generate_maze(self, layout: list[list[Cell]], perfect: bool):
        from maze_algorithms import MazeAlgorithms
        maze_algo = MazeAlgorithms()
        if perfect:
            maze_algo.generate_perfect_maze(layout)
        else:
            maze_algo.generate_imperfect_maze(layout)
    