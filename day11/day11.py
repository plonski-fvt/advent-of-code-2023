from typing import List, Tuple

# f = open("day11-test.txt")
f = open("day11-input.txt")

EXPANSION_COEFFICIENT = 1000000

all_lines = f.readlines()
num_rows = len(all_lines)
num_cols = len(all_lines[0])

print(num_rows, num_cols)

used_rows = set()
used_cols = set()
galaxy_positions: List[Tuple[int, int]] = []

for row_id, row in enumerate(all_lines):
    for col_id, char in enumerate(row):
        if char == "#":
            used_rows.add(row_id)
            used_cols.add(col_id)
            galaxy_positions.append((row_id, col_id))

print(used_rows, used_cols)

mapping_from_old_row_to_new = []
row_offset = 0
for row_id in range(num_rows):
    if row_id not in used_rows:
        row_offset += EXPANSION_COEFFICIENT - 1
    mapping_from_old_row_to_new.append(row_id + row_offset)

mapping_from_old_col_to_new = []
col_offset = 0
for col_id in range(num_cols):
    if col_id not in used_cols:
        col_offset += EXPANSION_COEFFICIENT - 1
    mapping_from_old_col_to_new.append(col_id + col_offset)

print(mapping_from_old_row_to_new, mapping_from_old_col_to_new)

adjusted_galaxy_positions: List[Tuple[int, int]] = []

for source_row, source_col in galaxy_positions:
    new_row = mapping_from_old_row_to_new[source_row]
    new_col = mapping_from_old_col_to_new[source_col]
    adjusted_galaxy_positions.append((new_row, new_col))

path_length_sum = 0

for i in range(len(adjusted_galaxy_positions)):
    for j in range(i + 1, len(adjusted_galaxy_positions)):
        source_row, source_col = adjusted_galaxy_positions[i]
        destination_row, destination_col = adjusted_galaxy_positions[j]
        distance = abs(source_row - destination_row) + abs(source_col - destination_col)
        path_length_sum += distance

print(path_length_sum)