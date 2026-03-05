

class Stats:
    def __init__(self) -> None:
        self.steps: int = 0
        self.mazes_solved: int = 0

    def add_step(self) -> None:
        self.steps += 1

    def add_maze(self) -> None:
        self.mazes_solved += 1
        self.steps = 0
