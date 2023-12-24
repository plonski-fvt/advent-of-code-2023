from dataclasses import dataclass
from enum import Enum
from typing import Set, Tuple
import re

class Direction(Enum):
    up = "U"
    down = "D"
    left = "L"
    right = "R"

@dataclass
class Segment:
    direction: Direction
    length: int
    color: int

    def __init__(self, input_string: str):
        match = re.match(r"([UDLR]) (\d+) \(\#(.*)\)", input_string)
        assert match is not None
        groups = match.groups()
        self.direction = Direction(groups[0])
        self.length = int(groups[1])
        self.color = int(groups[2], base=16)

def get_next_position(x: int, y: int, segment: Segment):
    match segment.direction:
        case Direction.up:
            y -= segment.length
        case Direction.down:
            y += segment.length
        case Direction.left:
            x -= segment.length
        case Direction.right:
            x += segment.length
    return x, y

f = open("day18-input.txt")
all_lines = f.readlines()
all_segments = [Segment(line) for line in all_lines if len(line) > 0]

current_position = (0, 0)
trench_positions: Set[Tuple[int, int]] = set([current_position])
lava_positions: Set[Tuple[int, int]] = set([current_position])

# the starting point of the flood fill is arbitrary but hopefully it's within the lake
positions_to_examine: Set[Tuple[int, int]] = set([(1, 1)])

for segment in all_segments:
    x_old = current_position[0]
    y_old = current_position[1]
    x_new, y_new = get_next_position(x_old, y_old, segment)
    xs_to_mark = range(min(x_old, x_new), max(x_old, x_new) + 1)
    ys_to_mark = range(min(y_old, y_new), max(y_old, y_new) + 1)
    for x in xs_to_mark:
        for y in ys_to_mark:
            trench_positions.add((x, y))
            lava_positions.add((x,y))
    current_position = (x_new, y_new)

while len(positions_to_examine) > 0:
    x, y = positions_to_examine.pop()
    # print(f"{len(positions_to_examine)} {len(lava_positions)}")
    if (x, y) not in lava_positions:
        lava_positions.add((x, y))
        positions_to_examine.add((x - 1, y))
        positions_to_examine.add((x + 1, y))
        positions_to_examine.add((x, y - 1))
        positions_to_examine.add((x, y + 1))

print(len(lava_positions))