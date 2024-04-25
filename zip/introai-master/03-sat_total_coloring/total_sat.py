from pysat.solvers import Glucose3


def total_coloring(graph):
    solution = []
    colors = []
    node = {}
    total_edges = {}
    edge1 = len(graph.nodes)
    value_edges = []
    max_deg = 0

    for node_val in graph.nodes:
        max_deg = max(graph.degree[node_val], max_deg)
    count = max_deg

    for edge in graph.edges:
        value_edges.append(edge1)
        total_edges[edge[0], edge[1]] = edge1
        total_edges[edge[1], edge[0]] = edge1
        edge1 += 1

    solution = False

    while not solution:
        Glu = Glucose3()
        count += 1
        color = list(range(1, count + 1))

        y = 0
        node = {}
        for v in graph.nodes:
            for c in color:
                node[(v, c)] = y * count + c
            y += 1
        for e in value_edges:
            for c in color:
                node[(e, c)] = y * count + c
            y += 1

        for v in graph.nodes:
            Glu.add_clause([node[v, c] for c in color])

            for j in range(len(color) - 1):
                for i in range(j + 1, len(color)):
                    Glu.add_clause([-node[v, color[j]], -node[v, color[i]]])
            incident = [e for e in graph.edges(v)]
            for c in color:
                if len(incident) > 1:
                    for i in range(len(incident) - 1):
                        for j in range(i + 1, len(incident)):
                            Glu.add_clause([-node[total_edges[incident[i]], c], -node[total_edges[incident[j]], c]])

        for e0, e1 in graph.edges:
            e = total_edges[e0, e1]
            for i in range(len(color) - 1):
                for j in range(i + 1, len(color)):
                    Glu.add_clause([-node[e, color[i]], -node[e, color[j]]])
            Glu.add_clause([node[e, c] for c in color])
            for c in color:
                Glu.add_clause([-node[e0, c], -node[e1, c]])
                Glu.add_clause([-node[e0, c], -node[e, c]])
                Glu.add_clause([-node[e1, c], -node[e, c]])
            Glu.add_clause([node[e, c] for c in color])
        if Glu.solve():
            solution = Glu.get_model()

    solution = [x for x in solution if x > 0]

    for u in graph.nodes():
        col = -1
        for c in color:
            var_num = node[u, c]
            i, j = 0, len(solution) - 1
            while i <= j:
                m = (i + j) // 2
                if solution[m] == var_num:
                    col = c
                    break
                elif solution[m] < var_num:
                    i = m + 1
                else:
                    j = m - 1
            if col != -1:
                break
        graph.nodes[u]["color"] = col - 1

    for x, y in graph.edges():
        e_color = -1
        for c in color:
            var_num = node[total_edges[x, y], c]
            i, j = 0, len(solution) - 1
            while i <= j:
                m = (i + j) // 2
                if solution[m] == var_num:
                    e_color = c
                    break
                elif solution[m] < var_num:
                    i = m + 1
                else:
                    j = m - 1
            if e_color != -1:
                break
        graph.edges[x, y]["color"] = e_color - 1

    return count
