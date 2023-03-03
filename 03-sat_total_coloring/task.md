Total coloring (see e.g. https://en.wikipedia.org/wiki/Total_coloring) of a graph is the coloring of vertices and edges such that
* vertices connected by an edge have different colors,
* edges sharing a common vertex have different colors and
* edges and their end-vertices have different colors.
The total chromatic number of a graph is the minimum number of colors required for total coloring of the graph. Write a program which finds the total chromatic number using the Satisfiability of boolean formulas (SAT). Implement function total_coloring in the file total_sat.py and upload only this file to ReCodex.

This task can be solved using many methods (e.g. CSP, Linear Programming and backtracking), but the goal of this assignment is to practice using SAT solvers on a simple problem. Therefore, you are expected to use the library **python-sat** (https://pypi.org/project/python-sat/). A graph is given using the library networkx (https://pypi.org/project/networkx/), so a part of the assignment is reading the documentation of mentioned libraries.
