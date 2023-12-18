from typing import List

def roll_rocks_north(rock_rows: List[List[str]]):
    rolled_a_rock = False
    for row_a, row_b in zip(rock_rows, rock_rows[1:]):
        for i in range(len(row_a)):
            if row_b[i] == "O" and row_a[i] == ".":
                row_a[i] = "O"
                row_b[i] = "."
                rolled_a_rock = True
    return rolled_a_rock

def compute_weight(rock_rows: List[List[str]]):
    weight = 0
    for row_index, row in enumerate(rock_rows):
        multiplier = len(rock_rows) - row_index
        weight += multiplier * row.count("O")
    return weight

f = open("day14-input.txt")
lines = f.read().split("\n")
cols = len(lines[0])
rock_rows: List[List[str]] = []

for line_index, line in enumerate(lines):
    if len(line) != cols:
        break
    rock_rows.append(list(line))

while(roll_rocks_north(rock_rows)):
    print("rollin...")

print(rock_rows)
print(compute_weight(rock_rows))