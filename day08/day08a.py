import re

f = open("day08-input.txt")
all_lines = f.readlines()

instructions = all_lines[0]

edge_dict = {}

for line in all_lines[2::]:
    match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
    assert match is not None
    groups = match.groups()
    edge_dict[groups[0]] = (groups[1], groups[2])

current_node = "AAA"
destination_node = "ZZZ"
num_hops = 0
instruction_index = 0

while current_node != destination_node:
    next_nodes = edge_dict[current_node]
    instruction = instructions[instruction_index]
    print(f"{current_node} {instruction}")
    if instruction == "L":
        current_node = next_nodes[0]
    else:
        current_node = next_nodes[1]
    num_hops += 1
    instruction_index += 1
    if instruction_index == len(instructions) - 1:
        instruction_index = 0

print(num_hops)   
