from enum import Enum
from typing import List
import re

class Spring(Enum):
    WORKING = "."
    BROKEN = "#"
    UNKNOWN = "?"

    def __repr__(self):
        return self.value

def convert_string_to_springs(str) -> List[Spring]:
    springs = []
    for c in str:
        springs.append(Spring(c))
    return springs

consistency_cache = {}

def test_consistency(spring_row_a: List[Spring], spring_row_b: List[Spring]):
    # note that if one of these is shorter, it'll only test the first part of the other
    # this is actually desired behavior here!
    consistent = True
    for a, b in zip(spring_row_a, spring_row_b):
        if a != Spring.UNKNOWN and b != Spring.UNKNOWN and a != b:
            consistent = False
            break
    return consistent

def count_consistent_arrangements(spring_row: List[Spring], constraints: List[int]) -> int:
    if len(constraints) == 0:
        all_good_row = [Spring(".")] * len(spring_row)
        if test_consistency(spring_row, all_good_row):
            return 1
        else:
            return 0
    num_arrangements_found = 0
    total_required_broken = sum(constraints)
    space_for_constraints = total_required_broken + len(constraints) - 1
    for start_of_first_constraint in range(len(spring_row) + 1 - space_for_constraints):
        test_row = [Spring(".")] * start_of_first_constraint 
        test_row += [Spring("#")] * constraints[0]
        if len(test_row) < len(spring_row):
            test_row += [Spring(".")]
        if test_consistency(test_row, spring_row):
            if len(spring_row) == len(test_row):
                if len(constraints) == 1:
                    num_arrangements_found += 1
            else:
                spring_row_remainder = spring_row[len(test_row):]
                num_arrangements_found += count_consistent_arrangements(spring_row_remainder, constraints[1:])
    return num_arrangements_found

# print(count_consistent_arrangements(convert_string_to_springs("....."), []))
# print(count_consistent_arrangements(convert_string_to_springs("?###?"), [3]))
# print(count_consistent_arrangements(convert_string_to_springs("?###??????"), [3,2,1]))
# print(count_consistent_arrangements(convert_string_to_springs("?###????????"), [3,2,1]))

f = open("input-day12.txt")

total_num_arrangements = 0

for line in f:
    spring_match = re.match(r"([\?\#\.]+)", line)
    assert spring_match is not None
    spring_row = convert_string_to_springs(spring_match.groups()[0])
    constraint_strings = re.findall(r"(\d+)", line)
    constraints = [int(x) for x in constraint_strings]
    num_arrangements = count_consistent_arrangements(spring_row, constraints)
    total_num_arrangements += num_arrangements

print(total_num_arrangements)

f = open("input-day12.txt")

total_num_arrangements2 = 0

for line in f:
    spring_match = re.match(r"([\?\#\.]+)", line)
    assert spring_match is not None
    spring_row = convert_string_to_springs(spring_match.groups()[0])
    spring_row = spring_row + [Spring("?")]
    spring_row = spring_row * 5
    spring_row = spring_row[:-1]
    constraint_strings = re.findall(r"(\d+)", line)
    constraints = [int(x) for x in constraint_strings]
    constraints = constraints * 5
    print(spring_row, constraints)
    num_arrangements = count_consistent_arrangements(spring_row, constraints)
    total_num_arrangements2 += num_arrangements

print(total_num_arrangements2)