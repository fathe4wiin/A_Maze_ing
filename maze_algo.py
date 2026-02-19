import random
from cell import Cell

class MazeAlgo():
    def __init__(self, seed, perfect: bool):
        self.seed = seed
        self.perfect = perfect
        random.seed(seed)
        
    @staticmethod
    def generate_maze(maze: list[list[Cell]], start_x, start_y, perfect: bool, seed=None):
        if seed is not None:
            random.seed(seed)
        
        stack = []
        current: Cell = maze[start_y][start_x]
        current.visited = True

        mark_four_two(maze)
        while True:
            unvisited_neighbors = []
            for direction, neighbor in current.neighbors.items():
                if neighbor and not neighbor.visited:
                    unvisited_neighbors.append((direction, neighbor))
            
            if unvisited_neighbors:
                n_dir, n_cell = random.choice(unvisited_neighbors)
                current.remove_wall_with(n_cell)
                stack.append(current)
                n_cell.visited = True
                current = n_cell
            elif stack:
                current = stack.pop()
            else:
                break
            yield maze
        
        if not perfect:
            unpefect_the_maze(maze)
            yield maze


def unpefect_the_maze(maze: list[list[Cell]], seed=None):
    if seed is not None:
        random.seed(seed)
    height = len(maze)
    width = len(maze[0])
    section_height = 2
    section_width = 2

    for y in range(0, height - section_height + 1, section_height):
        for x in range(0, width - section_width + 1, section_width):
            ruin_the_maze(maze, y, x, section_height, section_width)


def ruin_the_maze(
    maze: list[list[Cell]],
    y: int,
    x: int,
    section_height: int,
    section_width: int,
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
                    cell.walls[d]
                ):
                    candidates.append((cell, neighbor))
    if candidates:
        target, neighbor = random.choice(candidates)
        target.remove_wall_with(neighbor)
        
        

def mark_four_two(maze: list[list[Cell]]):
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
        offset_x = (len(maze[0]) - 7) // 2
        offset_y = (len(maze) - 5) // 2
        for x, y in four + two:
            if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
                maze[y+offset_y][x+offset_x].visited = True

