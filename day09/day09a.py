from typing import List
import re

def get_next_line(prev_line: List[int]) -> List[int]:
    next_line = []
    for item, next_item in zip(prev_line, prev_line[1::]):
        next_line.append(next_item - item)
    return next_line

def is_all_zeros(line: List[int]):
    for item in line:
        if 0 != item:
            return False
    return True

def extrapolate_line(line: List[int]) -> int:
    if is_all_zeros(line):
        print(line, 0)
        return 0
    next_line = get_next_line(line)
    extrapolated_next_line = extrapolate_line(next_line)
    extrapolated_this_line = line[-1] + extrapolated_next_line
    print(line, extrapolated_this_line)
    return extrapolated_this_line

f = open("day09-input.txt")

sum = 0
for text_line in f:
    split_line = re.findall(r"(-?\d+)", text_line)
    line = [int(x) for x in split_line]
    e = extrapolate_line(line)
    sum += e

print(sum)
    