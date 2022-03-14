Using Planning Domain Definition Language [PDDL](https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language) write a domain definition for the following transportation problem.

A logistic company needs to create a plan for transporting goods packed in boxes by cars located in various places.
The initial and the goal positions are given in problem definition files.
Note that the capacity of every can is one box and boxes can be transported only by car (i.e. no teleportation).

Your task is to write the domain definition file for this task containing the following commands with arguments in the given order.
* *load(box car place)*: Load a box into a car, both located the given place.
* *unload(box car place)*: Unload a box from a car located a place.
* *move(car place_origin place_destination)*: Move a car from the original place to the destination.

In order to test your program, install Python library [pyperplan](https://github.com/aibasel/pyperplan).
Ten problem definition files are provided in our git for testing and you are expected to write a single domain definition file called *domain.pddl* solving all of them and submit it to recodex.
Please note that there are many variants of PDDL and you are expected to use the version 1.2 accepted by pyperplan for testing.
Examples of acceptable domain definition files are available at (https://github.com/aibasel/pyperplan/tree/master/benchmarks).

There are many resources about PDDL on the Internet (see below), but be aware that not all versions of PDDL are accepted by our testing script.
Note that the used PDDL solver does not accept negative preconditions. Furthermore, no *require* command is needed to solve this task.
* http://users.cecs.anu.edu.au/~patrik/pddlman/writing.html
* https://github.com/pellierd/pddl4j/wiki/Logistics:-a-simple-running-example
* https://cw.fel.cvut.cz/old/_media/courses/ae3b33kui/lectures/lecture_09_10.pdf
* https://courses.cs.washington.edu/courses/cse473/06sp/pddl.pdf
