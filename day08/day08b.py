import re

def everything_ends_in_z(nodes):
    condition = True
    for node in nodes:
        if node[2] != "Z":
            condition = False
            break
    return condition

f = open("day08-input.txt")
all_lines = f.readlines()

instructions = all_lines[0]

edge_dict = {}

current_nodes = []

for line in all_lines[2::]:
    match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
    assert match is not None
    groups = match.groups()
    edge_dict[groups[0]] = (groups[1], groups[2])
    if groups[0][2] == "A":
        current_nodes.append(groups[0])

num_hops = 0
instruction_index = 0

while not everything_ends_in_z(current_nodes):

    # print(current_nodes)

    instruction = instructions[instruction_index]
    instruction_index += 1
    if instruction_index == len(instructions) - 1:
        instruction_index = 0

    next_nodes = []

    for node in current_nodes:
        potential_jumps = edge_dict[node]
        if instruction == "L":
            next_nodes.append(potential_jumps[0])
        else:
            next_nodes.append(potential_jumps[1])

    current_nodes = next_nodes
    num_hops += 1

print(num_hops)   
