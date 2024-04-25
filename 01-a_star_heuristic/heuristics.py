# TODO: Implement more efficient monotonic heuristic
#
# Every function receive coordinates of two grid points returns estimated distance between them.
# Each argument is a tuple of two or three integer coordinates.
# See file task.md for description of all grids.

import math
from graphs import Grid2D, GridDiagonal2D, GridGreatKing2D, GridRook2D, GridJumper2D, Grid3D, GridFaceDiagonal3D, GridAllDiagonal3D

# For two points a and b in the n-dimensional space, return the d-dimensional point r such that r_i = | a_i - b_i | for i = 1...d
def distance_in_each_coordinate(x, y):
    return [ abs(a-b) for (a,b) in zip(x, y) ]

def grid_2D_heuristic(current, destination): #Using the Manhathan distance
    x,y = distance_in_each_coordinate(current,destination)       #Calculating the absolute of the y distance from initial position to the goal
    return  x+y

def grid_diagonal_2D_heuristic(current, destination):   # Using the max or the chebyshev
    x,y = distance_in_each_coordinate(current,destination)  
    return max(x,y)

def grid_3D_heuristic(current, destination):
    x,y,z = distance_in_each_coordinate(current,destination)  
    return x+y+z

def grid_face_diagonal_3D_heuristic(current, destination):
    x,y,z = distance_in_each_coordinate(current,destination) 
    return max(x,y,z,math.ceil((x+y+z)/2))

def grid_all_diagonal_3D_heuristic(current, destination):
    d=(current[0]-destination[0])**2+(current[1]-destination[1])**2+(current[2]-destination[2])**2
    return min((max(abs(current[0]-destination[0]),abs(current[1]-destination[1]),abs(current[2]-destination[2])),math.sqrt(d)))

def grid_great_king_2D_heuristic(current, destination):
    x,y = distance_in_each_coordinate(current,destination) 
    return (math.ceil(((x+y)/8)/2))

def grid_rook_2D_heuristic(current, destination):
    x,y = distance_in_each_coordinate(current,destination) 
    return(math.ceil((x+y)/8))

def grid_jumper_2D_heuristic(current, destination):
    x,y = distance_in_each_coordinate(current,destination) 
    return(math.ceil(max((x+y)/3,x/3,y/2)))
