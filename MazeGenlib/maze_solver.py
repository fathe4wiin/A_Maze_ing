from .cell import Cell
from typing import Optional, Dict


def bfs(maze: list[list[Cell]], start: Cell, exit: Cell) -> list[Cell] | None:
    queue: list[Cell] = [start]
    visited: set[Cell] = {start}
    parent: Dict[Cell, Optional[Cell]] = {start: None}

    while queue:
        current = queue.pop(0)
        if current == exit:
            break

        for neighbor in current.neighbors.values():
            if neighbor and current.is_accessible(
                    neighbor) and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    if exit not in parent:
        return None

    path: list[Cell] = []
    cell: Optional[Cell] = exit
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    return path
