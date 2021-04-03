#!/usr/bin/env python3

import logging
import sys
import os
import time

import search
import pyperplan
from pddl.parser import Parser

# Source: https://github.com/aibasel/pyperplan, modified to testing purposes.
def pyperplan_solver(problem_file, domain_file):
    search_algorithm = search.breadth_first_search
    heuristic = None

    parser = Parser(domain_file, problem_file)
    logging.info("Parsing Domain {}".format(domain_file))
    domain = parser.parse_domain()
    logging.info("Parsing Problem {}".format(problem_file))
    problem = parser.parse_problem(domain)
    logging.debug(domain)
    logging.info("{} Predicates parsed".format(len(domain.predicates)))
    logging.info("{} Actions parsed".format(len(domain.actions)))
    logging.info("{} Objects parsed".format(len(problem.objects)))
    logging.info("{} Constants parsed".format(len(domain.constants)))

    task = pyperplan._ground(problem)
    search_start_time = time.process_time()
    solution = pyperplan._search(task, search_algorithm, heuristic)
    logging.info("Search time: {:.2}".format(time.process_time() - search_start_time))

    if solution is None:
        logging.warning("No solution could be found")
        return problem, None
    else:
        solution_file = problem_file + ".soln"
        logging.info("Plan length: %s" % len(solution))
        return problem, solution

problems = {
    "load": ("task_load.pddl", True),
    "unload": ("task_unload.pddl", True),
    "move": ("task_move.pddl", True),
    "load_move_unload": ("task_load_move_unload.pddl", True),
    "first_move": ("task_first_move.pddl", True),
    "teleport": ("task_teleport.pddl", False),
    "three_boxes": ("task_three_boxes.pddl", True),
    "split_box": ("task_split_box.pddl", False),
    "split_car": ("task_split_car.pddl", False),
    "three_cars": ("task_three_cars.pddl", True),
}

def verify_plan(problem, solution):
    boxes = dict()
    cars = dict()

    for state in problem.initial_state:
        if state.name == "at":
            object = state.signature[0][0]
            place = state.signature[1][0]
            assert(object[:-1] in ["car", "box"] and place[:-1] in ["car", "place"])
            if object[:-1] == "box":
                assert(place[:-1] in ["car", "place"])
                logging.info("Initial state: {} is located in {}".format(object, place))
                boxes[object] = place
            else:
                assert(place[:-1] == "place")
                logging.info("Initial state: {} is located at {}".format(object, place))
                cars[object] = place

    for action in solution:
        logging.info("Action: {}".format(action.name))
        action = action.name[1:-1].split()
        assert(all(a[:-1] in ["car", "box", "place"] for a in action[1:]))

        if action[0] == "load":
            _, box, car, place = action
            if not box in boxes:
                logging.error("Cannot load {} in a car".format(box))
                return False
            if not car in cars:
                logging.error("{} is not a car".format(car))
                return False
            if not place == cars[car]:
                logging.error("Car {} is not located at {}".format(car, place))
                return False
            if not place == boxes[box]:
                logging.error("Box {} is already loaded".format(box))
                return False
            if car in boxes.values():
                logging.error("Car {} is full".format(car))
                return False
            boxes[box] = car
        elif action[0] == "unload":
            _, box, car, place = action
            if not box in boxes:
                logging.error("Cannot load {} in a car".format(box))
                return False
            if not car in cars:
                logging.error("{} is not a car".format(car))
                return False
            if not place == cars[car]:
                logging.error("Car {} is not located at {}".format(car, place))
                return False
            if not car == boxes[box]:
                logging.error("Box {} is not loaded in car {}".format(box, car))
                return False
            boxes[box] = place
        elif action[0] == "move":
            _, car, src, dst = action
            if not car in cars:
                logging.error("{} is not a car".format(car))
                return False
            if not src == cars[car]:
                logging.error("Car {} is not located at {}".format(car, place))
                return False
            if not dst[:-1] == "place":
                logging.error("{} is not a place}".format(dst))
                return False
            cars[car] = dst
        else:
            logging.error("Invalid action {}".format(action[0]))
            return False

    for goal in problem.goal:
        assert(goal.name == "at")
        object = goal.signature[0][0]
        place = goal.signature[1][0]
        assert(object[:-1] in ["car", "box"] and place[:-1] in ["car", "place"])
        if object[:-1] == "box":
            assert(place[:-1] in ["car", "place"])
            logging.info("Goal: Box {} is expected to be at {}".format(object, place))
            if not boxes[object] == place:
                logging.error("Box {} is located at {}".format(object, boxes[object]))
                return False
        else:
            assert(place[:-1] == "place")
            logging.info("Goal: Car {} is expected to be at {}".format(object, place))
            if not cars[object] == place:
                logging.error("Car {} is located at {}".format(object, cars[object]))
                return False

    return True

def run_problem(domain_file, name):
    problem_file, feasible = problems[name]
    problem, solution = pyperplan_solver(problem_file, domain_file)
    if feasible:
        if not solution:
            logging.error("Problem {} is feasible".format(name))
            return False
        elif verify_plan(problem, solution):
            logging.info("Passed.")
            return True
    else:
        if not feasible:
            logging.info("Passed.")
            return True
        else:
            logging.error("Problem {} is infeasible".format(name))
            return False

def usage(str):
    print(str)
    print("Usage: transport_test domain_file [ problem ]")
    exit(1)

def parse_args():
    if len(sys.argv) <= 1:
        usage("At least one argument expected.")
    if len(sys.argv) >= 4:
        usage("At most two arguments expected.")
    domain_file = sys.argv[1]
    if not os.path.isfile(domain_file):
        usage(domain_file + " is not a file.")
    if len(sys.argv) == 2:
        return domain_file, None
    problem = sys.argv[2]
    if not problem in problems:
        usage("Unknown test: " + problem)
    return domain_file, problem

def main():
    domain_file, problem = parse_args()

    logging.basicConfig(
        level=getattr(logging, "INFO"),
        format="%(asctime)s %(levelname)-8s %(message)s",
        stream=sys.stdout,
    )

    if problem:
        run_problem(domain_file, problem)
        return

    points = 0
    for problem in problems:
        print("=====================================   TEST  ", problem, "    ================================")
        if run_problem(domain_file, problem):
            points += 1

    print("Number of points:", points)
    print(points/10)

if __name__ == "__main__":
    main()
