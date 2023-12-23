from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue

class Direction(Enum):
    north = 0
    east = 1
    south = 2
    west = 3

@dataclass
class TableEntry:
    row: int
    col: int
    direction: Direction
    speed: int

    def __repr__(self):
        return f"{self.row} {self.col} {self.direction if self.speed > 0 else ''} {self.speed}"
    
    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

f = open("day17-input.txt")
all_lines = f.readlines()
cols = len(all_lines[0])
all_lines = [[int(c) for c in l.strip()] for l in all_lines if len(l) == cols]
cols = len(all_lines[0])
rows = len(all_lines)

queue = PriorityQueue()
entries_visited = set()
queue.put((0, TableEntry(0, 1, Direction.east, 1)))
queue.put((0, TableEntry(1, 0, Direction.south, 1)))

while not queue.empty():
    priority, entry = queue.get()
    print(priority, entry)
    if entry.__repr__() in entries_visited:
        continue
    entries_visited.add(entry.__repr__())
    if entry.speed > 10:
        continue
    if entry.row < 0 or entry.col < 0 or entry.row >= rows or entry.col >= cols:
        continue
    priority += all_lines[entry.row][entry.col]
    if entry.row == rows - 1 and entry.col == cols - 1 and entry.speed >= 4:
        print(priority)
        break
    valid_directions = []
    if entry.speed < 4:
        valid_directions = [entry.direction]
    else:
        if entry.direction != Direction.north:
            valid_directions.append(Direction.south)
        if entry.direction != Direction.east:
            valid_directions.append(Direction.west)
        if entry.direction != Direction.south:
            valid_directions.append(Direction.north)
        if entry.direction != Direction.west:
            valid_directions.append(Direction.east)
    for direction in valid_directions:
        if direction == entry.direction:
            speed = entry.speed + 1
        else:
            speed = 1
        row = entry.row
        col = entry.col
        match direction:
            case Direction.north:
                queue.put((priority, TableEntry(row - 1, col, direction, speed)))
            case Direction.east:
                queue.put((priority, TableEntry(row, col + 1, direction, speed)))
            case Direction.south:
                queue.put((priority, TableEntry(row + 1, col, direction, speed)))
            case Direction.west:
                queue.put((priority, TableEntry(row, col - 1, direction, speed)))



