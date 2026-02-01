import pygame
import sys
from maze_gen import MazeGen
from parsing import Config


class MazeVisualizer:
    def __init__(self, config_file="config.txt"):
        # Parse configuration
        self.config = Config(config_file)
        self.WIDTH = self.config.WIDTH
        self.HEIGHT = self.config.HEIGHT
        self.ENTRY = self.config.ENTRY
        self.EXIT = self.config.EXIT
        self.PERFECT = self.config.PERFECT
        
        # Cell size in pixels
        self.CELL_SIZE = 40
        self.WALL_THICKNESS = 2
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (0, 100, 255)
        
        # Screen dimensions
        self.screen_width = self.WIDTH * self.CELL_SIZE
        self.screen_height = self.HEIGHT * self.CELL_SIZE
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Maze Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Generate maze
        self.maze_gen = MazeGen()
        self.layout = self.maze_gen.create_cell_layout(self.WIDTH, self.HEIGHT)
        self.maze_gen.generate_maze(self.layout, self.PERFECT)
        
    def draw_maze(self):
        """Draw the maze on the pygame screen"""
        self.screen.fill(self.WHITE)
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                cell = self.layout[y][x]
                if cell is None:
                    continue
                
                # Calculate cell position
                cell_x = x * self.CELL_SIZE
                cell_y = y * self.CELL_SIZE
                
                # Draw cell background
                pygame.draw.rect(
                    self.screen,
                    self.WHITE,
                    (cell_x, cell_y, self.CELL_SIZE, self.CELL_SIZE)
                )
                
                # Draw walls
                if cell.walls['N']:  # North wall
                    pygame.draw.line(
                        self.screen,
                        self.BLACK,
                        (cell_x, cell_y),
                        (cell_x + self.CELL_SIZE, cell_y),
                        self.WALL_THICKNESS
                    )
                if cell.walls['E']:  # East wall
                    pygame.draw.line(
                        self.screen,
                        self.BLACK,
                        (cell_x + self.CELL_SIZE, cell_y),
                        (cell_x + self.CELL_SIZE, cell_y + self.CELL_SIZE),
                        self.WALL_THICKNESS
                    )
                if cell.walls['S']:  # South wall
                    pygame.draw.line(
                        self.screen,
                        self.BLACK,
                        (cell_x, cell_y + self.CELL_SIZE),
                        (cell_x + self.CELL_SIZE, cell_y + self.CELL_SIZE),
                        self.WALL_THICKNESS
                    )
                if cell.walls['W']:  # West wall
                    pygame.draw.line(
                        self.screen,
                        self.BLACK,
                        (cell_x, cell_y),
                        (cell_x, cell_y + self.CELL_SIZE),
                        self.WALL_THICKNESS
                    )
        
        # Draw entry point (green circle)
        entry_x, entry_y = self.ENTRY
        entry_center = (
            int(entry_x * self.CELL_SIZE + self.CELL_SIZE / 2),
            int(entry_y * self.CELL_SIZE + self.CELL_SIZE / 2)
        )
        pygame.draw.circle(self.screen, self.GREEN, entry_center, 8)
        
        # Draw exit point (red circle)
        exit_x, exit_y = self.EXIT
        exit_center = (
            int(exit_x * self.CELL_SIZE + self.CELL_SIZE / 2),
            int(exit_y * self.CELL_SIZE + self.CELL_SIZE / 2)
        )
        pygame.draw.circle(self.screen, self.RED, exit_center, 8)
        
        # Draw legend
        legend_text = "Green = Entry | Red = Exit"
        text_surface = self.font.render(legend_text, True, self.BLACK)
        self.screen.blit(text_surface, (10, 10))
    
    def run(self):
        """Run the visualization loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    visualizer = MazeVisualizer()
    visualizer.run()


if __name__ == "__main__":
    main()
