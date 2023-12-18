from typing import List

def test_reflection_axis(lines: List[str], reflection_index):
    if reflection_index == 0:
        return False
    good_reflection = True
    for line in lines:
        # print(line[reflection_index:])
        # print(line[reflection_index - 1::-1])
        for c_a, c_b in zip(line[reflection_index:], line[reflection_index - 1::-1]):
            if c_a != c_b:
                good_reflection = False
                break
        if not good_reflection:
            break
    return good_reflection

print(test_reflection_axis(["##....."], 0))
print(test_reflection_axis(["##....."], 1))
print(test_reflection_axis(["##....."], 2))

f = open("input-day13.txt")
inputs_as_strings = f.read().split("\n\n")

answer = 0

for pattern in inputs_as_strings:
    print(pattern + "\n")
    lines = pattern.split("\n")

    # first try the horizontal reflections
    horizontal_reflection = None
    for reflection_index in range(1, len(lines[0])):
        if test_reflection_axis(lines, reflection_index):
            horizontal_reflection = reflection_index
            break
    
    if horizontal_reflection is not None:
        answer += horizontal_reflection
        continue

    # now try the vertical reflections
    rotated_lines = []
    for new_row_index in range(len(lines[0])):
        next_row = [lines[i][new_row_index] for i in range(len(lines))]
        rotated_lines.append(next_row)

    vertical_reflection = None
    for reflection_index in range(1, len(rotated_lines[0])):
        if test_reflection_axis(rotated_lines, reflection_index):
            vertical_reflection = reflection_index
            break

    assert vertical_reflection is not None
    answer += vertical_reflection * 100

print(answer)
