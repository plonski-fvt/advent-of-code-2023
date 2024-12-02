from dataclasses import dataclass
from enum import Enum
from typing import Set, Tuple, List
import re

class Direction(Enum):
    right = "0"
    down = "1"
    left = "2"
    up = "3"

@dataclass
class Segment:
    direction: Direction
    length: int

    def __init__(self, input_string: str):
        match = re.match(r"[UDLR] \d+ \(\#(.....)(\d)\)", input_string)
        assert match is not None
        groups = match.groups()
        self.length = int(groups[0], base=16)
        self.direction = Direction(groups[1])


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

@dataclass
class LineSegment:
    horizontal: bool
    xs: Tuple[int, int]
    ys: Tuple[int, int]

    # we sort based on leftmost x axis
    def __lt__(self, other):
        return min(self.xs) < min(other.xs)
    
    def __init__(self, x: int, y: int, segment: Segment):
        self.horizontal = segment.direction in [Direction.left, Direction.right]
        x_new, y_new = get_next_position(x, y, segment)
        self.xs = (x, x_new)
        self.ys = (y, y_new)

class AxisAlignedLoop:
    line_segments: List[LineSegment]

    def __init__(self, segments: List[Segment]):
        x = 0
        y = 0
        self.line_segments = []
        for segment in segments:
            line_segment = LineSegment(x, y, segment)
            x = line_segment.xs[1]
            y = line_segment.ys[1]
            # we don't actually need to save the horizontal ones
            if not line_segment.horizontal:
                # we ensure our line segment ys are sorted low to high
                if line_segment.ys[0] > line_segment.ys[1]:
                    line_segment.ys = (line_segment.ys[1], line_segment.ys[0])
                self.line_segments.append(line_segment)

    def compute_area(self):
        list.sort(self.line_segments)
        current_x_coord = min(self.line_segments[0].xs)

        print(self.line_segments)
        print(current_x_coord)
        # these are always disjoint
        active_y_ranges: List[Tuple[int, int]] = []
        area_so_far = 0
        for line_segment in self.line_segments:
            assert not line_segment.horizontal

            # if this line segment intersects with an active range
            # it might expand it, contract it, or split it in two
            # note it's possible that after expanding, two ranges will be adjacent
            # in this case they should be combined after

            print(f"{current_x_coord} {line_segment.xs[0]} {line_segment.xs[0] - current_x_coord}")

            found_match = False
            next_y_ranges = []
            for range in active_y_ranges:
                area_so_far += (1 + range[1] - range[0]) * (line_segment.xs[0] - current_x_coord)
                if found_match:
                    next_y_ranges.append(range)
                    continue
                matched_part = (max(line_segment.ys[0], range[0]), min(line_segment.ys[1], range[1]))
                if matched_part[0] > matched_part[1]:
                    # no match, so skip
                    next_y_ranges.append(range)
                    continue
                found_match = True
                # expansion
                if line_segment.ys[1] == range[0]:
                    next_y_ranges.append((line_segment.ys[0], range[1]))
                    area_so_far += line_segment.ys[1] - line_segment.ys[0]
                elif line_segment.ys[0] == range[1]:
                    next_y_ranges.append((range[0], line_segment.ys[1]))
                    area_so_far += line_segment.ys[1] - line_segment.ys[0]
                # contraction
                elif line_segment.ys[0] == range[0] and line_segment.ys[1] == range[1]:
                    pass # don't append anything, this range should be deleted
                elif line_segment.ys[0] == range[0]:
                    next_y_ranges.append((line_segment.ys[1], range[1]))
                elif line_segment.ys[1] == range[1]:
                    next_y_ranges.append((range[0], line_segment.ys[0]))
                # split
                else:
                    next_y_ranges.append((range[0], matched_part[0]))
                    next_y_ranges.append((matched_part[1], range[1]))
            
            print(f"{area_so_far} {current_x_coord} {line_segment.ys} : {active_y_ranges}")

            #if area_so_far > 1000000000000:
            #    exit(0)

            if not found_match:
                next_y_ranges.append(line_segment.ys)
                area_so_far += 1 + line_segment.ys[1] - line_segment.ys[0]

            if len(next_y_ranges) == 0:
                continue

            current_x_coord = line_segment.xs[0]

            list.sort(next_y_ranges)

            consolidated_y_ranges = []

            working_range = next_y_ranges[0]

            for range in next_y_ranges[1:]:
                if working_range[1] == range[0]:
                    working_range = (working_range[0], range[1])
                else:
                    consolidated_y_ranges.append(working_range)
                    working_range = range
            
            consolidated_y_ranges.append(working_range)
            active_y_ranges = consolidated_y_ranges

        return area_so_far

f = open("day18-input.txt")
# f = open("day18-test.txt")
# f = open("day18-test2.txt")
# f = open("day18-test3.txt")
all_lines = f.readlines()
all_segments = [Segment(line) for line in all_lines if len(line) > 0]

# print(all_segments)

loop = AxisAlignedLoop(all_segments)
area = loop.compute_area()
print(area)

print(952408144115 - area)