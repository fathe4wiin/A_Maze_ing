

class Stats:
    def __init__(self):
        self.steps = 0
        self.mazes_solved = 0

    def add_step(self):
        self.steps += 1

    def add_maze(self):
        self.mazes_solved += 1
        self.steps = 0
