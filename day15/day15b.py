import re
from dataclasses import dataclass
from typing import List, Optional

def hash_algorithm(input: str):
    current_value = 0
    for c in input:
        assert c != "\n"
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

@dataclass
class Lens:
    label: str
    focal_length: Optional[int]

print(hash_algorithm("HASH"))

# input_lines = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")

f = open("day15-input.txt")
input_lines = f.readlines()[0].split(",")

boxes: List[List[Lens]] = [[] for _ in range(256)]

for line in input_lines:
    parsed_line = re.match(r"([a-z]+)([\=\-])(\d?)", line)
    assert parsed_line is not None
    groups = parsed_line.groups()
    lens = Lens(groups[0], int(groups[2]) if len(groups[2]) > 0 else None)
    lens_box = boxes[hash_algorithm(lens.label)]
    labels_in_box = [x.label for x in lens_box]
    try:
        index_in_box = labels_in_box.index(lens.label)
        if lens.focal_length is None:
            del lens_box[index_in_box]
        else:
            lens_box[index_in_box] = lens
    except ValueError:
        if lens.focal_length:
            lens_box.append(lens)

result = 0

for box_index, box in enumerate(boxes):
    for slot_index, lens in enumerate(box):
        assert lens.focal_length is not None
        result += (1 + box_index) * (1 + slot_index) * lens.focal_length

print(boxes)

print(result)