#!/usr/bin/env python3

import networkx
import sys
import total_sat as student_solver

def verify_total_coloring(graph_original, graph_student, expected_colors, colors):
    if not isinstance(colors, int):
        return f"Number of colors '{colors}' is not an integer."

    for u in graph_original.nodes():
        if not "color" in graph_student.nodes[u]:
            return f"Vertex {u} has no assigned color."
        c = graph_student.nodes[u]["color"]
        if not isinstance(c, int):
            return f"Color '{c}' of a vertex {u} is not an integer."
        if not 0 <= c < colors:
            return f"Color '{c}' of a vertex {u} is outside the expected range from 0 to {colors-1}."

    for u,v in graph_original.edges():
        if not "color" in graph_student.edges[u,v]:
            return f"Edge {u,v} has no assigned color."
        c = graph_student.edges[u,v]["color"]
        if not isinstance(c, int):
            return f"Color '{c}' of an edge {u,v} is not an integer."
        if not 0 <= c < colors:
            return f"Color '{c}' of an edge {u,v} is outside the expected range from 0 to {colors-1}."

    for u,v in graph_original.edges():
        if graph_student.nodes[u]["color"] == graph_student.nodes[v]["color"]:
            c = graph_student.nodes[v]["color"]
            return f"Vertices {u} and {v} have the same color {c}."
        if graph_student.nodes[u]["color"] == graph_student.edges[u,v]["color"]:
            c = graph_student.nodes[u]["color"]
            return f"Vertex {u} and edge {u,v} have the same color {c}."
        if graph_student.nodes[v]["color"] == graph_student.edges[u,v]["color"]:
            c = graph_student.nodes[v]["color"]
            return f"Vertex {v} and edge {u,v} have the same color {c}."

    for u in graph_original.nodes():
        for v in graph_original[u]:
            for w in graph_original[u]:
                if v != w and graph_student.edges[u,v]["color"] == graph_student.edges[u,w]["color"]:
                    c = graph_student.edges[u,v]["color"]
                    return f"Edges {u,v} and {u,w} have the same color {c}."

    if colors != expected_colors:
        return f"The number of colors {colors} differs from the minimal {expected_colors}."

def total_coloring_test(name, graph_original, expected_colors):
    print("Test: ", name)
    graph_student = graph_original.copy()
    colors = student_solver.total_coloring(graph_student)
    result = verify_total_coloring(graph_original, graph_student, expected_colors, colors)
    if result:
        print("Failed: ", result)
        return False
    else:
        return True

def small_graph_tests():
    if not total_coloring_test("Complete graph on 3 vertices", networkx.complete_graph(3), 3):
        return False
    if not total_coloring_test("Cycle of length 5", networkx.cycle_graph(5), 4):
        return False
    if not total_coloring_test("Star graph on 5 vertices", networkx.star_graph(4), 5):
        return False
    if not total_coloring_test("Petersen graph", networkx.petersen_graph(), 4):
        return False
    if not total_coloring_test("Chvatal graph", networkx.chvatal_graph(), 5):
        return False
    return True

def large_graph_tests():
    if not total_coloring_test("Complete graph on 7 vertices", networkx.complete_graph(7), 7):
        return False
    if not total_coloring_test("Cycle of length 100", networkx.cycle_graph(100), 4):
        return False
    if not total_coloring_test("Star graph on 200 vertices", networkx.star_graph(200), 201):
        return False
    if not total_coloring_test("Complete bipartite graph on 4+4 vertices", networkx.complete_multipartite_graph(4,4), 6):
        return False
    if not total_coloring_test("Hypercube of dimension 5", networkx.hypercube_graph(5), 6):
        return False
    return True

if __name__ == "__main__":
    tests = {
            "small": small_graph_tests,
            "large": large_graph_tests,
    }
    if len(sys.argv) == 1:
        for name in tests:
            print("Running test", name)
            if tests[name]():
                print("Passed.")
            else:
                break
    else:
        name = sys.argv[1]
        if name in tests:
            if tests[name]():
                print("Tests passed.")
        else:
            print("Unknown test", name)
