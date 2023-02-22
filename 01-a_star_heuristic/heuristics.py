# TODO: Implement more efficient monotonic heuristic
#
# Every function receive coordinates of two grid points returns estimated distance between them.
# Each argument is a tuple of two or three integer coordinates.
# See file task.md for description of all grids.

import math
from graphs import Grid2D, GridDiagonal2D, GridQueen2D, GridGreatKing2D, GridRook2D, GridJumper2D, Grid3D, GridFaceDiagonal3D, GridAllDiagonal3D

# For two points a and b in the n-dimensional space, return the d-dimensional point r such that r_i = | a_i - b_i | for i = 1...d
def distance_in_each_coordinate(x, y):
    return [ abs(a-b) for (a,b) in zip(x, y) ]

def calculate_distance(graph, size):
    """
        For a given graph (derived from Grid) and size, calculate lengths of shortest paths from (0,0) to all vertices (a,b) where 0 <= a < size and 0 <= b < size.
        Returns a matrix dists (a list of lists) where dists[a][b] is the length of the shortest path between (0,0) to (a,b) in the graph.
        Warning: Vertices of the graph must be two dimensional coordinates.
    """
    dists = [ [-1 for _ in range(size)] for _ in range(size) ]
    dists[0][0] = 0
    queue = [ (0,0) ]
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        d = dists[u[0]][u[1]] + 1
        for v in graph.neighbours(u):
            a = abs(v[0])
            b = abs(v[1])
            if a < size and b < size and dists[a][b] == -1:
                dists[a][b] = d
                queue.append((a,b))
    return dists

def grid_2D_heuristic(current, destination):
    return 0

def grid_diagonal_2D_heuristic(current, destination):
    return 0

def grid_3D_heuristic(current, destination):
    return 0

def grid_face_diagonal_3D_heuristic(current, destination):
    return 0

def grid_all_diagonal_3D_heuristic(current, destination):
    return 0

def grid_queen_2D_heuristic(current, destination):
    return 0

def grid_great_king_2D_heuristic(current, destination):
    return 0

def grid_rook_2D_heuristic(current, destination):
    return 0

def grid_jumper_2D_heuristic(current, destination):
    return 0
