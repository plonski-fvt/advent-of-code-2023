from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
    north = 0
    east = 1
    south = 2
    west = 3

@dataclass
class LaserBeam:
    row: int
    col: int
    direction: Direction

    def propagate_forward(self):
        match self.direction:
            case Direction.north:
                self.row -= 1
            case Direction.east:
                self.col += 1
            case Direction.south:
                self.row += 1
            case Direction.west:
                self.col -= 1

    def __repr__(self):
        return f"{self.row} {self.col} {self.direction}"

f = open("day16-input.txt")
all_lines = f.readlines()
cols = len(all_lines[0])
all_lines = [l.strip() for l in all_lines if len(l) == cols]
cols = len(all_lines[0])
rows = len(all_lines)

print(rows, cols)

lava_array = [cols * [False] for _ in range(rows)]

lasers_already_processed = set()
lasers_to_process = [LaserBeam(0, 0, Direction.east)]

while len(lasers_to_process) > 0:
    laser = lasers_to_process.pop()
    if laser.__repr__() in lasers_already_processed:
        continue
    lasers_already_processed.add(laser.__repr__())
    if laser.row < 0 or laser.col < 0 or laser.row >= rows or laser.col >= cols:
        # it's easier to deal with this when expanding the laser rather than trying
        # to ensure it doesn't get added in the first place
        continue
    print(laser.__repr__())
    lava_array[laser.row][laser.col] = True
    c = all_lines[laser.row][laser.col]
    if c == ".":
        laser.propagate_forward()
        lasers_to_process.append(laser)
    elif c == "/":
        match laser.direction:
            case Direction.north:
                laser.direction = Direction.east
            case Direction.east:
                laser.direction = Direction.north
            case Direction.south:
                laser.direction = Direction.west
            case Direction.west:
                laser.direction = Direction.south
        laser.propagate_forward()
        lasers_to_process.append(laser)
    elif c == "\\":
        match laser.direction:
            case Direction.north:
                laser.direction = Direction.west
            case Direction.east:
                laser.direction = Direction.south
            case Direction.south:
                laser.direction = Direction.east
            case Direction.west:
                laser.direction = Direction.north
        laser.propagate_forward()
        lasers_to_process.append(laser)
    elif c == "-":
        if laser.direction in [Direction.north, Direction.south]:
            laser_a = LaserBeam(laser.row, laser.col, Direction.west)
            laser_b = LaserBeam(laser.row, laser.col, Direction.east)
            laser_a.propagate_forward()
            laser_b.propagate_forward()
            lasers_to_process.append(laser_a)
            lasers_to_process.append(laser_b)
        else:
            laser.propagate_forward()
            lasers_to_process.append(laser)
    elif c == "|":
        if laser.direction in [Direction.east, Direction.west]:
            laser_a = LaserBeam(laser.row, laser.col, Direction.north)
            laser_b = LaserBeam(laser.row, laser.col, Direction.south)
            laser_a.propagate_forward()
            laser_b.propagate_forward()
            lasers_to_process.append(laser_a)
            lasers_to_process.append(laser_b)
        else:
            laser.propagate_forward()
            lasers_to_process.append(laser)


lava_sum = sum([sum([1 for x in row if x]) for row in lava_array])

print(lava_sum)