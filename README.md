# AI Projects - MFF Charles University Exchange

This repository hosts a series of advanced Artificial Intelligence projects developed during my academic exchange at the Mathematics and Physics Faculty of Charles University. These projects cover a broad spectrum of AI techniques and applications.

## Project Descriptions

Each project is accompanied by a `task.md` file, which provides a detailed description of the project's objectives and requirements.

### Heuristic Implementations for Grid Navigation

- **Files**: `heuristics.py`, `graphs.py`, `task.md`
- **Description**: Implementations of various heuristic functions to estimate distances in grid-based problems, facilitating pathfinding algorithms for grids with different properties:
  - **2D Grids**: Manhattan and Chebyshev distances.
  - **3D Grids**: Euclidean-like measures and composite heuristics for more complex 3D environments.
  - **Special Grids**: Adaptations for grids mimicking movements of chess pieces like the rook and the knight.

### Minesweeper AI Strategy

- **Files**: `minesweeper_ai.py`, `task.md`
- **Description**: Development of an AI strategy for playing Minesweeper that uses probability calculations and safe exploration strategies to efficiently clear mines without detonating them.

### Robot Control Simulation

- **Files**: `robot_control.py`, `task.md`
- **Description**: Implementation of a control system for a robot navigating a grayscale environment, with strategies based on sensor readings and probabilistic movement outcomes.

### Graph Coloring and Constraint Solving

- **Files**: `graph_coloring.py`, `constraint.py`, `task.md`
- **Description**: Application of constraint programming and SAT solving techniques for graph coloring. This project involves:
  - **Total Coloring**: Finding total chromatic index and coloring for a graph using a constraint satisfaction problem solver.
  - **Using PySAT**: Implementing SAT solver strategies to determine minimal colorings and validate chromatic properties.
  - **Transport Domain**: Strategies and actions defined for manipulating transport scenarios within a specified domain, highlighting automated planning.

## Technologies Used

- Python
- SciPy and NumPy for numerical operations
- NetworkX for graph-based data structures
- PySAT for Boolean satisfiability problems
- Constraint Programming for solving complex coloring problems

## Installation

Clone the repository and install required Python libraries:

```bash
git clone https://github.com/Sou7ai1/IntroAI.git
cd IntroAImff
pip install -r requirements.txt
