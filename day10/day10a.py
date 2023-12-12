from typing import List, Set, Tuple, Optional

symbol_to_coord_diff = {
    "|" : [(-1, 0), (1, 0)],
    "-" : [(0, -1), (0, 1)],
    "L" : [(-1, 0), (0, 1)],
    "J" : [(-1, 0), (0, -1)],
    "7" : [(0, -1), (1, 0)],
    "F" : [(0, 1), (1, 0)],
    "." : [],
    "\n" : [],
    "S" : [(-1, 0), (0, 1)] # this was obtained by inspection from the input
}

class Node:
    row: int
    col: int
    # row col
    connected_coords: List[Tuple[int, int]]

    def __init__(self, symbol, row, col):
        self.row = row
        self.col = col
        coord_diffs = symbol_to_coord_diff[symbol]
        self.connected_coords = [(x[0] + self.row, x[1] + self.col) for x in coord_diffs]

f = open("day10-input.txt")
all_lines = f.readlines()

num_rows = len(all_lines)
num_cols = len(all_lines[0])

node_array: List[List[Optional[Node]]] = [[None] * num_cols for _ in range(num_rows)]

active_row = 0
active_col = 0

visited_nodes: Set[Node] = set()
nodes_to_visit: Set[Node] = set()

for row_index, line in enumerate(all_lines):
    for col_index, char in enumerate(line):
        new_node = Node(char, row_index, col_index)
        node_array[row_index][col_index] = new_node
        if char == "S":
            nodes_to_visit.add(new_node)

while len(nodes_to_visit) > 0:
    node_to_visit = nodes_to_visit.pop()
    visited_nodes.add(node_to_visit)
    for x in node_to_visit.connected_coords:
        next_node = node_array[x[0]][x[1]]
        assert next_node is not None
        if (next_node not in visited_nodes) and (next_node not in nodes_to_visit):
            nodes_to_visit.add(next_node)

print(visited_nodes)
print(len(visited_nodes))
print(len(visited_nodes) / 2)
