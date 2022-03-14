#!/usr/bin/env python3

import logging
import sys
import os
import time
from time import time
from prettytable import PrettyTable
from pyperplan import search, planner
from pyperplan.pddl.parser import Parser

# Source: https://github.com/aibasel/pyperplan, modified for testing purposes.
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

    task = planner._ground(problem)
    solution = planner._search(task, search_algorithm, heuristic)

    if solution is None:
        logging.warning("No solution could be found")
        return problem, None
    else:
        solution_file = problem_file + ".soln"
        logging.info("Plan length: %s" % len(solution))
        return problem, solution

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
                return (False, "Cannot load {} in a car".format(box))
            if not car in cars:
                return (False, "{} is not a car".format(car))
            if not place == cars[car]:
                return (False, "Car {} is not located at {}".format(car, place))
            if not place == boxes[box]:
                return (False, "Box {} is already loaded".format(box))
            if car in boxes.values():
                return (False, "Car {} is full".format(car))
            boxes[box] = car
        elif action[0] == "unload":
            _, box, car, place = action
            if not box in boxes:
                return (False, "Cannot load {} in a car".format(box))
            if not car in cars:
                return (False, "{} is not a car".format(car))
            if not place == cars[car]:
                return (False, "Car {} is not located at {}".format(car, place))
            if not car == boxes[box]:
                return (False, "Box {} is not loaded in car {}".format(box, car))
            boxes[box] = place
        elif action[0] == "move":
            _, car, src, dst = action
            if not car in cars:
                return (False, "{} is not a car".format(car))
            if not src == cars[car]:
                return (False, "Car {} is not located at {}".format(car, place))
            if not dst[:-1] == "place":
                return (False, "{} is not a place}".format(dst))
            cars[car] = dst
        else:
            return (False, "Invalid action {}".format(action[0]))

    for goal in problem.goal:
        assert(goal.name == "at")
        object = goal.signature[0][0]
        place = goal.signature[1][0]
        assert(object[:-1] in ["car", "box"] and place[:-1] in ["car", "place"])
        if object[:-1] == "box":
            assert(place[:-1] in ["car", "place"])
            logging.info("Goal: Box {} is expected to be at {}".format(object, place))
            if not boxes[object] == place:
                return (False, "Box {} is located at {}".format(object, boxes[object]))
        else:
            assert(place[:-1] == "place")
            logging.info("Goal: Car {} is expected to be at {}".format(object, place))
            if not cars[object] == place:
                return (False, "Car {} is located at {}".format(object, cars[object]))

    return (True, "Correct")

def run_problem(domain_file, name, problem_file, feasible):
    problem, solution = pyperplan_solver(problem_file, domain_file)
    if not solution:
        if feasible:
            return (False, "Problem {} is feasible".format(name))
        else:
            return (True, "Correct")

    status,msg = verify_plan(problem, solution)
    if status and not feasible:
        # This should not happend
        return (False, "Problem {} should be infeasible".format(name))

    return (status, msg)

def pddl_test(domain_file, name, problem_file, feasible):
    (status,msg) = run_problem(domain_file, name, problem_file, feasible)
    if status:
        logging.info(msg)
    else:
        logging.error(msg)
    return (status,msg)

def usage(str):
    print(str)
    print("Usage: transport_test [ domain_file [ problem ] ]")
    exit(1)

def parse_args():
    if len(sys.argv) <= 1:
        return "domain.pddl", None
    if len(sys.argv) >= 4:
        usage("At most two arguments expected.")
    domain_file = sys.argv[1]
    if not os.path.isfile(domain_file):
        usage(domain_file + " is not a file.")
    if len(sys.argv) == 2:
        return domain_file, None
    problem = sys.argv[2]
    return domain_file, problem

def main():
    tests = {
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

    domain_file, problem = parse_args()

    logging.basicConfig(
        level=getattr(logging, "INFO"),
        format="%(asctime)s %(levelname)-8s %(message)s",
        stream=sys.stdout,
    )

    if not problem:
        results = PrettyTable(["Test name", "Points", "Reference time [s]", "Your time [s]", "Evaluation"])
        for problem in tests:
            print("=====================================   TEST  ", problem, "    ================================")
            problem_file, feasible = tests[problem]
            start_time = time()
            status, msg = pddl_test(domain_file, problem, problem_file, feasible)
            running_time = time() - start_time
            print()
            results.add_row([problem, 1, "< 0.1", running_time, msg])
        print(results)
    else:
        if problem in tests:
            problem_file, feasible = tests[problem]
            status, msg = pddl_test(domain_file, problem, problem_file, feasible)
        else:
            print("Unknown test", problem)

"""
To run all tests, run the command
$ python3 transport_tests.py

To run a test NAME, run the command
$ python3 transport_tests.py NAME
"""
if __name__ == "__main__":
    main()
