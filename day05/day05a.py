from dataclasses import dataclass
from typing import List
import re

@dataclass
class RangeMap:
    destination_start: int
    source_start: int
    length: int
    
    def map(self, source_id: int):
        if source_id < self.source_start:
            return None
        if source_id >= self.source_start + self.length:
            return None
        return source_id - self.source_start + self.destination_start
    
class RangeMapSet:
    range_maps: List[RangeMap]

    def __init__(self, lines: List[str]):
        self.range_maps = []
        for line in lines:
            vals = re.match(r"(\d+) (\d+) (\d+)", line)
            assert vals is not None
            self.range_maps.append(RangeMap(int(vals.groups()[0]), 
                                            int(vals.groups()[1]), 
                                            int(vals.groups()[2])))

    def map(self, source_id: int):
        for range_map in self.range_maps:
            candidate_dest = range_map.map(source_id)
            if candidate_dest is not None:
                return candidate_dest
        # if not found in any maps, return the source
        return source_id
    
def map_seed_to_location(seed_id: int, sequential_maps: List[RangeMapSet]):
    working_id = seed_id
    for map in sequential_maps:
        working_id = map.map(working_id)
    return working_id

f = open("day05-input.txt")

all_lines = f.readlines()

seeds_as_strs = re.findall(r"(\d+)", all_lines[0])
seeds = [int(x) for x in seeds_as_strs]

seed_to_soil = RangeMapSet(all_lines[3:20])
soil_to_fertilizer = RangeMapSet(all_lines[22:31])
fertilizer_to_water = RangeMapSet(all_lines[33:73])
water_to_light = RangeMapSet(all_lines[75:99])
light_to_temperature = RangeMapSet(all_lines[101:121])
temperature_to_humidity = RangeMapSet(all_lines[123:167])
humidity_to_location = RangeMapSet(all_lines[169:210])

sequential_maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]

closest = 99999999999
for seed in seeds:
    location = map_seed_to_location(seed, sequential_maps)
    print(location)
    if location < closest:
        closest = location

print(closest)