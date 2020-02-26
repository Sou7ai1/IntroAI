#!/usr/bin/env python3

import statistics
from heuristics import *
from graphs import *
from informed_search import *

def heuristics_2D_experiment():
    print("n grid_2D_heuristic grid_diagonal_2D_heuristic")
    grid = Grid2D(42,1)
    for n in range(10,501,10):
        print(n, informed_search(grid, grid_2D_heuristic, (0,0), (n,n))[1], informed_search(grid, grid_diagonal_2D_heuristic, (0,0), (n,n))[1])

def heuristics_3D_experiment():
    print("n grid_3D_heuristic grid_face_diagonal_3D_heuristic grid_all_diagonal_3D_heuristic")
    grid = Grid3D(42,1)
    for n in range(2,41,2):
        print(n, informed_search(grid, grid_3D_heuristic, (0,0,0), (n,n,n))[1], informed_search(grid, grid_face_diagonal_3D_heuristic, (0,0,0), (n,n,n))[1], informed_search(grid, grid_all_diagonal_3D_heuristic, (0,0,0), (n,n,n))[1])

def density_experiment():
    print("p first min mean max")
    for i in range(24):
        probability = (100-i)/100
        visited = list(informed_search(Grid2D(1+j+i*54253,probability), grid_2D_heuristic, (0,0), (0,100))[1] for j in range(10))
        print(probability, visited[0], min(visited), statistics.mean(visited), max(visited))

def repetition_experiment():
    print("distance visited")
    for i in range(150):
        print(*informed_search(Grid2D(1+i*577,0.9), grid_2D_heuristic, (0,0), (0,100)))

if __name__ == "__main__":
    tests = {
            "Heuristics2D": heuristics_2D_experiment,
            "Heuristics3D": heuristics_3D_experiment,
            "Density": density_experiment,
            "Repetition": repetition_experiment
    }
    if len(sys.argv) == 1:
        for name in tests:
            print("Running experiment ", name)
            tests[name]()
            print("Experiment done.")
    else:
        name = sys.argv[1]
        if name in tests:
            tests[name]()
        else:
            print("Unknown test", name)
