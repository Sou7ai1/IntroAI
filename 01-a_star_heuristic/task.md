Implementujte monotónní heurestiky pro A* algoritmus spuštěný na podgrafy následujících nekonečných mřížek.

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

