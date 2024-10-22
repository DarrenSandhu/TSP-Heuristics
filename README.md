# Travelling Salesman Problem (TSP) Solver

## Project Overview

This project implements various algorithms to solve the Travelling Salesman Problem (TSP), a classic problem in combinatorial optimization. The goal is to find the shortest route that visits each city once and returns to the starting point. The project includes both a **Command Line Interface (CLI)** for benchmarking the algorithms and a **Graphical User Interface (GUI)** for visualization.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Usage](#usage)
    - [Running the CLI](#running-the-cli)
    - [Running the GUI](#running-the-gui)
5. [Algorithms Implemented](#algorithms-implemented)
6. [Project Structure](#project-structure)
7. [Future Work](#future-work)
8. [License](#license)

## Key Features

- Implements multiple algorithms to solve TSP, including:
  - **Heuristics**: Two-Opt, Nearest Neighbour, Greedy with Cycle Avoidance, Insertion Heuristic with Convex Hull
  - **Meta-heuristics**: Large Neighbourhood Search with Max Iterations, Large Neighbourhood Search with Convergence
  - **Integer Programming**: Miller-Tucker-Zemlin formulation
- A GUI to visualize the algorithms and the solutions generated
- CLI for benchmarking algorithm performance and quality
- Extensive performance evaluation metrics (solution quality, execution time)

## Installation

1. Clone this repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that you have Python 3.6+ installed on your system.

4. For Gurobi license installation, follow the academic license instructions from Gurobi's website.

## Usage

### Running the CLI

To run the CLI and benchmark algorithms, navigate to the project’s code directory and run:

```bash
python3 Run_Code/CLI/cli.py
```

This will allow you to test various algorithms on predefined datasets and view their performance metrics.

### Running the GUI

To visualize the TSP solutions and interact with the algorithms via the GUI, execute:

```bash
python3 Run_Code/GUI/gui.py
```

Ensure you are in the `Run_Code` directory while running this command. The GUI will provide options for selecting algorithms and datasets for visualization.

## Algorithms Implemented

### Heuristics

- **Nearest Neighbour**: Simple greedy approach that builds a tour by selecting the nearest unvisited city.
- **Two-Opt**: Iterative optimization that improves the solution by reversing segments of the route.
- **Greedy with Cycle Avoidance**: Builds a solution while avoiding the creation of smaller cycles.
- **Insertion Heuristic with Convex Hull**: Starts with a convex hull and iteratively inserts the remaining cities.

### Meta-heuristics

- **Large Neighbourhood Search (Max Iterations)**: A local search-based optimization algorithm that explores larger neighborhoods.
- **Large Neighbourhood Search (Convergence)**: Similar to the max iteration variant but stops when solution convergence is achieved.

### Integer Programming

- **Miller-Tucker-Zemlin formulation**: An exact approach based on integer programming to solve the TSP.

## Project Structure

```bash
├── Run_Code
│   ├── CLI
│   │   ├── cli.py
│   ├── GUI
│   │   ├── gui.py
│   └── Algorithms
│       ├── heuristics.py
│       ├── meta_heuristics.py
│       ├── integer_programming.py
├── Data
│   ├── test_files
├── requirements.txt
└── README.md
```

## Future Work

- **Algorithm Optimization**: Fine-tuning the algorithms for performance improvements.
- **Parallelization**: Implement parallel computing to improve the execution time of algorithms.
- **Machine Learning Integration**: Exploring machine learning techniques to enhance the solution quality of the algorithms.
- **Improving the GUI**: Enhance the user interface for more interactive features and usability.
- **Real-world Applications**: Extend the algorithms to tackle real-world logistic and routing problems.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

