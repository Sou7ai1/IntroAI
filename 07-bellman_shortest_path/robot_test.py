#!/usr/bin/env python3

import sys
sys.path.append("..")
import check_versions
import numpy
import copy
from prettytable import PrettyTable
from time import time
from robot_control import RobotControl

numpy.set_printoptions(precision=6, linewidth=200)

# Necessary data for one test
class Environment:
    # Possible commands for moving the robot
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Change of position on matrix for every command
    DIRECTION = numpy.array([ [-1,0], [0,1], [1,0], [0,-1] ])

    # Rotation relative to a given command
    FORWARD = 0
    RIGHT = 1
    BACKWARD = 2
    LEFT = 3

    # ROTATION[command,rotation] gives the actual movement for a given command and performed relative rotation.
    ROTATION = numpy.array([ [0,1,2,3], [1,2,3,0], [2,3,0,1], [3,0,1,2] ])

    # Create deterministic (when rng=None) or random environment.
    def __init__(self, rng=None, rows=None, columns=None, alpha=None, energy=None, rotation_probability=None, destination=None, forward_probability=None):
        if rng:
            # Size of a matrix where our robot will be walk
            self.rows = rows
            self.columns = columns

            # Position of the station
            self.destination = numpy.array([rows//2, columns//2])

            # The matrix of energy consumptions to enter each cell.
            self.energy = numpy.full((rows, columns), 100.)
            for i in range(1, rows-1):
                for j in range(1, columns-1):
                    self.energy[i,j] = rng.gamma(1.1, 5)
            self.energy[tuple(self.destination)] = 0.

            # Distribution of actual movement relative to the given command.
            self.forward_probability = rng.uniform(0.5, 0.8) if forward_probability == None else forward_probability
            self.backward_probability = rng.uniform(0.0, min(1.-self.forward_probability, 0.1))
            self.left_probability = rng.uniform(0.0, 1. - self.forward_probability - self.backward_probability)
            self.right_probability = 1. - self.forward_probability - self.backward_probability - self.left_probability
            self.rotation_probability = numpy.array([ self.forward_probability, self.right_probability, self.backward_probability, self.left_probability ])

        else:
            self.energy = energy
            self.rows, self.columns = energy.shape
            self.destination = destination
            self.forward_probability, self.right_probability, self.backward_probability, self.left_probability = self.rotation_probability = rotation_probability

    # Probability of successfully entrance to a given cell.
    def get_energy(self, position):
        return self.energy[tuple(position)]

    # Return position which the robot reaches when it make one step from origin position by a given command and rotation.
    # Both origin and returned positions are numpy arrays.
    def get_position_after_action(self, origin, command, rotation):
        return origin + self.DIRECTION[(command+rotation)%4]

# Simulates one landing and returns the energy consumed.
def single_landing(env, control, origin, rng):
    current = origin # Robot's current position
    consumed_energy = 0.
    while (current != env.destination).any(): # Repeat until robot reaches the station
        command = control.get_command(current)
        assert command in [env.NORTH, env.EAST, env.SOUTH, env.WEST], f"Command must be an integer between 0 and 3 but the returned value is {command} of type ${type(command)}."

        # Choose random movement relative to the given command
        rotation_random = rng.random()
        if rotation_random < env.forward_probability + env.backward_probability:
            if rotation_random < env.forward_probability:
                rotation = env.FORWARD
            else:
                rotation = env.BACKWARD
        elif rotation_random < env.forward_probability + env.backward_probability + env.left_probability:
            rotation = env.LEFT
        else:
            rotation = env.RIGHT

        # Determine new position and consumed energy
        next = env.get_position_after_action(current, command, rotation)
        consumed_energy += env.get_energy(next)
        # Move only if the new position is not on the first/last row/column
        if next[0] > 0 and next[0] < env.rows - 1 and next[1] > 0 and next[1] < env.columns - 1:
            current = next 

        # This just prevents the simulation to run too long.
        if consumed_energy > 100000:
            print("The robot consumed all energy and failed to reach to the base.")
            return consumed_energy

    return consumed_energy

def run_tests(rows, columns, forward_probability, alpha, seed, landings, win_points):
    """
        Run given number of games on a board of given size.
        In order to generate mines, their probability and seed generator is given.
        win_points is an array of total energies to get one point.
    """
    print("Test contains", landings, "landings on an area of size", rows, "*", columns)
    rng = numpy.random.default_rng(seed)
    origins = [ numpy.array([rng.integers(1, rows-1), rng.integers(1, columns-1)]) for _ in range(landings) ]
    env = Environment(rows=rows, columns=columns, forward_probability=forward_probability, alpha=alpha, rng=rng)
    control = RobotControl(copy.deepcopy(env))
    consumed_energy = 0.
    for origin in origins:
        consumed_energy += single_landing(env, control, origin, numpy.random.default_rng(rng.integers(numpy.iinfo(numpy.int64).max)))
    points = sum(1 if consumed_energy <= p else 0 for p in win_points)
    print(landings, "robots consumed", consumed_energy, "energy. You will receive", points, "points assuming time and memory limits are satisfied.")
    return consumed_energy, points

def numpy_random_generation_test():
    """
        This function tests determinism and portability of random number generators in numpy.
        If these sets fails, contact your teacher and write your operation system, versions of python and numpy, etc.
        You can turn off these tests since this assignment works also with different random number generators, 
        but limits may differ (significantly).
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
    #                rows, columns, forward_probability, alpha, seed, landings,  win_points, time
        "first":  (     7,       9,                 0.7,     3,  579,    1000, [26000, 18500],        0.1), # 31934,  25661,  18443
        "second": (    15,      13,                 0.5,    10,    4,    1000, [110000,57000],        0.2), # 153622, 100141, 56019
        "third":  (    20,      21,                 0.4,    50,  457,    1000, [300000,130000],       0.4), # 406475, 298057, 129172
        "fourth": (    45,      30,                 0.6,    50,  474,    1000, [160000,141000],       0.6), # 245968, 172079, 140976
        "fifth":  (    10,      70,                0.45,   100,  328,    1000, [240000,232500],         1), # 408149, 473656, 232420
        "sixth":  (   150,     100,                0.65,   150,  328,    1000, [350000,337100],         6), # 829318, 428780, 337070
    }

    if len(sys.argv) == 1:
        results = PrettyTable(["Test name", "Rows", "Columns", "Landings", "Consumed energy", "Points", "Reference time [s]", "Your time [s]"])
        for name in tests:
            print("Running test", name)
            rows, columns, forward_probability, alpha, seed, landings, win_points, reference_time = tests[name]
            start_time = time()
            successful, points = run_tests(rows, columns, forward_probability, alpha, seed, landings, win_points)
            running_time = time() - start_time
            print()
            results.add_row([name, rows, columns, landings, successful, points, reference_time, running_time])
        print(results)
    else:
        name = sys.argv[1]
        if name in tests:
            rows, columns, forward_probability, alpha, seed, landings, win_points, reference_time = tests[name]
            successful, points = run_tests(rows, columns, forward_probability, alpha, seed, landings, win_points)
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
