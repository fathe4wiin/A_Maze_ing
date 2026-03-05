from .cell import Cell
from .maze_solver import bfs
from .errors import MazeError

def generate_output_file(maze: list[list[Cell]], start_coord: tuple, exit_coord: tuple, filename: str):
    try:
        with open(filename, 'w') as f:
            for row in maze:
                line = ""
                for cell in row:
                    val = 0
                    if cell.walls['N']:
                        val |= 1
                    if cell.walls['E']:
                        val |= 2
                    if cell.walls['S']:
                        val |= 4
                    if cell.walls['W']:
                        val |= 8
                    line += hex(val)[2:].upper()
                f.write(line + "\n")
            
            f.write("\n")
            
            f.write(f"{start_coord[0]},{start_coord[1]}\n")
            f.write(f"{exit_coord[0]},{exit_coord[1]}\n")
            
            start_cell = maze[start_coord[1]][start_coord[0]]
            exit_cell = maze[exit_coord[1]][exit_coord[0]]
            path = bfs(maze, start_cell, exit_cell)
            
            path_str = ""
            if path:
                for i in range(len(path) - 1):
                    curr, next_c = path[i], path[i+1]
                    if next_c.y < curr.y: path_str += 'N'
                    elif next_c.x > curr.x: path_str += 'E'
                    elif next_c.y > curr.y: path_str += 'S'
                    elif next_c.x < curr.x: path_str += 'W'
            
            f.write(path_str + "\n")
    except PermissionError:
        raise MazeError(f"Permission denied: Cannot write to '{filename}'")
    except IsADirectoryError:
        raise MazeError(f"'{filename}' is a directory, not a file")
    except OSError as e:
        raise MazeError(f"Failed to write output file '{filename}': {e}")
