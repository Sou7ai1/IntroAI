import sys
from heuristics import grid_2D_heuristic, grid_diagonal_2D_heuristic, grid_3D_heuristic, grid_face_diagonal_3D_heuristic, grid_all_diagonal_3D_heuristic, grid_queen_2D_heuristic, grid_great_king_2D_heuristic, grid_rook_2D_heuristic, grid_jumper_2D_heuristic
from graphs import Grid2D, GridDiagonal2D, GridQueen2D, GridGreatKing2D, GridRook2D, GridJumper2D, Grid3D, GridFaceDiagonal3D, GridAllDiagonal3D

def evaluate(graph, size, heuristic):
    """
        Run tests to verify the monotonicity of a given heuristic function.
        graph: A grid derived from Grid.
        size: Tested are all position 
        heuristic: A heuristic function to be tested for monotonicity.
        Return True if all tests pass.

        Warning: For simplicity, the function assumes that vertices are two or tree dimensional coordinates.
    """
    destination = [ 0 for _ in range(graph.dimension) ]
    h = heuristic(destination, destination)
    if not isinstance(h, int):
        print("Heuristic function must always return an integer")
        return False
    if h != 0:
        print("Heuristic from the destination to the destination must be zero")
        return False

    rectangle = [ range(-size,size) if i < graph.dimension else range(1) for i in range(3) ]
    for a in rectangle[0]:
        for b in rectangle[1]:
            for c in rectangle[2]:
                origin = (a,b) if graph.dimension == 2 else (a,b,c)
                heuristic_origin = heuristic(origin, destination)
                if not isinstance(heuristic_origin, int) or heuristic_origin < 0:
                    print("Your heuristic from", origin, "to", destination, "is", heuristic_origin, "which is not a non-negative integer")
                    return False

                for neighbour in graph.neighbours(origin):
                    heuristic_neighbour = heuristic(neighbour, destination)
                    if not isinstance(heuristic_neighbour, int) or heuristic_neighbour < 0:
                        print("Your heuristic from", neighbour, "to", destination, "is", heuristic_neighbour, "which is not a non-negative integer")
                        return False
                    if heuristic_origin > 1 + heuristic_neighbour:
                        print("Your heuristic from", origin, "to", destination, "is", heuristic_origin,
                        "and heuristic from", neighbour, "to", destination, "is", heuristic_neighbour,
                        "which fails the monotonic property since the distance between", origin, "and", neighbour, "is 1.")
                        return False
    return True

def main():
    tests = {
        "Grid2D": (Grid2D(1,1.), 100, grid_2D_heuristic),
        "GridDiagonal2D": (GridDiagonal2D(1,1.), 100, grid_diagonal_2D_heuristic),
        "GridQueen2D": (GridQueen2D(1,1.), 100, grid_queen_2D_heuristic),
        "GridGreatKing2D": (GridGreatKing2D(1,1.), 50, grid_great_king_2D_heuristic),
        "GridRook2D": (GridRook2D(1,1.), 100, grid_rook_2D_heuristic),
        "GridJumper2D": (GridJumper2D(1,1.), 100, grid_jumper_2D_heuristic),
        "Grid3D": (Grid3D(1,1.), 10, grid_3D_heuristic),
        "GridFaceDiagonal3D": (GridFaceDiagonal3D(1,1.), 10, grid_face_diagonal_3D_heuristic),
        "GridAllDiagonal3D": (GridAllDiagonal3D(1,1.), 10, grid_all_diagonal_3D_heuristic),
}

    if len(sys.argv) == 1:
        success = True
        for name in tests:
            print("Running test", name)
            success = evaluate(*tests[name]) and success
            print()
        print("All tests passed." if success else "Some tests failed.")
    else:
        name = sys.argv[1]
        if name in tests:
            evaluate(*tests[name])
        else:
            print("Unknown test", name)

"""
To run all tests, run the command
$ python3 probability_test.py

To run a test NAME, run the command
$ python3 probability_test.py NAME
"""
if __name__ == "__main__":
    main()
