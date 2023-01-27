# TODO: Implement more efficient monotonic heuristic
#
# Every function receive coordinates of two grid points returns estimated distance between them.
# Each argument is a tuple of two or three integer coordinates.
# See file task.md for description of all grids.

import math

# For two points a and b in the n-dimensional space, return the d-dimensional point r such that r_i = | a_i - b_i | for i = 1...d
def distance_in_each_coordinate(x, y):
    return [ abs(a-b) for (a,b) in zip(x, y) ]

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

def grid_rook_2D_heuristic(current, destination):
    return 0

def grid_jumper_2D_heuristic(current, destination):
    return 0
