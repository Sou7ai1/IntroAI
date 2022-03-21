import numpy

UNKNOWN = -1
MINE = -2
NEIGHBOURS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def get_neighbors(rows, columns):
    neighbors = numpy.ndarray((rows,columns),dtype=numpy.object)
    for i in range(rows):
        for j in range(columns):
            neighbors[i,j] = [ (i+x,j+y) for (x,y) in NEIGHBOURS if 0 <= i+x and i+x < rows and 0 <= j+y and j+y < columns ]
    return neighbors
