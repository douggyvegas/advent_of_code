from dataclasses import dataclass
import time
import re
from typing import List, Optional, Tuple

class Map:
    sourceType: str
    destType:str
    conversions: List[Tuple[range, range]]
    
    def __init__(self, sourceType, destType):
        self.conversions = []
        self.sourceType = sourceType
        self.destType = destType

    def can_convert(self, sourceType) -> bool:
        return (sourceType == self.sourceType)

    def convert_ranges(self, source_range: range) -> Tuple[List[range], str]:
        source_ranges = [ ]
        dest_ranges = [ ]
        for c in self.conversions:
            i = range(max(source_range.start, c[0].start), min(source_range.stop, c[0].stop))
            if len(i) > 0:
                source_ranges.append(i)
                dest_ranges.append(range(i.start - c[0].start + c[1].start, i.stop - c[0].stop + c[1].stop))

        if len(source_ranges) > 0:
            source_ranges = [ d for d in source_ranges if len(d) > 0 ]
            source_ranges.sort(key = lambda i: i.start)
            dest_ranges.insert(0, range(source_range.start, source_ranges[0].start))
            dest_ranges.append(range(source_ranges[-1].stop, source_range.stop))

        for i in range(1, len(source_ranges)):
            dest_ranges.append(range(source_ranges[i - 1].stop, source_ranges[i].start))

        dest_ranges = [ d for d in dest_ranges if len(d) > 0 ]

        if len(dest_ranges) == 0:
            dest_ranges = [ source_range ]

        return (dest_ranges, self.destType)

class MapChain:
    maps: List[Map]

    def __init__(self):
        self.maps = []

    def convert_range(self, seed_range: range) -> List[range]:
        dest_ranges = [ seed_range ]
        destType = "seed"
        while destType != "location":
            source_ranges = dest_ranges
            sourceType = destType
            for map in self.maps:
                if map.can_convert(sourceType):
                    dest_ranges = [ ]
                    for source_range in source_ranges:
                        new_dest_ranges, destType = map.convert_ranges(source_range)
                        dest_ranges += new_dest_ranges
                    break
        return dest_ranges

def main():
    seeds_ranges_part_1 = []
    seeds_ranges_part_2 = []
    maps = MapChain()
    currentMap = None
    with open("05.in") as input:
        for line in input.read().splitlines():
            if line != "":
                if line.startswith("seeds: "):
                    seeds = [ int(s) for s in re.findall(r'\d+', line) ]
                    seeds_ranges_part_1 = [ range(s, s + 1) for s in seeds ]
                    seeds_ranges_part_2 = [ range(seeds[n], seeds[n] + seeds[n+1]) for n in range(0, len(seeds), 2) ]
                else:
                    matches = re.findall(r'(\w+)-to-(\w+) map:', line)
                    if matches:
                        currentMap = Map(matches[0][0], matches[0][1])
                        maps.maps.append(currentMap)
                    else:
                        matches = re.findall(r'\d+', line)
                        if matches and currentMap is not None:
                            dst = int(matches[0])
                            src = int(matches[1])
                            rng = int(matches[2])
                            currentMap.conversions.append((range(src, src + rng), range(dst, dst + rng)))

    optimal_location_part1 = min([ location_range.start  for seeds_range in seeds_ranges_part_1 for location_range in maps.convert_range(seeds_range) ])
    print(f"part 1: {optimal_location_part1}")

    location_ranges = [ ]
    for i, seed_range in enumerate(seeds_ranges_part_2):
        print(f"converting seed range {i+1}/{len(seeds_ranges_part_2)}")
        location_ranges += maps.convert_range(seed_range)
    
    optimal_location_part2 = min([ location_range.start for seeds_range in seeds_ranges_part_2 for location_range in maps.convert_range(seeds_range) ])

    print(f"part 2: {optimal_location_part2}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")