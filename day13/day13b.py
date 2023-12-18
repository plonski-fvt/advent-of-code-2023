from typing import List

def find_valid_reflections(line: str):
    valid_reflections = set()
    for reflection_index in range(1, len(line)):
        good_reflection = True
        for c_a, c_b in zip(line[reflection_index:], line[reflection_index - 1::-1]):
            if c_a != c_b:
                good_reflection = False
                break
        if good_reflection:
            valid_reflections.add(reflection_index)
    return valid_reflections

print(find_valid_reflections("##....."))

def find_new_reflection_axis(lines: List[str]):
    sets_of_reflection_candidates = [find_valid_reflections(line) for line in lines]
    previous_reflection_set = set.intersection(*sets_of_reflection_candidates)
    for line_index, line in enumerate(lines):
        sets_for_other_lines = sets_of_reflection_candidates[:line_index] + sets_of_reflection_candidates[line_index + 1:]
        intersection_so_far = set.intersection(*sets_for_other_lines) - previous_reflection_set
        if not intersection_so_far:
            continue
        for mutated_index in range(len(line)):
            existing_value = line[mutated_index]
            new_value = "#" if existing_value == "." else "."
            mutated_line = line[:mutated_index] + new_value + line[mutated_index + 1:]
            mutant_reflections = find_valid_reflections(mutated_line)
            mutant_intersection = intersection_so_far & mutant_reflections
            if mutant_intersection:
                return list(mutant_intersection)[0]
    return None


f = open("input-day13.txt")
inputs_as_strings = f.read().split("\n\n")

answer = 0

for pattern in inputs_as_strings:
    print("\n" + pattern + "\n")
    lines = pattern.split("\n")

    # first try the horizontal reflections

    horizontal_reflection = find_new_reflection_axis(lines)

    print(f"horiz reflection: {horizontal_reflection}")

    if horizontal_reflection is not None:
        answer += horizontal_reflection
        continue

    # now try the vertical reflections

    rotated_lines = []
    for new_row_index in range(len(lines[0])):
        next_row = [lines[i][new_row_index] for i in range(len(lines))]
        rotated_lines.append("".join(next_row))

    vertical_reflection = find_new_reflection_axis(rotated_lines)

    print(f"vert reflection: {vertical_reflection}")

    assert vertical_reflection is not None
    answer += vertical_reflection * 100

print(answer)
