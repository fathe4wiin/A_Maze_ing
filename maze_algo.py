import random
from maze_gen import Cell
from cell import Cell

class MazeAlgo():
    def __init__(self, seed, perfect: bool):
        self.seed = seed
        self.perfect = perfect
        random.seed(seed)
        
    @staticmethod
    def generate_maze(maze: list[list[Cell]], start_x, start_y, seed=None):
        if seed is not None:
            random.seed(seed)
        height = len(maze)
        width = len(maze[0])
        
        stack = []
        n_cell: Cell
        current: Cell = maze[start_y][start_x]
        current.visited = True
        while True:
            unvisited_neighbors = []
            for direction, neighbor in current.neighbors.items():
                if neighbor and not neighbor.visited:
                    unvisited_neighbors.append((direction, neighbor))
            if unvisited_neighbors:
                n_dir, n_cell = random.choice(unvisited_neighbors)
            elif not stack:
                break
            else:
                current = stack.pop()
                continue
            current.remove_wall_with(n_cell)
            stack.append(current)
            n_cell.visited = True
            current = n_cell