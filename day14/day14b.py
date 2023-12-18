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

def roll_rocks_south(rock_rows: List[List[str]]):
    rolled_a_rock = False
    for row_a, row_b in zip(rock_rows[1:], rock_rows):
        for i in range(len(row_a)):
            if row_b[i] == "O" and row_a[i] == ".":
                row_a[i] = "O"
                row_b[i] = "."
                rolled_a_rock = True
    return rolled_a_rock

def roll_rocks_east(rock_rows: List[List[str]]):
    rolled_a_rock = False
    for row in rock_rows:
        for i in range(0,len(row)-1):
            if row[i] == "O" and row[i+1] == ".":
                row[i] = "."
                row[i+1] = "O"
                rolled_a_rock = True
    return rolled_a_rock

def roll_rocks_west(rock_rows: List[List[str]]):
    rolled_a_rock = False
    for row in rock_rows:
        for i in range(0,len(row)-1):
            if row[i] == "." and row[i+1] == "O":
                row[i] = "O"
                row[i+1] = "."
                rolled_a_rock = True
    return rolled_a_rock

def perform_spin_cycle(rock_rows: List[List[str]]):
    while roll_rocks_north(rock_rows):
        pass
    while roll_rocks_west(rock_rows):
        pass
    while roll_rocks_south(rock_rows):
        pass
    while roll_rocks_east(rock_rows):
        pass

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

for i in range(0, 1000000000):
    print(f"{i} {compute_weight(rock_rows)}")
    backup_rock_rows = [[x for x in line] for line in rock_rows]
    perform_spin_cycle(rock_rows)
    if rock_rows == backup_rock_rows:
        break

print(rock_rows)
print(compute_weight(rock_rows))