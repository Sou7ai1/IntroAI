After the shutdown of space stations Mir and ISS, people started colonizing the Mars.
The first station is already built but it is not self-sustainable yet, so it requires regular shipments of supplies.
Since navigation of rockets to Mars is not working properly, rockets land (crash to be more precise) somewhere in the vicinity of the station
and supplies need to be carried by an autonomous robot from the crash site to the station.
Our task is to write a program that drives the robot.

For simplicity of the task, the vicinity of the station is split into cells forming a two-dimensional grid.
Finding the shortest path in the two-dimension grid would be simple but there are two major problems.

1. The robot accepts commands NORTH, SOUTH, WEST, and EAST which move the robot by one cell in the given direction.
However, unsuccessful landing caused some damage to the robot's engines so its movement is imperfect.
After initial diagnosis, the robot estimates probabilities p_forward, p_backward, p_left, and p_right (summing up to one) which give the distribution of actual movement relative to the given direction.
For example; when the command is EAST, then the robot moves to the east with probability p_forward, south with probability p_right, west with probability p_backward, and north with probability p_left.

2. The environment of Mars is dangerous and there are many obstacles.
During previous explorations, the probability of losing the robot (fatal failure) was estimated for every cell.
Note that the probability of losing the robot remains the same even for repetitive entrances into the same cell (so this is not a variant of the Minesweeper task).

Luckily, the robot's location system works perfectly, so the robot knows its position after every landing and after every movement.

Our task is to write a program maximizing the number of robots successfully reaching the station.
File robot_control.py contains a trivial control algorithm and your task is to improve it.
You can modify this file as you like but keep the interface used by file robot_test.py.
Only the file robot_control.py is expected to be submitted.

You can use and combine every knowledge from our course, i.e. informed search, logic, and probabilistic reasoning.
Especially, chapters 17.2 and 17.3 from the book Artificial Intelligence: A modern approach (3rd edition) could be useful.
However, you are expected to explain your approach, so write comments in your code.
Teachers will reduce the number of points for unclear code.

Technical remarks:
* Probability of failure is given as a matrix which also determines the coordination system.
Therefore, going south increases the row index, and going east increases the column index.
Note that the first and the last row and column of the matrix are outside the explored areas, so the probability of failure there is 1.
As a consequence, this prevents the robot from moving outside the matrix.

* Every test contains multiple landings in the vicinity of one station, so probabilities of failure are unchanged.
It may be surprising that the distribution of actual movements (p_forward, p_backward, p_left, and p_right) is the same after every landing.
Therefore, it is recommended to precompute commands for every cell in the initialization of each test to make your program reasonably fast.

Hints:
* Mathematically speaking, the problem is stationary, i.e. the probability of reaching the station from a given cell does not depend on the past (where it landed or how the cell was reached assuming the cell was successfully reached).
Therefore, it is recommended to calculate the maximal probability of reaching the station from every cell and the best policy (direction) for every cell. The calculation of these probabilities and policies is tested by the script probability_test.py.
These tests are evaluated by 0 points on recodex, so their passing is voluntary.
Nevertheless, they may be helpful to fulfill this assignment.

* It may be easier to first implement value update but this method usually leads to 8 points since it is too slow for the fifth test.
To make the computation faster, you can try some tricks or policy update.

* Python package scipy may be useful to solve the task.
Especially, [a sparse matrix](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html) and [a linear system solver](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.spsolve.html) may be handy.
