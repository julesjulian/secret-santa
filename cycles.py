def get_all_cycles(graph, start):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path[1:]):
            if next == start:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def get_all_full_cycles(graph, start):
    all_cycles = list(get_all_cycles(graph, start))
    all_full_cycles = [cycle for cycle in all_cycles if len(cycle) == len(graph) + 1]
    return all_full_cycles
