#!/usr/bin/env python3

from copy import deepcopy
from itertools import pairwise
import time


def main():
    snakes = []
    with open('14.in') as input:
        for input_line in input.read().splitlines():
            snakes.append([ tuple([ int(c) for c in coords.split(',') ]) for coords in input_line.split(" -> ") ])

    flat_snakes = [ coords for lines in snakes for coords in lines ] + [(500,0)]
    cmin = (min(c[0] for c in flat_snakes), min(c[1] for c in flat_snakes))
    cmax = (max(c[0] for c in flat_snakes), max(c[1] for c in flat_snakes))

    grid = [ [ '.' for x in range(cmin[0], cmax[0] + 1)] for y in range(cmin[1], cmax[1] + 1) ]
    for snake in snakes:
        for p1, p2 in pairwise(snake):
            if p1[0] == p2[0]:
                v = sorted([ p1[1], p2[1] ])
                for y in range(v[0], v[1] + 1):
                    grid[y - cmin[1]][p1[0] - cmin[0]] = '#'
            if p1[1] == p2[1]:
                h = sorted([ p1[0], p2[0] ])
                for x in range(h[0], h[1] + 1):
                    grid[p1[1] - cmin[1]][x - cmin[0]] = '#'

    source = [ 500 - cmin[0], 0 - cmin[1] ]
    print("part 1:", theSandIsFalling(deepcopy(grid), source, False) - 1)

    grid.append([ '.' for x in range(len(grid[0]))])
    grid.append([ '#' for x in range(len(grid[0]))])
    print("part 2:", theSandIsFalling(grid, source, True))

def theSandIsFalling(grid, source, infinite_floor):
    width = len(grid[0])
    height = len(grid)
    directions = [ [0,1], [-1,1], [1,1] ]
    sand_units_count = 0
    end = False
    while not end:
        sand_units_count += 1
        sand = source
        sand_unit_blocked = False
        while not sand_unit_blocked and not end:
            sand_unit_blocked = True
            for direction in directions:
                next_pos = [ sand[0] + direction[0], sand[1] + direction[1] ]
                if not infinite_floor:
                    if next_pos[0] < 0 or next_pos[0] >= width or next_pos[1] < 0 or next_pos[1] >= height:
                        end = True
                        break
                elif next_pos[0] < 0 or next_pos[0] >= width:
                    growth_empty = [ '.' for _ in range(width // 2) ]
                    growth_rock = [ '#' for _ in range(width // 2) ]
                    if next_pos[0] >= width:
                        for y in range(height):
                            grid[y] += growth_empty if y < height - 1 else growth_rock
                    else:
                        next_pos[0] += width // 2
                        source[0] += width // 2
                        for y in range(height):
                            grid[y] = (growth_empty if y < height - 1 else growth_rock) + grid[y]
                    width += width // 2

                if grid[next_pos[1]][next_pos[0]] == '.':
                    sand = next_pos
                    sand_unit_blocked = False
                    break

            if sand_unit_blocked:
                grid[sand[1]][sand[0]] = "o"
                if sand[0] == source[0] and sand[1] == source[1]:
                    end = True


    print("")
    for line in grid:
        print(' '.join(line))

    return sand_units_count

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
