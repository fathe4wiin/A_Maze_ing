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
        self.color: int = 0xFFFFFFFF
        self.dark_color: int = 0xFF7F7F7F
        self.in_path: bool = False

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

    def is_accessible(self, neighbor: 'Cell'):
        if neighbor.x == self.x + 1:
            return not self.walls['E']
        elif neighbor.x == self.x - 1:
            return not self.walls['W']
        elif neighbor.y == self.y + 1:
            return not self.walls['S']
        elif neighbor.y == self.y - 1:
            return not self.walls['N']
        return False