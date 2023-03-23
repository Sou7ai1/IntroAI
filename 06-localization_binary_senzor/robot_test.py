#!/usr/bin/env python3

import sys
import numpy
import copy
from prettytable import PrettyTable
from time import time
from robot_control import RobotControl

numpy.set_printoptions(precision=4, linewidth=100)

# Necessary data for one test
class Environment:
    # Possible commands for moving the robot
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Change of position on matrix for every command
    DIRECTION = numpy.array([ [-1,0], [0,1], [1,0], [0,-1] ])

    # Create deterministic (when rng=None) or random environment.
    def __init__(self, rng=None, rows=None, columns=None, grayscale=None, destination=None):
        if rng:
            # Size of a matrix where our robot will be walk
            self.rows = rows
            self.columns = columns

            # Position of the station the robot has to reach
            self.destination = (rows//2, columns//2)

            # Number of steps the robot can make before it runs out of battery
            self.steps = 3*(self.rows+self.columns)

            # Matrix giving the grayscale of every position
            # This gives the probability that the sensor reads true
            self.grayscale = numpy.zeros((rows, columns))
            for i in range(rows):
                for j in range(columns):
                    self.grayscale[i,j] = rng.uniform(0,1)

        else: # Predetermined environment for testing your calculation of distribution of robot's location
            self.grayscale = grayscale
            self.rows, self.columns = grayscale.shape
            self.destination = destination

# Simulates one landing and returns True if the robot successfully reached the station from a given landing position (origin).
def single_landing(env, origin, rng):
    current = origin # Robot's current position
    control = RobotControl(copy.deepcopy(env))
    for step in range(env.steps+1):
        if (current == env.destination).all(): 
            return True
        sensor = rng.uniform(0,1) < env.grayscale[current[0],current[1]]
        command = control.get_command(sensor)
        assert command in [env.NORTH, env.EAST, env.SOUTH, env.WEST], f"Command must be an integer between 0 and 3 but the returned value is {command} of type ${type(command)}."
        current = current + env.DIRECTION[command]
        if current[0] < 0 or current[0] >= env.rows or current[1] < 0 or current[1] >= env.columns:
            return False

    return False

def run_tests(rows, columns, seed, landings, win_points):
    """
        Run the given number of landings on a map of given size.
        win_points is an array of numbers of robots needed to reach the station to get one point.
        Returns the number of successful landings and the number of received points.
    """
    print("Test contains", landings, "landings on an area of size", rows, "*", columns)
    rng = numpy.random.default_rng(seed)
    successful = 0
    for i in range(landings):
        env = Environment(rows=rows, columns=columns, rng=rng)
        origin = numpy.array([rng.integers(0, rows), rng.integers(0, columns)])
        if single_landing(env, origin, numpy.random.default_rng(rng.integers(numpy.iinfo(numpy.int64).max))):
            successful += 1
    points = sum(1 if successful >= p else 0 for p in win_points)
    print(landings, "robots landed and", successful, "successfully reached the destination. You will receive", points, "points assuming time and memory limits are satisfied.")
    return successful, points

def numpy_random_generation_test():
    """
        This function tests determinism and portability of random number generators in numpy.
        If these sets fails, contact your teacher and write your operation system, versions of python and numpy, etc.
        You can turn off these tests since this assignment works also with different random number generators, 
        but limits of successful landing may differ.
    """
    rng = numpy.random.default_rng(42)
    assert [rng.random() for _ in range(5)] == [0.7739560485559633, 0.4388784397520523, 0.8585979199113825, 0.6973680290593639, 0.09417734788764953]
    assert [rng.integers(1000000) for _ in range(5)] == [526478, 975622, 735752, 761139, 717477]
    assert [rng.beta(1, 3) for _ in range(5)] == [0.05014086883548152, 0.2817671069441921, 0.4516645021220816, 0.0672174548533563, 0.42291529387311344]
    assert [rng.random() for _ in range(5)] == [0.8931211213221977, 0.7783834970737619, 0.19463870785196757, 0.4667210037270342, 0.04380376578722878]
    rng = numpy.random.default_rng(rng.integers(numpy.iinfo(numpy.int64).max))
    assert [rng.random() for _ in range(5)] == [0.9722232784934238, 0.11981033678856667, 0.6507573893950737, 0.9434296766405612, 0.04959891689064433]

def main():
    # Parameters for all tests.
    tests = {
    #                rows, columns,seed, landings,       win_points, reference_time
        "first":  (     6,       7, 579,    10000, [4800,5200,6100],        12), # 2826, 4836, 5131, 5926
        "second": (    15,      13,   4,     2000, [1100,1180,1350],        15), #  587, 1115, 1198, 1277
        "third":  (    20,      21, 457,     1000, [ 540, 650, 750],        20), #  292,  549,  615,  708
        "fourth": (    30,      25, 457,      300, [ 180, 195, 230],        13), #   63,  183,  197,  217
        "fifth":  (    45,      30, 474,      200, [ 130, 140, 160],        20), #   37,  136,  139,  150
    }

    if len(sys.argv) == 1:
        results = PrettyTable(["Test name", "Rows", "Columns", "Landings", "Successful", "Points", "Reference time [s]", "Your time [s]"])
        for name in tests:
            print("Running test", name)
            rows, columns, seed, landings, win_points, time_limit = tests[name]
            start_time = time()
            successful, points = run_tests(rows, columns, seed, landings, win_points)
            running_time = time() - start_time
            print()
            results.add_row([name, rows, columns, landings, successful, points, time_limit, running_time])
        print(results)
    else:
        name = sys.argv[1]
        if name in tests:
            rows, columns, seed, landings, win_points, time_limit = tests[name]
            successful, points = run_tests(rows, columns, seed, landings, win_points)
            print("Successful landing", successful, "out of", landings, "and points limit are", win_points)
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 robot_test.py

To run a test NAME, run the command
$ python3 robot_test.py NAME
"""
if __name__ == "__main__":
    numpy_random_generation_test()
    main()
