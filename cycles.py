def get_all_cycles(graph, start):
    stack = [(start, [start])]
    all_cycles = []
    while len(stack) > 0:
        (vertex, path) = stack.pop()
        children_not_on_path_or_start = graph[vertex] - set(path[1:])
        for child in children_not_on_path_or_start:
            if child == start:
                all_cycles.append(path + [child])
            else:
                stack.append((child, path + [child]))
    return all_cycles

def get_all_full_cycles(graph, start):
    all_cycles = get_all_cycles(graph, start)
    all_full_cycles = [cycle for cycle in all_cycles if len(cycle) == len(graph) + 1]
    return all_full_cycles
