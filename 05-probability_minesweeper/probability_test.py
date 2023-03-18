#!/usr/bin/env python3

import sys
import numpy as np
from minesweeper_common import UNKNOWN, MINE, get_neighbors
from minesweeper_player import Player

def evaluate(mine_prb, board, correct_probabilities):
    """
        Run a single tests to verify the correctness of calculating the probability of a mine on each cell.
        mine_prb: The unconditional probability of a mine on each cell.
        board: A state of a game with some explored cells.
        correct_probabilities: Expected probabilities (calculated by teacher)

        Note that it is impossible to calculate all probabilities exactly since some results are rational numbers
        which cannot be exactly stored in floating point numbers.
    """
    player = Player(board.shape[0], board.shape[1], board, mine_prb)
    player.preprocess_all()
    print("Tested board:")
    print(board)
    tested_probabilities = player.get_each_mine_probability()
    print("Correct probabilities of mines")
    print(correct_probabilities)
    print("Your probabilities of mines")
    print(tested_probabilities)
    diff = sum(abs(tested_probabilities[i,j] - correct_probabilities[i,j]) for i in range(board.shape[0]) for j in range(board.shape[1]))
    print("The sum of differences between the correct and your probabilities of mines is", diff)
    return diff < 1e-6

def main():
    tests = {
        "first": (
            0.2,
            np.array([
                [1, UNKNOWN, UNKNOWN],
                [UNKNOWN, UNKNOWN, UNKNOWN]
            ]),
            np.array([
                [0, 1 / 3, 0.2],
                [1 / 3, 1 / 3, 0.2]
            ]),
        ),
        "second": (
            0.7,
            np.array([
                [2, UNKNOWN, UNKNOWN],
                [UNKNOWN, UNKNOWN, UNKNOWN]
            ]),
            np.array([
                [0, 2 / 3, 0.7],
                [2 / 3, 2 / 3, 0.7]
            ]),
        ),
        "third": (
            0.2,
            np.array([
                [1, UNKNOWN, UNKNOWN],
                [1, UNKNOWN, UNKNOWN]
            ]),
            np.array([
                [0, 0.5, 0.2],
                [0, 0.5, 0.2]
            ]),
        ),
        "fourth": (
            0.3,
            np.array(
                [[1, UNKNOWN, UNKNOWN],
                [1, UNKNOWN, UNKNOWN],
                [1, UNKNOWN, UNKNOWN]]
            ),
            np.array([
                [0, 0, 0.3],
                [0, 1, 0.3],
                [0, 0, 0.3]
            ]),
        ),
        "fifth": (
            0.4,
            np.array(
                [[1, UNKNOWN, UNKNOWN],
                [2, UNKNOWN, UNKNOWN],
                [1, UNKNOWN, UNKNOWN]]
            ),
            np.array([
                [0, 1, 0.4],
                [0, 0, 0.4],
                [0, 1, 0.4]
            ]),
        ),
        "sixth": (
            0.15,
            np.array([
                [1, UNKNOWN, UNKNOWN],
                [2, UNKNOWN, UNKNOWN],
                [MINE, 2, 1]
            ]),
            np.array([
                [0, 0.15, 0.15],
                [0, 0.85, 0.15],
                [1, 0, 0]
            ]),
        ),
        "seventh": (
            0.2,
            np.array(
                [
                    [0, 1, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                    [0, 1, UNKNOWN, 3, UNKNOWN, UNKNOWN, UNKNOWN],
                    [0, 1, 1, 3, UNKNOWN, UNKNOWN, UNKNOWN],
                    [0, 1, UNKNOWN, 3, UNKNOWN, UNKNOWN, UNKNOWN],
                    [0, 1, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                ]
            ),
            np.array(
                [
                    [0.0, 0.0, 0.5, 0.3, 0.3, 0.2, 0.2],
                    [0.0, 0.0, 0.5, 0.0, 0.6, 0.2, 0.2],
                    [0.0, 0.0, 0.0, 0.0, 0.8, 0.2, 0.2],
                    [0.0, 0.0, 0.5, 0.0, 0.6, 0.2, 0.2],
                    [0.0, 0.0, 0.5, 0.3, 0.3, 0.2, 0.2],
                ]
            ),
        ),
        "eighth": (
            0.22,
            np.array(
                [
                    [0, 2, MINE, 3, UNKNOWN, 2, UNKNOWN],
                    [0, 3, UNKNOWN, 5, UNKNOWN, UNKNOWN, UNKNOWN],
                    [1, 3, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                    [UNKNOWN, UNKNOWN, 4, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                    [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                ]
            ),
            np.array(
                [
                    [0.0, 0.0, 1.0, 0.0, 0.5, 0.0, 1 / 3],
                    [0.0, 0.0, 1.0, 0.0, 0.5, 1 / 3, 1 / 3],
                    [0.0, 0.0, 1.0, 0.73898942, 0.26101058, 0.22, 0.22],
                    [0.26101058, 0.73898942, 0.0, 0.38050529, 0.22, 0.22, 0.22],
                    [0.22, 0.38050529, 0.38050529, 0.38050529, 0.22, 0.22, 0.22],
                ]
            ),
        ),
    }

    if len(sys.argv) == 1:
        success = True
        for name in tests:
            print("Running test", name)
            success = evaluate(*tests[name]) and success
            print()
        print("All tests passed." if success else "Some tests failed.")
    else:
        name = sys.argv[1]
        if name in tests:
            evaluate(*tests[name])
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 probability_test.py

To run a test NAME, run the command
$ python3 probability_test.py NAME
"""
if __name__ == "__main__":
    main()
