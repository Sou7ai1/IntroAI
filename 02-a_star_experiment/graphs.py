import sys

class Grid:
    """ Interface of an abstract grid. """

    def __init__(self, salt, probability, directions):
        """
        salt -- additional integer input to the oracle
        probability -- probability of each edge to be kept in a subgraph of a grid
        directions -- list of all neighbours of the origin
        """

        self.salt = salt * 6487304627
        self.probability = probability
        self.directions = directions + list( tuple(-x for x in d) for d in directions )

    def oracle(self, u, v):
        """ Return a list of all neighbours of a given vertex. """
        if not tuple(a-b for (a,b) in zip(u,v)) in self.directions:
            return False
        if v < u:
            u,v = v,u
        prime = 2147483647
        acc = prime//2
        for x in [u,v]:
            for y in x:
                acc = (acc * self.salt + y) % prime
        return abs(acc)  < self.probability * prime

    def neighbours(self, vertex):
        """ Return a list of all neighbours of a given vertex. """
        grid_neighbours = [ tuple(a+b for (a,b) in zip(vertex,d)) for d in self.directions ]
        return list( u for u in grid_neighbours if self.oracle(vertex,u) )


# All grids follows.
# See file task.md for description of all grids.

class Grid2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (0,1), (1,0) ])

class GridDiagonal2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (0,1), (1,0), (1,1), (1,-1) ])

class GridKnight2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (2,1), (1,2), (-2,1), (-1,2) ])

class Grid3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (0,0,1), (0,1,0), (1,0,0) ])

class GridFaceDiagonal3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (0,0,1), (0,1,0), (1,0,0), (0,1,1), (1,1,0), (1,0,1), (0,-1,1), (-1,1,0), (-1,0,1) ])

class GridAllDiagonal3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ (0,0,1), (0,1,0), (1,0,0), (0,1,1), (1,1,0), (1,0,1), (0,-1,1), (-1,1,0), (-1,0,1), (1,1,1), (1,1,-1), (1,-1,1), (-1,1,1) ])
