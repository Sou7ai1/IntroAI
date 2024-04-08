#!/usr/bin/env python3

import sys
import numpy
import copy
from prettytable import PrettyTable
sys.path.append("..")
import check_versions
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

        # Number of steps the robot can make before it runs out of battery
        self.steps = 3*(self.rows+self.columns)

# Simulates one landing and returns True if the robot successfully reached the station from a given landing position (origin).
def single_landing(env, origin, rng):
    current = origin # Robot's current position
    control = RobotControl(copy.deepcopy(env))
    for step in range(env.steps+1):
        if (current == env.destination).all(): 
            return (True,None,step)
        sensor = rng.uniform(0,1) < env.grayscale[current[0],current[1]]
        command = control.get_command(sensor)
        assert command in [env.NORTH, env.EAST, env.SOUTH, env.WEST], f"Command must be an integer between 0 and 3 but the returned value is {command} of type ${type(command)}."
        current = current + env.DIRECTION[command]
#        print("COMMAND: ", ["NORTH", "EAST", "SOUTH", "WEST"][command], current)
        if current[0] < 0 or current[0] >= env.rows or current[1] < 0 or current[1] >= env.columns:
            return (False,True,step)

    return (False,False,env.steps+1)

def run_tests(rows, columns, seed, landings, win_points):
    """
        Run the given number of landings on a map of given size.
        win_points is an array of numbers of robots needed to reach the station to get one point.
        Returns the number of successful landings and the number of received points.
    """
    print("Test contains", landings, "landings on an area of size", rows, "*", columns)
    rng = numpy.random.default_rng(seed)
    cnt_success = cnt_fall = cnt_battery = steps_success = steps_fall = total_steps = 0
    for i in range(landings):
        env = Environment(rows=rows, columns=columns, rng=rng)
        total_steps = env.steps
        origin = numpy.array([rng.integers(0, rows), rng.integers(0, columns)])
        success, fall, steps = single_landing(env, origin, numpy.random.default_rng(rng.integers(numpy.iinfo(numpy.int64).max)))
#        print("********************************************** END:", success, fall, steps, "**********************************************")
        if success:
            cnt_success += 1
            steps_success += steps
        elif fall:
            cnt_fall += 1
            steps_fall += steps
        else:
            cnt_battery += 1
    points = sum(1 if cnt_success >= p else 0 for p in win_points)
    print("Number of landings: {}, successful reaches of destination: {}, falls out of map: {}, runs out of battery: {}".format(landings, cnt_success, cnt_fall, cnt_battery))
    print("Average number of steps when reaching destination: {}, average number of steps when falling out of map: {}, maximal number of steps {}".format(steps_success/cnt_success, steps_fall/cnt_fall, total_steps))
    print("You will receive", points, "points assuming time and memory limits are satisfied.")
    return cnt_success, points

def main():
    # Parameters for all tests.
    tests = {
    #                rows, columns,seed, landings,       win_points
        "first":  (     6,       7, 579,     5000, [2380,2540,3000,3420]), # 1401, 2394, 2524, 3160, 3441
        "second": (    15,      13,   4,     2000, [1100,1180,1350,1600]), #  587, 1115, 1198, 1333, 1613
        "third":  (    20,      21, 457,     1000, [ 540, 650, 750, 860]), #  292,  549,  615,  701,  865
        "fourth": (    30,      25, 457,      300, [ 180, 195, 230, 275]), #   63,  183,  197,  219,  279
        "fifth":  (    45,      30, 474,      200, [ 130, 140, 160, 190]), #   37,  136,  139,  159,  191
    }

    if len(sys.argv) == 1:
        results = PrettyTable(["Test name", "Rows", "Columns", "Landings", "Successful", "Points", "Your time [s]", "Time limit on Recodex [s]"])
        for name in tests:
            print("Running test", name)
            rows, columns, seed, landings, win_points = tests[name]
            start_time = time()
            successful, points = run_tests(rows, columns, seed, landings, win_points)
            running_time = time() - start_time
            print()
            results.add_row([name, rows, columns, landings, successful, points, running_time, 300])
        print(results)
    else:
        name = sys.argv[1]
        if name in tests:
            rows, columns, seed, landings, win_points = tests[name]
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
    main()
