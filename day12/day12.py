from enum import Enum
from typing import List
import re

arrangement_cache = {}

def test_consistency(spring_row: str, proposed_substring: str):
    # note that if one of these is shorter, it'll only test the first part of the other
    # this is actually desired behavior here!
    consistent = True
    for a, b in zip(spring_row, proposed_substring):
        if a != "?" and a != b:
            consistent = False
            break
    return consistent

def count_consistent_arrangements(spring_row: str, constraints: List[int]) -> int:
    cache_key = spring_row + "&"
    for x in constraints:
        cache_key += str(x)
        cache_key += ","
    cache_value = arrangement_cache.get(cache_key)
    if cache_value is not None:
        return cache_value
    if len(constraints) == 0:
        all_good_row = "." * len(spring_row)
        if test_consistency(spring_row, all_good_row):
            arrangement_cache[cache_key] = 1
            return 1
        else:
            arrangement_cache[cache_key] = 0
            return 0
    num_arrangements_found = 0
    total_required_broken = sum(constraints)
    space_for_constraints = total_required_broken + len(constraints) - 1
    for start_of_first_constraint in range(len(spring_row) + 1 - space_for_constraints):
        test_row = "." * start_of_first_constraint 
        test_row += "#" * constraints[0]
        if len(test_row) < len(spring_row):
            test_row += "."
        if test_consistency(spring_row, test_row):
            if len(spring_row) == len(test_row):
                if len(constraints) == 1:
                    num_arrangements_found += 1
            else:
                spring_row_remainder = spring_row[len(test_row):]
                num_arrangements_found += count_consistent_arrangements(spring_row_remainder, constraints[1:])
    arrangement_cache[cache_key] = num_arrangements_found
    return num_arrangements_found

f = open("input-day12.txt")

total_num_arrangements = 0

for line in f:
    spring_match = re.match(r"([\?\#\.]+)", line)
    assert spring_match is not None
    spring_row = spring_match.groups()[0]
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
    spring_row = spring_match.groups()[0]
    spring_row = spring_row + "?"
    spring_row = spring_row * 5
    spring_row = spring_row[:-1]
    constraint_strings = re.findall(r"(\d+)", line)
    constraints = [int(x) for x in constraint_strings]
    constraints = constraints * 5
    print(spring_row, constraints)
    num_arrangements = count_consistent_arrangements(spring_row, constraints)
    total_num_arrangements2 += num_arrangements

print(total_num_arrangements2)