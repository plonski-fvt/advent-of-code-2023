from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class IdRange:
    start_id: int
    length: int

    def __init__(self, start_id, length):
        self.start_id = start_id
        self.length = length
        assert length > 0

@dataclass
class QueryResult:
    mapped_result: Optional[IdRange]
    unmatched_ids: List[IdRange]

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
    
    def map_range(self, source_range: IdRange) -> QueryResult:
        if source_range.start_id + source_range.length <= self.source_start:
            return QueryResult(None, [source_range])
        if self.source_start + self.length <= source_range.start_id:
            return QueryResult(None, [source_range])
        lower_intersection = max(source_range.start_id, self.source_start)
        upper_intersection = min(source_range.start_id + source_range.length, 
                                 self.source_start + self.length)
        mapped_result = IdRange(lower_intersection + self.destination_start - self.source_start,
                               upper_intersection - lower_intersection)
        unmatched_ids = []
        if source_range.start_id < lower_intersection:
            unmatched_ids.append(IdRange(source_range.start_id, 
                                         lower_intersection - source_range.start_id))
        if source_range.start_id + source_range.length > upper_intersection:
            unmatched_ids.append(IdRange(upper_intersection, 
                                         source_range.start_id + source_range.length - upper_intersection))

        return QueryResult(mapped_result, unmatched_ids)    
    
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
    
    def map_range(self, source_range: IdRange):
        mapped_results: List[IdRange] = []
        unmatched_ranges = [source_range]
        for range_map in self.range_maps:
            for unmatched_range in unmatched_ranges:
                result = range_map.map_range(unmatched_range)
                if result.mapped_result is not None:
                    mapped_results.append(result.mapped_result)
                    unmatched_ranges = unmatched_ranges + result.unmatched_ids
                    unmatched_ranges.remove(unmatched_range)
        return mapped_results + unmatched_ranges

    
def map_seed_to_location(seed_id: int, sequential_maps: List[RangeMapSet]):
    working_id = seed_id
    for map in sequential_maps:
        working_id = map.map(working_id)
    return working_id

def map_seed_range_to_location(seed_range: IdRange, sequential_maps: List[RangeMapSet]):
    range_list = [seed_range]
    for map in sequential_maps:
        print("input range list: ", range_list)
        next_range_list: List[IdRange] = []
        for range in range_list:
            next_range_list = next_range_list + map.map_range(range)
        range_list = next_range_list
        print("output range list", range_list)
    return range_list

f = open("day05-input.txt")

all_lines = f.readlines()

seeds_as_strs = re.findall(r"(\d+) (\d+)", all_lines[0])
seeds = [IdRange(int(x[0]), int(x[1])) for x in seeds_as_strs]

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
    locations = map_seed_range_to_location(seed, sequential_maps)
    min_location = min([x.start_id for x in locations])
    print(min_location)
    if min_location < closest:
        closest = min_location

print(closest)