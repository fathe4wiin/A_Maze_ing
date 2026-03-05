from .cell import Cell
from .maze_algo import MazeAlgo
from .parsing import Config


class MazeGen:
    def __init__(self) -> None:
        pass

    def create_cell_layout(self, width: int, height: int) -> list[list[Cell]]:
        layout: list[list[Cell | None]] = [
            [None for _ in range(width)] for _ in range(height)]
        visited: list[list[bool]] = [
            [False for _ in range(width)] for _ in range(height)]

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < width and 0 <= y < height

        # Directions table : (dx, dy, direction, opposite)
        directions = [
            (0, -1, 'N', 'S'),
            (1, 0, 'E', 'W'),
            (0, 1, 'S', 'N'),
            (-1, 0, 'W', 'E')
        ]

        def flood_fill(start_x: int, start_y: int) -> None:
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
                            assert cell is not None
                            cell.neighbors[dirn] = neighbor
                            neighbor.neighbors[opp] = cell

        flood_fill(0, 0)
        # Filter out None values and return
        result: list[list[Cell]] = []
        for row in layout:
            filtered_row: list[Cell] = [cell for cell in row if cell is not None]
            if filtered_row:
                result.append(filtered_row)
        return result

    def generate_maze(self,
                      layout: list[list[Cell]],
                      config: Config) -> list[list[Cell]]:
        return MazeAlgo.generate_maze(layout, 0, 0, config)
