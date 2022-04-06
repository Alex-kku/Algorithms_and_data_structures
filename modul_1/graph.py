import sys
import re
from collections import deque

graph_type = ''
search_type = ''
start_vertex = ''
graph_edges = dict()
visited_vertices = set()
traversal_sequence = deque()
for string in sys.stdin:
    if re.match(r"\s*$", string):
        continue
    elif re.match(r"[ud]?\s\S+\s[db]?$", string) and start_vertex == '':
        split_string = string.split()
        graph_type = split_string[0]
        start_vertex = split_string[1]
        search_type = split_string[2]
    elif re.match(r"\S+\s\S+$", string):
        split_string = string.split()
        if split_string[0] not in graph_edges:
            graph_edges[split_string[0]] = []
        if split_string[1] not in graph_edges:
            graph_edges[split_string[1]] = []
        if split_string[1] not in graph_edges[split_string[0]]:
            graph_edges[split_string[0]].append(split_string[1])
        if graph_type == 'u':
            if split_string[0] not in graph_edges[split_string[1]]:
                graph_edges[split_string[1]].append(split_string[0])
traversal_sequence.append(start_vertex)
if search_type == 'b':
    visited_vertices.add(start_vertex)
    while traversal_sequence:
        for vertex in sorted(graph_edges[traversal_sequence[0]]):
            if vertex not in visited_vertices:
                visited_vertices.add(vertex)
                traversal_sequence.append(vertex)
        print(traversal_sequence.popleft())
if search_type == 'd':
    while traversal_sequence:
        next_vertex = traversal_sequence.pop()
        if next_vertex not in visited_vertices:
            print(next_vertex)
            visited_vertices.add(next_vertex)
            for vertex in sorted(graph_edges[next_vertex])[::-1]:
                traversal_sequence.append(vertex)

