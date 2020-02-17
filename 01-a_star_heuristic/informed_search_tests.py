#!/usr/bin/env python3

from heuristics import *
from graphs import *
from informed_search import *

def informed_search_test(graph, heuristic, origin, destination, distance):
    """ Run a single test of A* algorithm. 
    graph -- an instance of a Grid
    heuristic -- a function estimating distance between two vertices
    origin -- a starting point of a path
    destination -- a terminal point of a path
    distance -- the expected length of a shortest path
    """
    (length,visited) = informed_search(graph, heuristic, origin, destination)
    print("Distance between an origin and a destination is {} and heuristic is {}. Number of visited vertices is {}.".format(distance, heuristic(origin,destination), visited))
    assert length == distance, "A* did not found a shortest path"

def grid_2D_tests():
    informed_search_test(Grid2D(42,0.9), grid_2D_heuristic, (0,0), (3,3), 6)
    informed_search_test(Grid2D(16424,0.8), grid_2D_heuristic, (1,2), (21,26), 46)
    informed_search_test(Grid2D(1234,0.7), grid_2D_heuristic, (-5,3), (112,147), 263)
    informed_search_test(Grid2D(93532,0.5), grid_2D_heuristic, (-674,-341), (284,148), 4721)
    informed_search_test(Grid2D(565,1), grid_2D_heuristic, (-76457,-36498), (47647,28745), 189347)

def grid_diagonal_2D_tests():
    informed_search_test(GridDiagonal2D(42,0.9), grid_diagonal_2D_heuristic, (0,0), (3,3), 3)
    informed_search_test(GridDiagonal2D(16424,0.8), grid_diagonal_2D_heuristic, (1,2), (21,26), 25)
    informed_search_test(GridDiagonal2D(1234,0.7), grid_diagonal_2D_heuristic, (-5,3), (112,147), 150)
    informed_search_test(GridDiagonal2D(93532,0.5), grid_diagonal_2D_heuristic, (-574,-641), (784,448), 1567)
    informed_search_test(GridDiagonal2D(565,1), grid_diagonal_2D_heuristic, (-76457,-36498), (47647,28745), 124104)

def grid_knight_2D_tests():
    informed_search_test(GridKnight2D(42,0.9), grid_knight_2D_heuristic, (0,0), (3,3), 2)
    informed_search_test(GridKnight2D(16424,0.8), grid_knight_2D_heuristic, (1,2), (21,26), 16)
    informed_search_test(GridKnight2D(1234,0.7), grid_knight_2D_heuristic, (-5,3), (112,147), 91)
    informed_search_test(GridKnight2D(45645,0.2), grid_knight_2D_heuristic, (-248,-398), (147,145), 850)
    informed_search_test(GridKnight2D(565,1), grid_knight_2D_heuristic, (-6457,-6498), (7647,8745), 9783)
    informed_search_test(GridKnight2D(4387,1), grid_knight_2D_heuristic, (-6457,-898), (-6647,745), 823)

def grid_3D_tests():
    informed_search_test(Grid3D(42,0.9), grid_3D_heuristic, (0,0,0), (3,3,3), 9)
    informed_search_test(Grid3D(54236,0.5), grid_3D_heuristic, (50,-12,34), (-5,24,65), 122)
    informed_search_test(Grid3D(4348,0.4), grid_3D_heuristic, (124,353,-124), (145,200,-234), 308)
    informed_search_test(Grid3D(24325,1), grid_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8989)
    informed_search_test(Grid3D(4578,1), grid_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 8049)
    informed_search_test(Grid3D(7687,1), grid_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 11412)

def grid_face_diagonal_3D_tests():
    informed_search_test(GridFaceDiagonal3D(42,0.9), grid_face_diagonal_3D_heuristic, (0,0,0), (3,3,3), 5)
    informed_search_test(GridFaceDiagonal3D(54236,0.5), grid_face_diagonal_3D_heuristic, (50,-12,34), (-5,24,65), 61)
    informed_search_test(GridFaceDiagonal3D(4348,0.7), grid_face_diagonal_3D_heuristic, (124,-245,-657), (-354,124,-416), 544)
    informed_search_test(GridFaceDiagonal3D(4348,0.2), grid_face_diagonal_3D_heuristic, (174,253,-224), (245,200,-284), 112)
    informed_search_test(GridFaceDiagonal3D(24325,1), grid_face_diagonal_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8196)
    informed_search_test(GridFaceDiagonal3D(4578,1), grid_face_diagonal_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 4196)
    informed_search_test(GridFaceDiagonal3D(7687,1), grid_face_diagonal_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 5706)

def grid_all_diagonal_3D_tests():
    informed_search_test(GridAllDiagonal3D(42,0.9), grid_all_diagonal_3D_heuristic, (0,0,0), (3,3,3), 3)
    informed_search_test(GridAllDiagonal3D(54236,0.5), grid_all_diagonal_3D_heuristic, (50,-12,34), (-5,24,65), 55)
    informed_search_test(GridAllDiagonal3D(43547,0.7), grid_all_diagonal_3D_heuristic, (124,-145,-257), (-154,124,-316), 279)
    informed_search_test(GridAllDiagonal3D(4348,0.1), grid_all_diagonal_3D_heuristic, (224,253,-224), (245,200,-284), 91)
    informed_search_test(GridAllDiagonal3D(24325,1), grid_all_diagonal_3D_heuristic, (654321,123456,-5548), (654784,123786,2648), 8196)
    informed_search_test(GridAllDiagonal3D(4578,1), grid_all_diagonal_3D_heuristic, (654321,-1245,-2548), (654784,2145,1648), 4196)
    informed_search_test(GridAllDiagonal3D(7687,1), grid_all_diagonal_3D_heuristic, (654321,-1245,-2548), (658147,2145,1648), 4196)

if __name__ == "__main__":
    tests = {
            "Grid2D": grid_2D_tests,
            "GridDiagonal2D": grid_diagonal_2D_tests,
            "GridKnight2D": grid_knight_2D_tests,
            "Grid3D": grid_3D_tests,
            "GridAllDiagonal3D": grid_all_diagonal_3D_tests,
            "GridFaceDiagonal3D": grid_face_diagonal_3D_tests
    }
    if len(sys.argv) == 1:
        for name in tests:
            print("Running tests for", name)
            tests[name]()
            print("Passed.")
    else:
        name = sys.argv[1]
        if name in tests:
            tests[name]()
        else:
            print("Unknown test", name)
