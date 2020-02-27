Implementujte monotónní heuristiky pro A* algoritmus spuštěný na podgrafy následujících nekonečných mřížek.

* *Grid2D*: Klasická dvourozměrná mřížka
* *Grid3D*: Klasická třírozměrná mřížka
* *GridDiagonal2D*: Dvourozměrná mřížka obsahující i úhlopříčky (obsahuje například hrany {(0,0),(1,1)} a {(0,1),(1,0)})
* *GridAllDiagonal3D*: Třírozměrná mřížka obsahující stěnové i prostorové úhlopříčky (obsahuje například hrany {(0,0,0),(1,1,0)} a {(0,0,0),(1,1,1)})
* *GridFaceDiagonal3D*: Třírozměrná mřížka obsahující stěnové úhlopříčky ale nikoliv prostorové (obsahuje například hranu {(0,0,0),(1,1,0)} ale neobsahuje {(0,0,0),(1,1,1)})
* *GridKnight2D*: Hrany odpovídají právě pohybům koně po šachovnici (obsahuje například hrany {(0,0),(2,1)} a {(0,0),(-1,2)} ale neobsahuje {(0,0),(1,0)})

Podgraf mřížky je daný orákulem, který danou hranu rozhodne, zda je hrana mřížky v podgrafu zachovaná nebo je odstraněná.

Stáhněte si gitový repozitář https://gitlab.mff.cuni.cz/finkj1am/introai.git a v souboru heuristics.py implementujte všechny funkce. Do ReCodexu odevzdávejte pouze soubor heuristics.py. Při ladění můžete upravovat i ostatní soubory, ale mějte na paměti, že recodex nebude brát tyto změny v potaz.

Testy na recodexu jsou stejné jako máte v souboru informed_search_tests.py. Očekávaná heuristika navštíví nejvýše milion vrcholů v každém testu a neefektivní heuristika nestihne najít nejkratší cestu v časovém limitu. Doba běhu všech testů je 1 až 3 minuty v závislosti na rychlosti počítače.

Rada na závěr: Znáte příkaz "ulimit -v"?


====================================================================================================

Implement monotone heuristics for the A* algorithm running on subgraphs of the following infinite grids.

* Grid2D: The classic two-dimensional grid
* Grid3D: The classic three-dimensional grid
* GridDiagonal2D: The two-dimensional grid that includes diagonals (including {(0,0), (1,1)} and {(0,1), (1,0)})
* GridAllDiagonal3D: The three-dimensional grid containing both face and space diagonals (including, for example, {(0,0,0), (1,1,0)} and {(0,0,0), (1,1,1)})
* GridFaceDiagonal3D: The three-dimensional grid containing face diagonals but not space ones (for example, it contains {(0,0,0), (1,1,0)} but does not contain {(0,0,0), (1,1,1)} )
* GridKnight2D: Edges correspond exactly to the movement of the knight on the chessboard (for example, it contains {(0,0), (2,1)} and {(0,0), (-1,2)} but it does not include {(0,0), (1.0)})

A subgraph is given by an oracle that decides whether an edge of the grid is presented or removed from the subgraph.

Download the git repository https://gitlab.mff.cuni.cz/finkj1am/introai.git and implement all functions in heuristics.py. Submit only the heuristics.py file to ReCodex. Please, do not change the name of the file when submitting. You can also edit other files while debugging, but keep in mind that recodex will not take these changes into account.

Recodex tests are the same as in the file informed_search_tests.py. The expected heuristics visit at million vertices in each test, and inefficient heuristics fails to find the shortest path within time limit set in ReCodex. All tests should run between 1 and 3 minutes depending on speed of a computer.

Finally, do you know the command "ulimit -v"?

