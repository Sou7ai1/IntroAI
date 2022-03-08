#!/usr/bin/env python3

import networkx
import sys
from time import time
from prettytable import PrettyTable
from total_sat import total_coloring

def verify_total_coloring(graph_original, graph_student, expected_colors, colors):
    if not isinstance(colors, int):
        return (False, f"Number of colors '{colors}' is not an integer.")

    for u in graph_original.nodes():
        if not "color" in graph_student.nodes[u]:
            return (False, f"Vertex {u} has no assigned color.")
        c = graph_student.nodes[u]["color"]
        if not isinstance(c, int):
            return (False, f"Color '{c}' of a vertex {u} is not an integer.")
        if not 0 <= c < colors:
            return (False, f"Color '{c}' of a vertex {u} is outside the expected range from 0 to {colors-1}.")

    for u,v in graph_original.edges():
        if not "color" in graph_student.edges[u,v]:
            return (False, f"Edge {u,v} has no assigned color.")
        c = graph_student.edges[u,v]["color"]
        if not isinstance(c, int):
            return (False, f"Color '{c}' of an edge {u,v} is not an integer.")
        if not 0 <= c < colors:
            return (False, f"Color '{c}' of an edge {u,v} is outside the expected range from 0 to {colors-1}.")

    for u,v in graph_original.edges():
        if graph_student.nodes[u]["color"] == graph_student.nodes[v]["color"]:
            c = graph_student.nodes[v]["color"]
            return (False, f"Vertices {u} and {v} have the same color {c}.")
        if graph_student.nodes[u]["color"] == graph_student.edges[u,v]["color"]:
            c = graph_student.nodes[u]["color"]
            return (False, f"Vertex {u} and edge {u,v} have the same color {c}.")
        if graph_student.nodes[v]["color"] == graph_student.edges[u,v]["color"]:
            c = graph_student.nodes[v]["color"]
            return (False, f"Vertex {v} and edge {u,v} have the same color {c}.")

    for u in graph_original.nodes():
        for v in graph_original[u]:
            for w in graph_original[u]:
                if v != w and graph_student.edges[u,v]["color"] == graph_student.edges[u,w]["color"]:
                    c = graph_student.edges[u,v]["color"]
                    return (False, f"Edges {u,v} and {u,w} have the same color {c}.")

    if colors > expected_colors:
        return (False, f"Your coloring uses {colors} colors but {expected_colors} is sufficient.")
    if colors < expected_colors:
        # This case is expected not to happend. This most likely means incorrect setting of tests.
        return (False, f"Your coloring uses smaller number of colors than expected which should not be possible.")

    return (True, "Correct")

def total_coloring_test(name, graph_original, expected_colors):
    print("Tested graph:", name)
    graph_student = graph_original.copy()
    colors = total_coloring(graph_student)
    return verify_total_coloring(graph_original, graph_student, expected_colors, colors)

def total_coloring_dataset(dataset):
    """ Run a set of tests """
    for d in dataset:
        status, msg = total_coloring_test(*d)
        if not status:
            return (status, msg)
    return (True, "Correct")

def main():
    small_graphs = [
        ("Complete graph on 3 vertices", networkx.complete_graph(3), 3),
        ("Cycle of length 5", networkx.cycle_graph(5), 4),
        ("Star graph on 5 vertices", networkx.star_graph(4), 5),
        ("Petersen graph", networkx.petersen_graph(), 4),
        ("Chvatal graph", networkx.chvatal_graph(), 5)
    ]
    large_graphs = [
        ("Complete graph on 7 vertices", networkx.complete_graph(7), 7),
        ("Cycle of length 14", networkx.cycle_graph(14), 4),
        ("Star graph on 200 vertices", networkx.star_graph(200), 201),
        ("Complete bipartite graph on 4+4 vertices", networkx.complete_multipartite_graph(4,4), 6),
        ("Hypercube of dimension 3", networkx.hypercube_graph(3), 4)
    ]

    tests = {
            "small": (small_graphs, 5, 0.01),
            "large": (large_graphs, 5, 3),
    }

    if len(sys.argv) == 1:
        results = PrettyTable(["Test name", "Points", "Reference time [s]", "Your time [s]", "Evaluation"])
        for name in tests:
            print("Running test", name)
            dataset, points, time_limit = tests[name]
            start_time = time()
            status, msg = total_coloring_dataset(dataset)
            running_time = time() - start_time
            print(msg)
            print()
            results.add_row([name, points, time_limit, running_time, msg])
        print(results)
    else:
        name = sys.argv[1]
        if name in tests:
            dataset, points, time_limit = tests[name]
            status, msg = total_coloring_dataset(dataset)
            print(msg)
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 total_tests.py

To run a test NAME, run the command
$ python3 total_tests.py NAME
"""
if __name__ == "__main__":
    main()
