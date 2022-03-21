import numpy
from minesweeper_common import UNKNOWN, MINE, get_neighbors

RUN_TESTS = False

"""
    TODO: Improve the strategy for playing Minesweeper provided in this file.
    The provided strategy simply counts the number of unexplored mines in the neighborhood of each cells.
    If this couting concludes that a cell has to contain a mine, then it is marked.
    If it concludes that a cell cannot contain a mine, then it is explored; i.e. function Player.preprocessing returns its coordinates.
    If the simple couting algorithm does not find a unexplored cell provably without a mine,
     function Player.probability_player is called to find an unexplored cell with the minimal probability having a mine.
    A recommended approach is implementing the function Player.get_each_mine_probability.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * Player.__init__ is called in the beginning of every game.
        * Player.turn is called to explore one cell.
"""

class Player:
    def __init__(self, rows, columns, game, mine_prb):
        # Initialize a player for a game on a board of given size with the probability of a mine on each cell.
        self.rows = rows
        self.columns = columns
        self.game = game
        self.mine_prb = mine_prb

        # Matrix of all neighbor cells for every cell.
        self.neighbors = get_neighbors(rows, columns)

        # Matrix of numbers of missing mines in the neighborhood of every cell.
        # -1 if a cell is unexplored.
        self.mines = numpy.full(rows*columns, -1).reshape((rows, columns))

        # Matrix of the numbers of unexplored neighborhood cells, excluding known mines.
        self.unknown = numpy.full(rows*columns, 0).reshape((rows, columns))
        for i in range(self.rows):
            for j in range(self.columns):
                self.unknown[i,j] = len(self.neighbors[i,j])

        # A set of cells for which the precomputed values self.mines and self.unknown need to be updated.
        self.invalid = set()

    def turn(self):
        # Returns the position of one cell to be explored.
        pos = self.preprocessing()
        if not pos:
            pos = self.probability_player()
        self.invalidate_with_neighbors(pos)
        return pos

    def probability_player(self):
        # Return an unexplored cell with the minimal probability of mine
        prb = self.get_each_mine_probability()
        min_prb = 1
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game[i,j] == UNKNOWN:
                    if prb[i,j] > 0.9999: # Float-point arithmetics may not be exact.
                        self.game[i,j] = MINE
                        self.invalidate_with_neighbors((i,j))
                    if min_prb > prb[i,j]:
                        min_prb = prb[i,j]
                        best_position = (i,j)
        return best_position

    def invalidate_with_neighbors(self, pos):
        # Insert a given position and its neighborhood to the list of cell requiring update of precomputed information.
        self.invalid.add(pos)
        for neigh in self.neighbors[pos]:
            self.invalid.add(neigh)

    def preprocess_all(self):
        # Preprocess all cells
        self.invalid = set((i,j) for i in range(self.rows) for j in range(self.columns))
        pos = self.preprocessing()
        assert(pos == None) # Preprocessing is incomplete

    def preprocessing(self):
        """
            Update precomputed information of cells in the set self.invalid.
            Using a simple counting, check cells which have to contain a mine.
            If this simple counting finds a cell which cannot contain a mine, then returns its position.
            Otherwise, returns None.
        """
        while self.invalid:
            pos = self.invalid.pop()

            # Count the numbers of unexplored neighborhood cells, excluding known mines.
            self.unknown[pos] = sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[pos])

            if self.game[pos] >= 0:
                # If the cell pos is explored, count the number of missing mines in its neighborhood.
                self.mines[pos] = self.game[pos] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[pos])
                assert(0 <= self.mines[pos] and self.mines[pos] <= self.unknown[pos])

                if self.unknown[pos] > 0:
                    if self.mines[pos] == self.unknown[pos]:
                        # All unexplored neighbors have to contain a mine, so mark them.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                self.game[neigh] = MINE
                                self.invalidate_with_neighbors(neigh)

                    elif self.mines[pos] == 0:
                        # All mines in the neighborhood was found, so explore the rest.
                        self.invalid.add(pos) # There may be other unexplored neighbors.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                return neigh
                        assert(False) # There has to be at least one unexplored neighbor.

        if not RUN_TESTS:
            return None

        # If the invalid list is empty, so self.unknown and self.mines should be correct.
        # Verify it to be sure.
        for i in range(self.rows):
            for j in range(self.columns):
                assert(self.unknown[i,j] == sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[i,j]))
                if self.game[i,j] >= 0:
                    assert(self.mines[i,j] == self.game[i,j] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[i,j]))

    def get_each_mine_probability(self):
        # Returns a matrix of probabilities of a mine of each cell
        probability = numpy.zeros((self.rows,self.columns))
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game[i,j] == MINE:
                    probability[i,j] = 1

        # TODO: Finish this calculations
        # Implementing this function is not obligatory but it may help to fulfill the homework.
        # This function is tested by the file probability_test.py.

        return probability
