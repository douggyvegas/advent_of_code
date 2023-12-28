import time
import re
from typing import List

def find_patterns(pattern: List[str], diff_count: int) -> int:
    found_row = 0
    for potential_mirror in range(1, len(pattern)):
        diffs = 0
        for row in range(0, potential_mirror):
            target = potential_mirror + potential_mirror - 1 - row
            if target < len(pattern):
                diffs += sum(1 for a, b in zip(pattern[row], pattern[target]) if a != b)
        if diffs == diff_count:
            found_row = potential_mirror
            break
    return found_row

def main():
    patterns : List[List[str]] = [ ]
    with open("13.in") as input:
        pattern : List[str] = [ ]
        for row in input.read().splitlines():
            if len(row) == 0:
                patterns.append(pattern)
                pattern = [ ]
            else:
                pattern.append(row)
        patterns.append(pattern)

    part_1 = 0
    for pattern in patterns:
        row = find_patterns(pattern, 0)
        part_1 += 100 * row
        row = find_patterns([''.join(s) for s in zip(*pattern)], 0)
        part_1 += row

    part_2 = 0
    for pattern in patterns:
        row = find_patterns(pattern, 1)
        part_2 += 100 * row
        row = find_patterns([''.join(s) for s in zip(*pattern)], 1)
        part_2 += row

    print(f"part 1: {part_1}")
    print(f"part 2: {part_2}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")