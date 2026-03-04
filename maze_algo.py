import random
from cell import Cell
from parsing import Config

class MazeAlgo():
    def __init__(self, perfect: bool):
        self.perfect = perfect
        
    @staticmethod
    def generate_maze(maze: list[list[Cell]], start_x, start_y, config: Config):
        if is_in_42_pattern(config.ENTRY[0], config.ENTRY[1], config) or is_in_42_pattern(config.EXIT[0], config.EXIT[1], config):
            return None
        
        stack = []
        current: Cell = maze[start_y][start_x]
        current.visited = True
        mark_four_two(maze, config)
        while True:
            unvisited_neighbors = []
            for direction, neighbor in current.neighbors.items():
                if neighbor and not neighbor.visited:
                    unvisited_neighbors.append((direction, neighbor))
            
            if unvisited_neighbors:
                n_dir, n_cell = random.choice(unvisited_neighbors)
                # Only remove wall if neither cell is part of the 42 config.pattern
                if not is_in_42_pattern(current.x, current.y, config) and not is_in_42_pattern(n_cell.x, n_cell.y, config):
                    current.remove_wall_with(n_cell)
                stack.append(current)
                n_cell.visited = True
                current = n_cell
            elif stack:
                current = stack.pop()
            else:
                break
        
        if not config.PERFECT:
            unpefect_the_maze(maze, config)
        return maze


def unpefect_the_maze(maze: list[list[Cell]], config: Config):
    height = config.HEIGHT
    width = config.WIDTH
    section_height = 2
    section_width = 2

    for y in range(0, height - section_height + 1, section_height):
        for x in range(0, width - section_width + 1, section_width):
            ruin_the_maze(maze, y, x, section_height, section_width, config)


def ruin_the_maze(
    maze: list[list[Cell]],
    y: int,
    x: int,
    section_height: int,
    section_width: int,
    config: Config
):
    candidates = []
    for i in range(y, y + section_height):
        for j in range(x, x + section_width):
            cell = maze[i][j]
            for d, neighbor in cell.neighbors.items():
                if neighbor is None:
                    continue
                ni, nj = neighbor.y, neighbor.x
                if (
                    y <= ni < y + section_height and
                    x <= nj < x + section_width and 
                    cell.walls[d] and not
                    is_in_42_pattern(nj, ni, config) and not
                    is_in_42_pattern(cell.x, cell.y, config)
                ):
                    candidates.append((cell, neighbor))
    if candidates:
        target, neighbor = random.choice(candidates)
        target.remove_wall_with(neighbor)
        
        

def is_in_42_pattern(x, y, config: Config):
    """Check if (x, y) is part of the '42' config.pattern centered in the maze."""
    if config.pattern == False:
        return
    four = [
        (0,0), (0,1), (0,2), # Left vertical
        (1,2),               # Middle horizontal
        (2,0), (2,1), (2,2), (2,3), (2,4) # Right vertical
    ]
    two = [
        (4,0), (5,0), (6,0), # Top horizontal
        (6,1),               # Top right
        (4,2), (5,2), (6,2), # Middle horizontal
        (4,3),               # Bottom left
        (4,4), (5,4), (6,4)  # Bottom horizontal
    ]
    offset_x = (config.WIDTH - 7) // 2
    offset_y = (config.HEIGHT - 5) // 2
    pattern_coords = set((px + offset_x, py + offset_y) for px, py in four + two)
    return (x, y) in pattern_coords


def mark_four_two(maze: list[list[Cell]], config: Config):
    for row in maze:
        for cell in row:
            if is_in_42_pattern(cell.x, cell.y, config):
                cell.visited = True

