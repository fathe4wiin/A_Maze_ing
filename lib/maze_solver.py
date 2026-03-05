from .cell import Cell

def bfs(maze: list[list[Cell]], start: Cell, exit: Cell):
    queue = [start]
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.pop(0)
        if current == exit:
            break

        for neighbor in current.neighbors.values():
            if neighbor and current.is_accessible(neighbor) and neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    if exit not in parent:
        return None

    path = []
    cell = exit
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    return path
