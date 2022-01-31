#!/usr/bin/env python3

import sys
from time import time
from prettytable import PrettyTable

from heuristics import grid_2D_heuristic, grid_diagonal_2D_heuristic, grid_3D_heuristic, grid_face_diagonal_3D_heuristic, grid_all_diagonal_3D_heuristic, grid_knight_2D_heuristic
from graphs import Grid2D, GridDiagonal2D, GridKnight2D, Grid3D, GridFaceDiagonal3D, GridAllDiagonal3D
from informed_search import informed_search

def informed_search_test(graph, heuristic, origin, destination, expected_distance):
    """ Run a single test of A* algorithm.
    graph -- an instance of a Grid
    heuristic -- a function estimating distance between two vertices
    origin -- a starting point of a path
    destination -- a terminal point of a path
    expected_distance -- the expected length of a shortest path
    """
    status,msg,found_distance,visited = informed_search(graph, heuristic, origin, destination)
    if not status:
        return (status, msg)
    if found_distance > expected_distance:
        # In this case, A* is confused by heuristic which is probably non-monotonic.
        return (False, "The path your heuristic found is longer than a shortest path")
    if found_distance < expected_distance:
        # This case is expected not to happend. This most likely means incorrect setting of tests.
        return (False, "Your heuristic found a shorter path than the optimal which should be impossible")
    print("Your heuristic found a path from", origin, "to", destination, "of length", expected_distance, "and visited", visited, "vertices")
    return (status, msg)

def informed_search_dataset(dataset):
    """ Run a set of tests """
    for d in dataset:
        status, msg = informed_search_test(*d)
        if not status:
            return (status, msg)
    return (True, "Correct")

def main():
    grid_2D_tests = [
        (Grid2D(42,0.9), grid_2D_heuristic, (0,0), (3,3), 6),
        (Grid2D(3240,0.8), grid_2D_heuristic, (1,2), (21,26), 44),
        (Grid2D(2235,0.7), grid_2D_heuristic, (-5,3), (112,147), 261),
        (Grid2D(1439,0.6), grid_2D_heuristic, (-674,-341), (284,148), 1605),
        (Grid2D(565,1), grid_2D_heuristic, (-76457,-36498), (47647,28745), 189347)
    ]
    grid_diagonal_2D_tests = [
        (GridDiagonal2D(42,0.9), grid_diagonal_2D_heuristic, (0,0), (3,3), 3),
        (GridDiagonal2D(16424,0.8), grid_diagonal_2D_heuristic, (1,2), (21,26), 29),
        (GridDiagonal2D(1234,0.7), grid_diagonal_2D_heuristic, (-5,3), (112,147), 166),
        (GridDiagonal2D(93542,0.5), grid_diagonal_2D_heuristic, (-574,-641), (784,448), 1426),
        (GridDiagonal2D(565,1), grid_diagonal_2D_heuristic, (-76457,-36498), (47647,28745), 124104)
    ]
    grid_knight_2D_tests = [
        (GridKnight2D(42,0.9), grid_knight_2D_heuristic, (0,0), (3,3), 2),
        (GridKnight2D(16424,0.8), grid_knight_2D_heuristic, (1,2), (21,26), 16),
        (GridKnight2D(1234,0.7), grid_knight_2D_heuristic, (-5,3), (112,147), 87),
        (GridKnight2D(45645,0.4), grid_knight_2D_heuristic, (-248,-398), (147,145), 424),
        (GridKnight2D(565,1), grid_knight_2D_heuristic, (-6457,-6498), (7647,8745), 9783),
        (GridKnight2D(4387,1), grid_knight_2D_heuristic, (-6457,-898), (-6647,745), 823)
    ]
    grid_3D_tests = [
        (Grid3D(42,0.9), grid_3D_heuristic, (0,0,0), (3,3,3), 9),
        (Grid3D(54236,0.5), grid_3D_heuristic, (50,-12,34), (-5,24,65), 198),
        (Grid3D(9748,0.5), grid_3D_heuristic, (124,353,-124), (145,200,-234), 330),
        (Grid3D(24325,1), grid_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8989),
        (Grid3D(4578,1), grid_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 8049),
        (Grid3D(7687,1), grid_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 11412)
    ]
    grid_face_diagonal_3D_tests = [
        (GridFaceDiagonal3D(42,0.9), grid_face_diagonal_3D_heuristic, (0,0,0), (3,3,3), 5),
        (GridFaceDiagonal3D(54236,0.5), grid_face_diagonal_3D_heuristic, (50,-12,34), (-5,24,65), 69),
        (GridFaceDiagonal3D(4348,0.7), grid_face_diagonal_3D_heuristic, (124,-245,-657), (-354,124,-416), 544),
        (GridFaceDiagonal3D(4348,0.2), grid_face_diagonal_3D_heuristic, (174,253,-224), (245,200,-284), 115),
        (GridFaceDiagonal3D(24325,1), grid_face_diagonal_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8196),
        (GridFaceDiagonal3D(4578,1), grid_face_diagonal_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 4196),
        (GridFaceDiagonal3D(7687,1), grid_face_diagonal_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 5706)
    ]
    grid_all_diagonal_3D_tests = [
        (GridAllDiagonal3D(42,0.9), grid_all_diagonal_3D_heuristic, (0,0,0), (3,3,3), 3),
        (GridAllDiagonal3D(54236,0.5), grid_all_diagonal_3D_heuristic, (50,-12,34), (-5,24,65), 55),
        (GridAllDiagonal3D(43547,0.7), grid_all_diagonal_3D_heuristic, (124,-145,-257), (-154,124,-316), 278),
        (GridAllDiagonal3D(4348,0.15), grid_all_diagonal_3D_heuristic, (224,253,-224), (245,200,-284), 94),
        (GridAllDiagonal3D(24325,1), grid_all_diagonal_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8196),
        (GridAllDiagonal3D(4578,1), grid_all_diagonal_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 4196),
        (GridAllDiagonal3D(7687,1), grid_all_diagonal_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 4196)
    ]

    tests = {
            "Grid2D": (grid_2D_tests, 1, 11),
            "Grid3D": (grid_3D_tests, 1, 26),
            "GridDiagonal2D": (grid_diagonal_2D_tests, 1, 18),
            "GridAllDiagonal3D": (grid_all_diagonal_3D_tests, 1, 14),
            "GridFaceDiagonal3D": (grid_face_diagonal_3D_tests, 3, 11),
            "GridKnight2D": (grid_knight_2D_tests, 3, 7)
    }

    if len(sys.argv) == 1:
        results = PrettyTable(["Test name", "Points", "Reference time [s]", "Your time [s]", "Evaluation"])
        for name in tests:
            print("Running test", name)
            dataset, points, time_limit = tests[name]
            start_time = time()
            status, msg = informed_search_dataset(dataset)
            running_time = time() - start_time
            print(msg)
            print()
            results.add_row([name, points, time_limit, running_time, msg])
        print(results)
    else:
        name = sys.argv[1]
        if name in tests:
            dataset, points, time_limit = tests[name]
            status, msg = informed_search_dataset(dataset)
            print(msg)
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 informed_search_tests.py

To run a test NAME, run the command
$ python3 informed_search_tests.py NAME
"""
if __name__ == "__main__":
    main()
