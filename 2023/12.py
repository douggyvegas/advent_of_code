import time
import re
from typing import Tuple
from functools import lru_cache

@lru_cache
def count_arrangements(row: str, damaged_springs: int, next_groups: Tuple[int]) -> int:
    if len(row) == 0:
        if len(next_groups) == 0:
            # no more groups and row is finished => we found a valid arrangement
            return 1
        elif len(next_groups) == 1 and damaged_springs == next_groups[0]:
            # one last group and damaged_springs is valid
            return 1
        else:
            # there are remaining groups but no more character in row => invalid arrangement
            return 0
    
    if row[0] == "#":
        if len(next_groups) == 0:
            # there are no remaining groups but we still found a damaged spring
            return 0
        # damaged spring
        if damaged_springs > next_groups[0]:
            # too many damaged springs => invalid arrangement
            return 0
        return count_arrangements(row[1:], damaged_springs + 1, next_groups)
    
    if row[0] == ".":
        # ok spring
        if damaged_springs != 0:
            # group is finished => new group
            if damaged_springs == next_groups[0]:
                return count_arrangements(row[1:], 0, tuple(list(next_groups)[1:]))
            else:
                # invalid arrangement
                return 0
        else:
            return count_arrangements(row[1:], damaged_springs, next_groups)

    if row[0] == "?":
        valid_arrangements = 0
        row = '.' + row[1:]
        valid_arrangements += count_arrangements(row, damaged_springs, next_groups)
        row = '#' + row[1:]
        valid_arrangements += count_arrangements(row, damaged_springs, next_groups)
        return valid_arrangements
    
    return 0

def main():
    total_arrangements_part_1 = 0
    total_arrangements_part_2 = 0
    with open("12.in") as input:
        for line in input.read().splitlines():
            print(f"{line}")
            tokens = line.split(" ")
            row = tokens[0]
            groups = tokens[1].split(",")
            total_arrangements_part_1 += count_arrangements(row, 0, tuple([ int(g) for g in groups ]))
            total_arrangements_part_2 +=  count_arrangements("?".join([ row ] * 5), 0, tuple([ int(g) for g in groups ] * 5))

    print(f"part 1: {total_arrangements_part_1}")
    print(f"part 2: {total_arrangements_part_2}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")