import numpy, scipy, networkx # You can use everything from these libraries if you find them useful.

"""
    TODO: Improve the strategy controlling the robot.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * RobotControl.__init__ is called in for every environment (test).
        * RobotControl.get_command is called to obtain command for movement on a given position.
    Furthermore, calculate_position_distribution is used by tests in the file probability_test.py.
"""

class RobotControl:
    def __init__(self, environment):
        self.env = environment

        # Size of the map
        self.rows = environment.rows
        self.columns = environment.columns

        # The position of the station
        self.destination = environment.destination

        # Map, i.e. a matrix containing color (on grayscale) for every cell
        self.grayscale = environment.grayscale

        # Step counter 
        self.remaining_steps = self.total_steps = environment.steps

        # The probability distribution of landing on each cell
        self.position_dist = numpy.full((self.rows, self.columns), 1/(self.rows * self.columns))

        # This is needed only for a trivial control
        self.spiral_direction = self.env.NORTH
        self.spiral_remains = self.spiral_steps = 1

        self.grayscale_complement = 1 - environment.grayscale

    # Returns command for movement.
    # sensor_reading - True if the robot's sensor reads black on the current position
    def get_command(self, sensor_reading):
        self.remaining_steps -= 1
        return self.get_command_using_spiral()
        
    # This is a trivial control in which the robot moves on a spiral.
    # Only for illustrative purposes.
    def get_command_using_spiral(self):
        if self.spiral_remains == 0:
            self.spiral_direction = (self.spiral_direction + 1) % 4
            if self.spiral_direction % 2 == 0:
                self.spiral_steps += 1
            self.spiral_remains = self.spiral_steps
        self.spiral_remains -= 1
        return self.spiral_direction

    # Calculate the probability distribution of robot's position after k steps
    # sensor_readings - a binary array of k+1 sensor readings
    # commands - an array of k robots commands (directions of movements)
    # The robots lands in the environment self.env, sensor reads sensor_readings[0], makes movement commands[0], sensor reads sensor_readings[1], ..., sensor reads sensor_readings[k+1]
    # Determine the probability distribution after these operations.
    # Returns a pair of
    # - a matrix of probability distribution
    # - an array of four probabilities of falling out of map when the robot is moved in corresponding directions 
    def calculate_position_distribution(self, sensor_readings, commands):
        # return (numpy.zeros((self.rows, self.columns)), [0]*4)
        # This is a recommended approach to calculate the probability distribution of robot's position
        for i in range(len(commands)):
            self.update_position_by_sensor_reading(sensor_readings[i])
            self.update_position_by_command(commands[i])
        self.update_position_by_sensor_reading(sensor_readings[-1])
        self.normalize_position_distribution()
        fall = self.get_probabilities_fall()
        return (self.position_dist, fall)
