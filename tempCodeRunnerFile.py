    config: Config = Config("config.txt")
    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    gen = maze.generate_maze(layout, config.PERFECT)