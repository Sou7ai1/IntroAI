import sys
import numpy
from numpy import array
from robot_test import Environment
from robot_control import RobotControl

# Run a single tests to verify the correctness of calculating the probabilities and policies
def evaluate(destination, sensor_readings, commands, grayscale, expected_position_distribution):
    rows, columns = grayscale.shape
    env = Environment(destination=array(destination), grayscale=grayscale)

    print("Testing grayscale:")
    print(grayscale)
    print("Destination:", destination)
    print("Sensor readings:", sensor_readings)
    print("Commands:", commands)

    robot = RobotControl(env)
    calculated_position_distribution = robot.calculate_position_distribution(sensor_readings, commands)

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

    return (incorrect_probabilities, max_probability_diff)

def main():
    # destination, sensor_readings, commands, grayscale, expected_position_distribution
    tests = {
        "first": ((1,1), [True], [],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.2273, 0.2045, 0.1818],
       [0.1591, 0.,     0.1136],
       [0.0682, 0.0455, 0.    ]])),

        "second": ((1,1), [False], [],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.0278, 0.0556],
       [0.0833, 0.,     0.1389],
       [0.1944, 0.2222, 0.2778]])),

        "third": ((1,1), [True,True], [0],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.5344, 0.,     0.3053],
       [0.1603, 0.,     0.    ],
       [0.,     0.,     0.    ]])),

        "fourth": ((1,1), [True,False], [1],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.1389, 0.25  ],
       [0.,     0.,     0.    ],
       [0.,     0.3333, 0.2778]])),

        "fifth": ((1,1), [False,False], [2],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.,     0.,     0.    ],
       [0.,     0.,     0.1235],
       [0.2593, 0.,     0.6173]])),

        "sixth": ((1,1), [False,True], [3],
array([[1. , .9 , .8 ],
       [.7 , .6 , .5 ],
       [.3 , .2 , .0 ]]),
array([[0.1389, 0.25,   0.    ],
       [0.,     0.,     0.    ],
       [0.3333, 0.2778, 0.    ]])),

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
       [0.,     0.0225, 0.2146, 0.1119]]))
}

    if len(sys.argv) == 1:
        sum_incorrect_probabilities = max_probability_diff = 0
        for name in tests:
            print("Running test", name)
            incorrect_probabilities, probability_diff = evaluate(*tests[name])
            sum_incorrect_probabilities += incorrect_probabilities
            max_probability_diff = max(max_probability_diff, probability_diff)
            print()
        success = sum_incorrect_probabilities == 0
        print("All tests passed." if success else "Some tests failed.", "The total number of positions with incorrect policies is", sum_incorrect_probabilities, "and the maximal of differences between the correct and your probabilities of survivability is", max_probability_diff)
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
