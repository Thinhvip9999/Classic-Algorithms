# Intro-to-AI
Classic path finding algorithms and some inference engine
# Intro to AI

This repository contains implementations of classic pathfinding algorithms and some inference engines. The main focus is on various search algorithms used in AI for finding paths in a grid-based environment.

## Table of Contents

- [Algorithms](#algorithms)
  - [A* Algorithm](#a-algorithm)
  - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
  - [Depth-Limited Search (DLS)](#depth-limited-search-dls)
  - [Iterative Deepening Search (IDS)](#iterative-deepening-search-ids)
  - [Iterative Deepening A* (IDA*)](#iterative-deepening-a-ida)
- [Utility Scripts](#utility-scripts)
  - [Check Map](#check-map)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Algorithms

### A* Algorithm

The A* algorithm is a popular pathfinding and graph traversal algorithm. It uses a heuristic to efficiently find the shortest path from a start node to a goal node.

- **File:** `astar.py`
- **Function:** `astar`
- **Description:** Finds the shortest path from the start position to one of the goal positions using the A* algorithm.

### Breadth-First Search (BFS)

BFS is a simple and effective algorithm for traversing or searching tree or graph data structures.

- **File:** `bfs.py`
- **Function:** `bfs`
- **Description:** Finds the shortest path from the start position to one of the goal positions using the BFS algorithm.

### Depth-Limited Search (DLS)

DLS is a depth-first search algorithm with a predetermined limit on the depth of search.

- **File:** `cus1.py`
- **Function:** `depth_limited_search`
- **Description:** Searches the grid to a specified depth limit.

### Iterative Deepening Search (IDS)

IDS combines the depth-first search's space-efficiency and breadth-first search's optimality.

- **File:** `cus1.py`
- **Function:** `iterative_deepening_search`
- **Description:** Repeatedly applies DLS with increasing depth limits until the goal is found.

### Iterative Deepening A* (IDA*)

IDA* is an informed search algorithm that combines the features of A* and iterative deepening search.

- **File:** `cus2.py`
- **Function:** `ida_star`
- **Description:** Uses a combination of depth-first search and heuristic information to find the shortest path to the goal.

## Utility Scripts

### Check Map

The `check_map.py` script is used to read and display a grid map from an input file.

- **File:** `check_map.py`
- **Description:** Reads grid data from an input file, marks start and goal positions, and prints the grid.

## Getting Started

To get started with these algorithms, clone the repository and ensure you have Python installed.

sh
git clone https://github.com/Thinhvip9999/Intro-to-AI.git
cd Intro-to-AI
Usage
Each algorithm can be executed individually by running the corresponding Python script. For example, to run the A* algorithm:

python astar.py

To check and print a map:
python check_map.py path/to/input_file.txt

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

License
This repository is licensed under the MIT License. See the LICENSE file for more information.

Feel free to customize this content further based on your specific needs and details.
