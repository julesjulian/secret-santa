# def depth_first_search(adjacency_list, node, visited, start, results):
#     if node in visited:
#         if node == start:
#             visited.append(node)
#             results.append(visited)
#             visited = list()
#         return
#     visited.append(node)
#     for child in adjacency_list[node]:
#         depth_first_search(adjacency_list, child, visited, start, results)
#     return results

# def depth_first_search(graph, start):
#     results, visited, stack = list(), list(), [start]
#     while stack:
#         vertex = stack.pop()
#         if vertex not in visited:
#             visited.append(vertex)
#             stack.extend(v for v in graph[vertex] if v not in visited or v is start)
#         elif vertex is start:
#             visited.append(vertex)
#             results.append(visited)
#     return results

def get_all_cycles(graph, start):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path[1:]):
            if next == start:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def get_all_cycles_of_length_n(graph, start, n_vertices):
    all_cycles = list(get_all_cycles(graph, start))
    all_cycles_length_n = [cycle for cycle in all_cycles if len(cycle) == n_vertices + 1]
    return all_cycles_length_n
