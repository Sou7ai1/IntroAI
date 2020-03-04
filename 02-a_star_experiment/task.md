## Goal

The goal of this assignment is to evaluate and compare your implementation of
heuristics for A-star algorithm experimentally.

You are given a test program (`informed_search_experiments`) which calls your
implementation from the previous assignment to perform the following
experiments. All experiments measure the number of visited vertices by A-star
algorithm.

- 2D-heuristics test: Consider the graph Grid2D (all edges are included) and
compare grid_2D_heuristic and grid_diagonal_2D_heuristic. How many vertices are
visited when A-star searches for the shortest path between vertices (0,0) and
(n,n)?
- 3D-heuristics test: Consider the graph Grid3D (all edges are included) and
compare grid_3D_heuristic, grid_face_diagonal_3D_heuristic and
grid_face_diagonal_3D_heuristic. How many vertices are visited when A-star
searches for the shortest path between vertices (0,0,0) and (n,n,n)?
- Density test: Consider a subgraph of Grid2D and grid_2D_heuristic where the
subgraph is obtained by keeping every edge of Grid2D with probability _p_. 10
experiments are done for every value of the probability _p_ and we count the number
visited vertices when searching for the shortest path between vertices (0,0)
and (0,100). Reported values are: the result of the first experiment, minimum,
average and maximum of 10 experiments.
- Repetition test: Repeat the previous test for _p_ = 0.9 many times and measure
the length of the shortest path and the number of visited vertices.

You should perform these experiments and write a report, which contains the following
plots of the measured data. 

- 2D and 3D heuristics tests: dependence of the number of visited vertices on _n_; 
one curve for each heuristics.
- Density test: dependence of the number of visited vertices on _p_;
one curve for each reported value.
- Repetition test: plot the length of the shortest path and the number of visited
vertices as x-y points.

The report should discuss the experimental results and try to explain the observed
behavior using theory from the lectures. (If you want, you can carry out further
experiments to gain better understanding of and include these in the report.
This is strictly optional.)

In 2D and 3D heuristics tests, you should be able to formally prove the
asymptotic number of visited vertices and estimate multiplicative constants.
In density and repetition tests, it is hard to formally explain the results, 
but try to write what you learn from these tests.

You should submit a PDF file with the report (and no source code).
You will get 1 temporary point upon submission if the file is syntantically correct;
proper points will be assigned later.

## Test program

The test program is given one argument which is the name of a test (Heuristic2D,
Heuristics3D, Density, Repetition). The output of the program contains one line
per experiment, except the first line which gives meaning of each column.

## Your implementation

Please include your implementation of the file heuristics.py from the previous
exercise. All heuristic functions will be augmented by the test program.

## Hints

The following tools can be useful for producing nice plots:
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [gnuplot](http://www.gnuplot.info/)

A quick checklist for plots:
- Is there a caption explaining what is plotted?
- Are the axes clearly labelled? Do they have value ranges and units?
- Have you mentioned that this axis has logarithmic scale? (Logarithmic graphs
  are more fitting in some cases, but you should tell.)
- Is it clear which curve means what?
- Is it clear what are the measured points and what is an interpolated
  curve between them?
- Are there any overlaps? (E.g., the most interesting part of the curve
  hidden underneath a label?)

In your discussion, please distinguish the following kinds of claims.
It should be always clear which is which:
- Experimental results (i.e., the raw data you obtained from the experiments)
- Theoretical facts (i.e., claims we have proved mathematically)
- Your hypotheses (e.g., when you claim that the graph looks like something is true,
  but you are not able to prove rigorously that it always holds)
