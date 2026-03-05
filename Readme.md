*This project has been created as part of the 42 curriculum by [aidbrm], [bfathi].*

# A_MAZE_ING

## Description

A_MAZE_ING is a Python-based maze project that generates, displays, and lets you solve mazes interactively. The goal is to build a fully functional maze experience — from procedural generation to interactive solving — with a clean terminal interface.

The project is split into two main phases:
- **Generation**: a perfect maze (no loops, fully connected) is generated using the **BFS (Breadth-First Search)** algorithm, ensuring an even, unbiased spread across the grid.
- **Solving**: the maze is solved using **DFS (Depth-First Search)**, which explores paths deeply before backtracking, mimicking how a player might navigate.

A player can be added to the maze, and a score is tracked during solving. A menu is displayed before generation, and the maze can be exported to a text file.

---

## Instructions

### Requirements

- Python 3.x
- `make` (GNU Make)

### Installation & Execution

```bash
# Clone the repository
git clone <git@vogsphere-v2-bg.1337.ma:vogsphere/intra-uuid-cc02e3ad-82f2-4939-b852-43d9d2f82228-7175356-aidbrm>
cd A_MAZE_ING

# Run the project
make run
```

All configuration is handled via the config file (see below). No additional arguments are required.

---

## Configuration File

The project is configured through a config file at the root of the repository. Here is the complete structure and all available fields:

```ini
WIDTH=20          # Number of columns in the maze
HEIGHT=15         # Number of rows in the maze
ENTRY=3,4         # Entry point coordinates (column,row)
EXIT=5,4          # Exit point coordinates (column,row)
OUTPUT_FILE=maze.txt  # Path to save the maze as a text file
PERFECT=True      # If True, generates a perfect maze (no loops, all cells connected)
SEED=42           # Random seed for reproducible maze generation
```

| Field         | Type    | Description                                      |
|---------------|---------|--------------------------------------------------|
| `WIDTH`       | int     | Width of the maze in cells                       |
| `HEIGHT`      | int     | Height of the maze in cells                      |
| `ENTRY`       | x,y     | Coordinates of the maze entry point              |
| `EXIT`        | x,y     | Coordinates of the maze exit point               |
| `OUTPUT_FILE` | string  | File path where the maze will be saved           |
| `PERFECT`     | bool    | Whether to enforce a perfect maze (no cycles)    |
| `SEED`        | int     | Seed for the random number generator             |

---

## Maze Generation Algorithm

**Algorithm used: BFS (Breadth-First Search)**

BFS was chosen for generation because it expands outward from the starting cell in a level-by-level fashion, producing mazes with shorter, more evenly distributed paths. This results in a more balanced maze structure compared to DFS-generated mazes, which tend to produce long winding corridors. BFS generation also pairs well with a DFS solver, since the generated maze's structure challenges the depth-first exploration without making it trivially easy.

---

## Maze Solving Algorithm

**Algorithm used: DFS (Depth-First Search)**

DFS was used for solving because it naturally mimics how a player explores a maze — committing to a path until hitting a dead end, then backtracking. It is simple to implement recursively and integrates cleanly with the player movement system.

---

## Advanced Features

- **Interactive player**: A player character can be placed in the maze and moved through it manually.
- **Score system**: A score is tracked during the solving phase.
- **Pre-generation menu**: A menu is shown before maze generation, allowing configuration review.
- **Text file output**: The maze can be exported to a `.txt` file via `OUTPUT_FILE`.
- **Reproducible mazes**: Setting a `SEED` value guarantees the same maze is generated every time.

---

## Reusable Components

The following modules are designed to be reusable outside of this project:

| Component          | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **Maze generation**| BFS-based generator; accepts width, height, seed, and perfect-maze flag     |
| **Maze solving**   | DFS-based solver; works on any valid grid-based maze structure              |
| **Seed system**    | Deterministic random generation; plug into any procedural generation task   |
| **Output file**    | Maze-to-text serializer; adaptable for other grid-based outputs             |

> The visualization module is tightly coupled to the project's display system and is **not** intended for reuse as-is.

---

## Team & Project Management

### Roles

| Member   | Responsibilities                                                                 |
|----------|----------------------------------------------------------------------------------|
| `aidbrm` | Config parsing, maze visualization, Makefile, output file export, project packaging |
| `bfathi` | Maze generation (BFS), maze solving (DFS), player system, pre-generation menu, score system |

### Planning & Evolution

The project was managed using **Git branches** — each feature was developed on its own branch and merged once stable. This kept the main branch clean and allowed both members to work in parallel without conflicts.

The initial plan was to split the project cleanly between "infrastructure" (aidbrm) and "logic" (bfathi), which held up well throughout development. Integration between the two halves (e.g. connecting the generator output to the visualizer) required some coordination but was manageable.

**What worked well:**
- Git branch separation kept work independent and conflicts minimal.
- The config file approach made testing different maze sizes and seeds fast and easy.
- Clear role separation meant both members could work simultaneously with little overlap.

**What could be improved:**
- More frequent integration checkpoints would have caught interface mismatches earlier.
- A shared document for agreed-upon data structures at the start would have saved some back-and-forth.

### Tools Used

- **Git / GitHub** — version control and branch-based collaboration
- **Claude (AI)** — used to understand project requirements, clarify algorithmic concepts (BFS vs DFS trade-offs), and get guidance on project structure

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [BFS — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [DFS — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Jamis Buck's blog — Maze algorithms (classic reference)](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Python `collections.deque` for BFS](https://docs.python.org/3/library/collections.html#collections.deque)
- [Visualizing maze algorithms — redblobgames.com](https://www.redblobgames.com/)

### AI Usage

**Tool used: Claude**

Claude was used during the project for:
- Understanding the requirements and how to approach the project structure
- Clarifying the differences and trade-offs between BFS and DFS for generation vs. solving
- Getting guidance on Python packaging and Makefile setup