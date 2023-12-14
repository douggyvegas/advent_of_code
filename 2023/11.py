import copy
import time
import re
from typing import List

def solve(stars: List[List[int]], width, height, expansion_rate) -> int:
    empty_rows = [ n for n in range(height) if all(s[0] != n for s in stars) ]
    empty_cols = [ n for n in range(width) if all(s[1] != n for s in stars) ]

    for star in stars:
        row_expansion = len([ r for r in empty_rows if r < star[0] ]) * (expansion_rate - 1)
        col_expansion = len([ c for c in empty_cols if c < star[1] ]) * (expansion_rate - 1)
        star[0] += row_expansion
        star[1] += col_expansion

    total = 0
    for i1 in range(len(stars)):
        s1 = stars[i1]
        for i2 in range(i1 + 1, len(stars)):
            s2 = stars[i2]
            distance = abs(s2[0] - s1[0]) + abs(s2[1] - s1[1]) 
            total += distance

    return total

def main():
    stars_part1 = [ ]
    width = 0
    height = 0
    with open("11.in") as input:
        lines = input.read().splitlines()
        height = len(lines)
        width = len(lines[0])
        for row, line in enumerate(lines):
            for col in [ m.start() for m in re.finditer(r"#", line) ]:
                stars_part1 += [ [row, col] ]

    stars_part2 = copy.deepcopy(stars_part1)

    print(f"part 1: {solve(stars_part1, width, height, 2)}")
    print(f"part 2: {solve(stars_part2, width, height, 1000000)}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")