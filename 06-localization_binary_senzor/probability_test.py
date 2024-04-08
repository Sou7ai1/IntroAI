import sys
import numpy
from numpy import array
from robot_test import Environment
from robot_control import RobotControl

# Run a single tests to verify the correctness of calculating the probabilities and policies
def evaluate(destination, sensor_readings, commands, grayscale, expected_position_distribution, expected_fall_probabilities):
    rows, columns = grayscale.shape
    env = Environment(destination=array(destination), grayscale=grayscale)

    print("Testing grayscale:")
    print(grayscale)
    print("Destination:", destination)
    print("Sensor readings:", sensor_readings)
    print("Commands:", commands)

    robot = RobotControl(env)
    calculated_position_distribution, calculated_fall_probabilities = robot.calculate_position_distribution(sensor_readings, commands)

    print("Expected position distribution:")
    print(expected_position_distribution)
    print("Your distribution:")
    print(calculated_position_distribution)

    incorrect_probabilities = 0
    max_probability_diff = 0.
    for i in range(rows):
        for j in range(columns):
            max_probability_diff = max(max_probability_diff, abs(expected_position_distribution[i,j] - calculated_position_distribution[i,j]))
            if abs(expected_position_distribution[i,j] - calculated_position_distribution[i,j]) > 0.001:
                incorrect_probabilities += 1

    print("The number of positions with incorrect probability is", incorrect_probabilities)
    print("The maximal of differences between the correct and your probabilities is", max_probability_diff)

    print("Expected probability of falling out of map when moving north is", expected_fall_probabilities[env.NORTH], "and your calculation is", calculated_fall_probabilities[env.NORTH])
    print("Expected probability of falling out of map when moving east is", expected_fall_probabilities[env.EAST], "and your calculation is", calculated_fall_probabilities[env.EAST])
    print("Expected probability of falling out of map when moving south is", expected_fall_probabilities[env.SOUTH], "and your calculation is", calculated_fall_probabilities[env.SOUTH])
    print("Expected probability of falling out of map when moving west is", expected_fall_probabilities[env.WEST], "and your calculation is", calculated_fall_probabilities[env.WEST])
    max_fall_diff = max(abs(expected_fall_probabilities[dir] - calculated_fall_probabilities[dir]) for dir in range(4))

    return (incorrect_probabilities, max_probability_diff, max_fall_diff)

def main():
    # destination, sensor_readings, commands, grayscale, expected_position_distribution
    tests = {
        "first": ((1,1), [True], [],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.2273, 0.2045, 0.1818],
       [0.1591, 0.,     0.1136],
       [0.0682, 0.0455, 0.    ]]),
[0.6136363636363635, 0.29545454545454547, 0.11363636363636363, 0.45454545454545453]),

        "second": ((1,1), [False], [],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.0278, 0.0556],
       [0.0833, 0.,     0.1389],
       [0.1944, 0.2222, 0.2778]]),
[0.08333333333333331, 0.47222222222222215, 0.6944444444444444, 0.27777777777777773]),

        "third": ((1,1), [True,True], [0],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.5344, 0.,     0.3053],
       [0.1603, 0.,     0.    ],
       [0.,     0.,     0.    ]]),
[0.8396946564885495, 0.3053435114503817, 0.0, 0.6946564885496183]),

        "fourth": ((1,1), [True,False], [1],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.1389, 0.25  ],
       [0.,     0.,     0.    ],
       [0.,     0.3333, 0.2778]]),
[0.38888888888888884, 0.5277777777777778, 0.6111111111111113, 0.0]),

        "fifth": ((1,1), [False,False], [2],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.,     0.    ],
       [0.,     0.,     0.1235],
       [0.2593, 0.,     0.6173]]),
[0.0, 0.7407407407407407, 0.8765432098765432, 0.2592592592592593]),

        "sixth": ((1,1), [False,True], [3],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.1389, 0.25,   0.    ],
       [0.,     0.,     0.    ],
       [0.3333, 0.2778, 0.    ]]),
[0.38888888888888884, 0.0, 0.6111111111111113, 0.4722222222222223]),

        "seventh": ((1,2), [False,True,False,True], [0,1,2],
array([[.24 , .94 , .45, .348 ],
       [.74 , .61 , .56, .2148 ],
       [.457 , .472 , .124, .044 ],
       [.245 , .457 , .453, .548 ],
       [.45 , .14 , .455, .457 ]]),
array([[0.,     0.,     0.,     0.    ],
       [0.,     0.005,  0.,     0.    ],
       [0.,     0.1623, 0.,     0.    ],
       [0.,     0.1827, 0.2231, 0.078 ],
       [0.,     0.0225, 0.2146, 0.1119]]),
[0.0, 0.1898443121626573, 0.3489613361431143, 0.0])
}

    if len(sys.argv) == 1:
        sum_incorrect_probabilities = max_probability_diff = max_fall_diff = 0
        for name in tests:
            print("Running test", name)
            incorrect_probabilities, probability_diff, fall_diff = evaluate(*tests[name])
            sum_incorrect_probabilities += incorrect_probabilities
            max_probability_diff = max(max_probability_diff, probability_diff)
            max_fall_diff = max(max_fall_diff, fall_diff)
            print()
        success = sum_incorrect_probabilities == 0 and max_fall_diff < 0.001
        print("All tests passed." if success else "Some tests failed.", "The total number of positions with incorrect probabilities is", sum_incorrect_probabilities, "and the maximal of differences between the correct and your probabilities of survivability is", max_probability_diff, ". Maximal difference between expected and calculated falling probabilities is", max_fall_diff)
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
