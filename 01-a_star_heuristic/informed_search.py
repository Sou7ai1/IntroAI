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
        """ Artificial comparison required by heapq. """
        return self.distance > other.distance

def check_path(graph, origin, destination):
    """ Fails if A* did not found a proper path. """
    vertex = destination
    while vertex.predecessor:
        assert vertex.predecessor.coord in graph.neighbours(vertex.coord)
        assert graph.oracle(vertex.coord, vertex.predecessor.coord)
        assert vertex.distance == vertex.predecessor.distance + 1
        vertex = vertex.predecessor
    assert vertex == origin

def call_heuristic(heuristic, current, destination):
    h = heuristic(current, destination)
    assert isinstance(h, int) and h >= 0
    return h

def informed_search(graph, heuristic, origin_coord, destination_coord):
    """
    A* algorithm finding a shortest path between two given coordinates using a given heuristic function.
    Return a pair of integers containing the length of a shortest path and the number of vertices visited during the algorithm.
    Fails if no path exists.
    """

    origin = Vertex(origin_coord, 0, call_heuristic(heuristic, origin_coord, destination_coord), None)

    # Dictionary which gives additional information stored in Vertex for given coordinates of visited point.
    visited = { origin_coord : origin }

    # A heap of vertices.
    # Since all tested graph has very small degree, decreasing priority would be inefficient.
    # Therefore, a single vertex may have multiple occurences in the heap.
    queue = []
    heapq.heappush(queue, (origin.distance+origin.heuristic,origin))

    while queue:
        _,explore = heapq.heappop(queue)
        assert not explore.predecessor or explore.distance == explore.predecessor.distance + 1

        # Terminate when the destination is reached.
        if explore.coord == destination_coord:
            check_path(graph, origin, explore)
            return (explore.distance,len(visited))

        # Explore all neighbours if this vertex has not been explored yet.
        elif not explore.explored:
            explore.explored = True
            distance = explore.distance + 1

            # Visit all neighbours
            for visit_coord in graph.neighbours(explore.coord):
                if not visit_coord in visited:
                    visit = Vertex(visit_coord, distance, call_heuristic(heuristic, visit_coord, destination_coord), explore)
                    visited[visit_coord] = visit
                    heapq.heappush(queue, (visit.distance+visit.heuristic,visit))

                else:
                    visit = visited[visit_coord]
                    if visit.distance > distance:
                        # The priority in the queue should be decreased
                        # but finding the vertex in the queue or updating its position would not be more efficent.
                        assert not visit.explored, "The distance of explored vertices cannot be decreased if the heuristic is monotonic"
                        visit.distance = distance
                        visit.predecessor = explore
                        heapq.heappush(queue, (visit.distance+visit.heuristic,visit))

                assert explore.heuristic <= visit.heuristic + 1, "Heuristic must be monotonic"

    assert False, "A path in all tests exist"

