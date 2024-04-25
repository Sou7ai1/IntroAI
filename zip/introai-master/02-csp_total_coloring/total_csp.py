import constraint

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TODO: The implementation of this function finds some total coloring but the number of colors may not be minimal.
        Find the total chromatic index.
    """
    
    ## Idea of values taken from here https://www.geeksforgeeks.org/python-assign-values-to-values-list/
    ## Some small concepts taken frm here : 
    total_edge = {}  
    solution = {}
    total_nodes = {}
        
    edge1 = len(graph.nodes())

    for edge in graph.edges():
        u, v = edge
        total_edge[u, v] = edge1
        total_edge[v, u] = edge1
        edge1 += 1
        
    node1 = 0
    max_deg = 0
    for node in graph.nodes:
        max_deg = max(graph.degree[node],max_deg)
        total_nodes[node] = node1
        node1 += 1
    
    
    solution = False

    while not solution:
        problem = constraint.Problem()
        max_deg += 1
        domain = range(max_deg)
        problem.addVariables(total_nodes.values(), domain)
        problem.addVariables(set(total_edge.values()), domain)   #Variable Declaration for the edges and vertices

        for node1 in total_nodes:
            inci_edges = []
            for edge in graph.edges(node1):
             inci_edges.append(total_edge[edge])
            problem.addConstraint(constraint.AllDifferentConstraint(),[total_nodes[node1]]+inci_edges)#Constraint for the edges and their neighbors

            for u in graph[node1]:
                problem.addConstraint(constraint.AllDifferentConstraint(), [total_nodes[u],total_nodes[node1], total_edge[(node1, u)]])

        solution = problem.getSolution()

    for u in graph.nodes():
        graph.nodes[u]["color"] = solution[total_nodes[u]]
    for u, v in graph.edges():
        num = total_edge[u, v]
        graph.edges[u, v]["color"] = solution[num]
        
    return max_deg