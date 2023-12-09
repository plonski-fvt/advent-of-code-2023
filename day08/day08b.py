import re
import math

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
z_nodes = []

for line in all_lines[2::]:
    match = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
    assert match is not None
    groups = match.groups()
    edge_dict[groups[0]] = (groups[1], groups[2])
    if groups[0][2] == "A":
        current_nodes.append(groups[0])
    if groups[0][2] == "Z":
        z_nodes.append(groups[0])

num_hops = 0
instruction_index = 0

first_hop_encountered_at = {}
last_hop_encountered_at = {}
distance_between_last_two_hops = {}

while num_hops < 1000000 and not everything_ends_in_z(current_nodes):

    # print(current_nodes)

    instruction = instructions[instruction_index]
    instruction_index += 1
    if instruction_index == len(instructions) - 1:
        instruction_index = 0

    next_nodes = []

    for node in current_nodes:
        if node[2] == "Z":
            print(instruction_index - 1, node, num_hops)
        potential_jumps = edge_dict[node]
        if instruction == "L":
            next_nodes.append(potential_jumps[0])
        else:
            next_nodes.append(potential_jumps[1])
        last_time_we_saw_this = last_hop_encountered_at.get(node, 0)
        last_hop_encountered_at[node] = num_hops
        distance_between_last_two_hops[node] = num_hops - last_time_we_saw_this
        if node not in first_hop_encountered_at:
            first_hop_encountered_at[node] = num_hops

    current_nodes = next_nodes
    num_hops += 1

print(num_hops)   

# we end up trying to solve an equation of the form:
# a + b x = c + d y = e + f z ... etc
# so lets just search that directly

cycling_indices = []
amounts_to_increment = []
first_time_encountered = []

for node in z_nodes:
    print(node, last_hop_encountered_at[node], distance_between_last_two_hops[node])
    cycling_indices.append(last_hop_encountered_at[node])
    amounts_to_increment.append(distance_between_last_two_hops[node])
    first_time_encountered.append(first_hop_encountered_at[node])

print(cycling_indices)
print(amounts_to_increment)
print(first_time_encountered)

gcd_of_increments = math.gcd(amounts_to_increment[0], amounts_to_increment[1], amounts_to_increment[2], amounts_to_increment[3], amounts_to_increment[4], amounts_to_increment[5])
print("gcd ", gcd_of_increments)

lcm_of_increments = math.lcm(amounts_to_increment[0], amounts_to_increment[1], amounts_to_increment[2], amounts_to_increment[3], amounts_to_increment[4], amounts_to_increment[5])
print("lcm ", lcm_of_increments)

# it is sort of a wild coincidence that lcm is the solution here.
# this only works because in this input the first time encountered is the same as the cycle length
# otherwise we would have to compute an offset lcm which would be a lot more work