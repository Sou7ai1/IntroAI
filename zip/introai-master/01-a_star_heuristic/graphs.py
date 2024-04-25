import itertools

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
        self.dimension = len(directions[0])
        self.directions = set()
        for d in directions:
            perm = list(set(itertools.permutations(d)))
            for n in range(len(d)+1):
                for c in itertools.combinations(range(len(d)), n):
                    for p in perm:
                        p = list(p)
                        for i in c:
                            p[i] = -p[i]                    
                        self.directions.add(tuple(p))
        self.directions = list(self.directions)
#        print("Directions: ", self.directions)

    def oracle(self, u, v):
        """
            Determine whether a given two vertices are connected by an edge in a subgraph.
            Vertices must be adjacent in whole grid which is not tested since it is slow.
        """
#        assert tuple(a-b for (a,b) in zip(u,v)) in self.directions
        if v < u:
            u,v = v,u
        prime = 2147483647
        acc = prime//2
        for x in [u,v]:
            for y in x:
                acc = (acc * self.salt + y) % prime
        return abs(acc) < self.probability * prime

    def neighbours(self, vertex):
        """ Return a list of all neighbours of a given vertex. """
        grid_neighbours = [ tuple(a+b for (a,b) in zip(vertex,d)) for d in self.directions ]
        return [ u for u in grid_neighbours if self.oracle(vertex,u) ]

# All grids follows.
# See file task.md for description of all grids.

class Grid2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,1] ])

class GridDiagonal2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,1], [1,1] ])

class GridRook2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,i+1] for i in range(8) ])

class GridGreatKing2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [i+1,j+1] for i in range(8) for j in range(8) ])  

class GridJumper2D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [2,3] ])

class Grid3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,0,1] ])

class GridFaceDiagonal3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,0,1], [0,1,1] ])

class GridAllDiagonal3D(Grid):
    def __init__(self, salt, probability):
        super().__init__(salt, probability, [ [0,0,1], [0,1,1], [1,1,1] ])
