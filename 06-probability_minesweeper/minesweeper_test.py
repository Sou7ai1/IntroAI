#!/usr/bin/env python3

import sys
import random
import numpy
from minesweeper_common import UNKNOWN, MINE, get_neighbors
from minesweeper_player import Player

class MineSweeper:
    # Data for a single game.
    def __init__(self, rows, columns, mine_prb, rng):
        #  Initialize a board of given size with the probability of a mine on each cell and mine generator.
        self.rows = rows
        self.columns = columns
        self.mine_prb = mine_prb

        # Matrix of all neighbor cells for every cell.
        self.neighbors = get_neighbors(rows, columns)

        # Matrix for the solution of the game.
        self.solution = solution = numpy.full(rows*columns, 0).reshape((rows, columns))
        for i in range(rows):
            for j in range(columns):
                solution[i,j] = MINE if rng.random() < mine_prb else UNKNOWN

        # The number of cells to be explored by a player.
        self.remaining = sum(1 if solution[i,j] == UNKNOWN else 0 for i in range(rows) for j in range(columns))

        # Matrix for a player
        self.game = numpy.full(rows*columns, UNKNOWN).reshape((rows, columns))
        self.player = Player(self.rows, self.columns, self.game, self.mine_prb)

    def play(self):
        # Play whole game.
        while self.remaining:
            if not self.turn():
                return False
        return True

    def turn(self):
        # Make one turn of the game.
        i,j = pos = self.player.turn()
        assert(isinstance(i, int) and 0 <= i and i < self.rows)
        assert(isinstance(j, int) and 0 <= j and j < self.columns)
        if self.solution[pos] == MINE:
            return False
        assert(self.solution[pos] == UNKNOWN)

        # Count the number of mines in the neighborhood of (x,y)
        self.game[pos] = self.solution[pos] = sum(1 if self.solution[neigh] == MINE else 0 for neigh in self.neighbors[pos])
        self.remaining -= 1
        return True

def evaluate(rows, columns, mine_prb, seed, games, win_points):
    """
        Run given number of games on a board of given size.
        In order to generate mines, thier probability and seed generator is given.
        win_points is an array of numbers of games needed to win to get one point.
    """
    print("Test contains", games, "games on a board of size", rows, "*", columns, "and the probability of a mine on cell is", mine_prb)
    rng = random.Random(seed)
    wins = 0
    for i in range(games):
        if MineSweeper(rows, columns, mine_prb, rng).play():
            wins += 1
    points = sum(1 if wins >= p else 0 for p in win_points)
    print("You won", wins, "out of", games, "games. You will recieve", points, "points assuming time and memory limits are satisfied.")

def main():
    # Parameters for all tests.
    # Two numbers in comments are numbers win games of the trivial and teacher's player.
    # Extra challenge is to surpass you teacher.
    tests = {
        "first": (5, 7, 0.2, 4, 100, [31,37]), # 28, 39
        "second": (9, 8, 0.1, 6, 100, [70,76]), # 63, 80
        "third": (12, 15, 0.15, 42, 100, [55,67]), # 42, 70
        "fourth": (15, 18, 0.16, 123, 50, [21,27]), # 17, 29
        "fifth": (30, 25, 0.12, 4125432, 30, [19,25]), # 16, 26
        }
    if len(sys.argv) == 1:
        for name in tests:
            print("Running test", name)
            evaluate(*tests[name])
    else:
        name = sys.argv[1]
        if name in tests:
            evaluate(*tests[name])
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 minesweeper_test.py

To run a test NAME, run the command
$ python3 minesweeper_test.py NAME
"""
if __name__ == "__main__":
    main()
