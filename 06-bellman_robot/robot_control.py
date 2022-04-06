import numpy, scipy, networkx # You can use everything from these libraries if you find them usefull.
import scipy.sparse as sparse # Calling scipy.sparse.csc_matrix does not work on Recodex, so call sparse.csc_matrix(...) instead
import scipy.sparse.linalg as linalg # Also, call linalg.spsolve

"""
    TODO: Improve the strategy controlling the robot.
    A recommended approach is implementing the function RobotControl.precompute_probability_policy.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * RobotControl.__init__ is called in for every environment (test).
        * RobotControl.get_command is called to obtain command for movement on a given position.
    Furthermore, get_survivability and get_policy is used by tests in the file probability_test.py.
"""

class RobotControl:
    def __init__(self, environment):
        self.env = environment
        self.survivability,self.policy = self.precompute_probability_policy()

    # Returns a matrix of maximal probabilities of reaching the station from every cell
    def get_survivability(self):
        return self.survivability

    # Returns a matrix of commands for every cell
    def get_policy(self):
        return self.policy

    # Returns command for movement from the current position.
    # This function is called quite a lot of times, so it is recommended to avoid any heavy computation here.
    def get_command(self, current):
        return self.policy[tuple(current)]

    # Place all your precomputation here.
    def precompute_probability_policy(self):
        return self.precompute_probability_policy_trivial()

    # Returns a trivial control strategy which just heads directly toward the station ignoring all dangers and movement imperfectness
    def precompute_probability_policy_trivial(self):
        env = self.env
        survivability = numpy.zeros((env.rows, env.columns)) # No probability is computed
        policy = numpy.zeros((env.rows, env.columns), dtype=int)
        for i in range(env.rows):
            for j in range(env.columns):
                if i > env.destination[0]:
                    policy[i,j] = env.NORTH
                elif i < env.destination[0]:
                    policy[i,j] = env.SOUTH
                elif j < env.destination[1]:
                    policy[i,j] = env.EAST
                elif j > env.destination[1]:
                    policy[i,j] = env.WEST
        return survivability, policy

