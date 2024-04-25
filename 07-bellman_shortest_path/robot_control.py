import numpy as np
import math
from heapq import heappush, heappop

class RobotControl:
    def __init__(self, environment):
        self.env = environment
        self.distance, self.policy = self.precompute_probability_policy()

    def get_distance(self):
        return self.distance

    def get_policy(self):
        return self.policy

    def get_command(self, current):
        return self.policy[tuple(current)]

    def euclidean_heuristic(self, pos, destination):
        return math.sqrt((pos[0] - destination[0])**2 + (pos[1] - destination[1])**2)

    def precompute_probability_policy(self):
        rows, cols = self.env.rows, self.env.columns
        policy = np.full((rows, cols), -1, dtype=int)
        distance = np.full((rows, cols), np.inf)
        destination = tuple(self.env.destination)
        heuristic_weight = 1.1

        heap = []
        start_cost = self.euclidean_heuristic(destination, destination)
        heappush(heap, (start_cost, 0, destination))
        distance[destination] = 0

        while heap:
            _, current_dist, current_pos = heappop(heap)
            if current_dist > distance[current_pos]:
                continue

            for direction in range(4):
                neighbor = self.env.get_position_in_direction(current_pos, direction)
                if self.env.get_energy(neighbor) > 0:
                    new_dist = current_dist + self.env.get_energy(neighbor)
                    if new_dist < distance[neighbor]:
                        distance[neighbor] = new_dist
                        policy[neighbor] = (direction + 2) % 4
                        estimated_cost = new_dist + heuristic_weight * self.euclidean_heuristic(neighbor, destination)
                        heappush(heap, (estimated_cost, new_dist, neighbor))

        return distance, policy
