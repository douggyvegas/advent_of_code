from copy import copy
from dataclasses import dataclass
import time
from typing import List, Set, Tuple

directions = [ (0,1),(1,0),(0,-1),(-1,0) ]

def solve(grid: List[List[str]], starting_beam: Tuple[int, int, int]) -> int:
    width = len(grid[0])
    height = len(grid)

    # beam: direction, row, column
    history: Set[Tuple[int, int, int]] = set() 
    beams: Set[Tuple[int, int, int]] = set()

    beams.add(starting_beam)

    def next_beam(direction: int, beam: Tuple[int, int, int]):
        next = ((direction, beam[1] + directions[direction][0], beam[2] + directions[direction][1]))
        if 0 <= next[1] < width and 0 <= next[2] < height:
            beams.add(next)

    while len(beams) > 0:
        # print('------------------------------------------------------')
        # for row, line in enumerate(grid):
        #     disp = copy(line)
        #     for col, _ in enumerate(line):
        #         if (row, col) in [ (beam[1], beam[2]) for beam in history ]:
        #             disp[col] = '#'
        #     print(''.join(disp))

        beam = beams.pop()
        if beam not in history:
            history.add(beam)
            match grid[beam[1]][beam[2]]:
                case '|':
                    if beam[0] == 0 or beam[0] == 2:
                        next_beam(1, beam)
                        next_beam(3, beam)
                    else:
                        next_beam(beam[0], beam)
                case '-':
                    if beam[0] == 1 or beam[0] == 3:
                        next_beam(0, beam)
                        next_beam(2, beam)
                    else:
                        next_beam(beam[0], beam)
                case '/':
                    if beam[0] == 0:
                        next_beam(3, beam)
                    elif beam[0] == 1:
                        next_beam(2, beam)
                    elif beam[0] == 2:
                        next_beam(1, beam)
                    elif beam[0] == 3:
                        next_beam(0, beam)
                case '\\':
                    if beam[0] == 0:
                        next_beam(1, beam)
                    elif beam[0] == 1:
                        next_beam(0, beam)
                    elif beam[0] == 2:
                        next_beam(3, beam)
                    elif beam[0] == 3:
                        next_beam(2, beam)
                case '.':
                    next_beam(beam[0], beam)

    energyzed_tiles = len(set([ (beam[1], beam[2]) for beam in history ]))
    return energyzed_tiles

def main():
    grid: List[List[str]] = []
    with open("16.in") as input:
        for line in input.read().splitlines():
            grid.append(list(line))

    # print('------------------------------------------------------')
    # for row, line in enumerate(grid):
    #     for col, _ in enumerate(line):
    #         if (row, col) in [ (beam[1], beam[2]) for beam in history ]:
    #             line[col] = '#'
    #     print(''.join(line))

    energyzed_tiles = solve(grid, (0, 0, 0))
    print(f"part 1: {energyzed_tiles}")

    energyzed_tiles = 0
    for col in range(len(grid[0])):
        energyzed_tiles = max(energyzed_tiles, solve(grid, (1, 0, col)), solve(grid, (3, len(grid) - 1, col)))
    for row in range(len(grid)):
        energyzed_tiles = max(energyzed_tiles, solve(grid, (0, row, 0)), solve(grid, (2, row, len(grid[0]) - 1)))

    print(f"part 2: {energyzed_tiles}")


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")