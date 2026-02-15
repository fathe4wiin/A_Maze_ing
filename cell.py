from typing import Dict, Optional

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: Dict[str, bool] = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited: bool = False
        self.neighbors: Dict[str, Optional['Cell']] = {
            'N': None, 'E': None, 'S': None, 'W': None
        }  

    def remove_wall_with(self, neighbor: 'Cell') -> None:
        dx = neighbor.x - self.x
        dy = neighbor.y - self.y
        if dx == 1:
            self.walls['E'] = False
            neighbor.walls['W'] = False
        elif dx == -1:
            self.walls['W'] = False
            neighbor.walls['E'] = False
        elif dy == 1:
            self.walls['S'] = False
            neighbor.walls['N'] = False
        elif dy == -1:
            self.walls['N'] = False
            neighbor.walls['S'] = False

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"