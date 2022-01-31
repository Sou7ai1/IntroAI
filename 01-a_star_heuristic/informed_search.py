import heapq

class Vertex:
    """ Addition data for every vertex visited by A* """
    def __init__(self, coord, distance, heuristic, predecessor):
        self.coord = coord
        self.distance = distance
        self.heuristic = heuristic
        self.predecessor = predecessor
        self.explored = False

    def __lt__(self, other):
        return self.distance > other.distance

def check_path(graph, origin, destination):
    """ Test whether A* found a proper path. """
    vertex = destination
    while vertex.predecessor:
        assert vertex.predecessor.coord in graph.neighbours(vertex.coord)
        assert graph.oracle(vertex.coord, vertex.predecessor.coord)
        assert vertex.distance == vertex.predecessor.distance + 1
        vertex = vertex.predecessor
    assert vertex == origin

def informed_search(graph, heuristic, origin_coord, destination_coord):
    """
    A* algorithm finding a shortest path between two given coordinates using a given heuristic function.
    Return a pair of integers containing the length of a shortest path and the number of vertices visited during the algorithm.
    Fails if no path exists.
    """

    h = heuristic(destination_coord, destination_coord)
    if not isinstance(h, int):
        return (False, "Heuristic function must always return an integer", 0, 0)
    if h != 0:
        return (False, "Heuristic from the destination to the destination must be zero", 0, 0)

    h = heuristic(origin_coord, destination_coord)
    if not isinstance(h, int) or h < 0:
        print("Your heuristic from", origin_coord, "to", destination_coord, "is", h, "which is not a non-negative integer")
        return (False, "Heuristic must be a non-negative integer", 0, 0)
    origin = Vertex(origin_coord, 0, h, None)

    # Dictionary which gives additional information stored in Vertex for given coordinates of visited point.
    visited = { origin_coord : origin }

    # A heap of vertices.
    # Since all tested graph has very small degree, decreasing priority would be inefficient.
    # Therefore, a single vertex may have multiple occurences in the heap.
    queue = []
    heapq.heappush(queue, (origin.distance+origin.heuristic,origin))

    while queue:
        if len(visited) > 3000000:
            print("Your heuristic is too inefficient so you need to find a better heuristic.")
            return (False, "Too many visited vertices", 0, 0)

        _,explore = heapq.heappop(queue)
        assert not explore.predecessor or explore.distance == explore.predecessor.distance + 1

        # Terminate when the destination is reached.
        if explore.coord == destination_coord:
            check_path(graph, origin, explore)
            return (True, "Correct", explore.distance, len(visited))

        # Explore all neighbours if this vertex has not been explored yet.
        elif not explore.explored:
            explore.explored = True
            distance = explore.distance + 1

            # Visit all neighbours
            for visit_coord in graph.neighbours(explore.coord):
                if not visit_coord in visited:
                    h = heuristic(visit_coord, destination_coord)
                    if not isinstance(h, int) or h < 0:
                        print("Your heuristic from", visit_coord, "to", destination_coord, "is", h, "which is not a non-negative integer")
                        return (False, "Heuristic function must always return a non-negative integer", 0, 0)
                    visit = Vertex(visit_coord, distance, h, explore)
                    visited[visit_coord] = visit
                    heapq.heappush(queue, (visit.distance+visit.heuristic,visit))

                else:
                    visit = visited[visit_coord]
                    if visit.distance > distance:
                        assert not visit.explored, "The distance of explored vertices cannot be decreased if the heuristic is monotonic"
                        # The priority in the queue should be decreased
                        # but finding the vertex in the queue or updating its position would not be more efficent.
                        visit.distance = distance
                        visit.predecessor = explore
                        heapq.heappush(queue, (visit.distance+visit.heuristic,visit))

                if explore.heuristic > visit.heuristic + 1:
                    print("Your heuristic from", explore.coord, "to", destination_coord, "is", explore.heuristic,
                        "and heuristic from", visit.coord, "to", destination_coord, "is", visit.heuristic,
                        "which fails the monotonic property since the distance between", explore.coord, "and", visit.coord, "is 1.")
                    return (False, "Heuristic must be monotonic", 0, 0)

    assert False, "A path exists in all tests"
