from functools import cache
import time
import re
from typing import List,Tuple

first_cycle = True

@cache
def tilt(round_rocks: Tuple[Tuple[int, int], ...], cube_rocks: Tuple[Tuple[int, int], ...]) -> List[Tuple[int, int]]:
    moved_rocks = []
    rocks = sorted(list(round_rocks))
    while len(rocks) > 0:
        rock = rocks.pop(0)
        if rock in moved_rocks:
            break
        if rock[0] == 0 or (rock[0] - 1,rock[1]) in moved_rocks or (rock[0] - 1, rock[1]) in cube_rocks:
            moved_rocks.append(rock)
        else:
            rocks.append((rock[0] - 1, rock[1]))
    
    return moved_rocks
        

@cache
def rotate(round_rocks: Tuple[Tuple[int, int], ...], 
           cube_rocks: Tuple[Tuple[int, int], ...],
           height: int, width: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], int, int]:

        return (
             [(j, height - i - 1) for i, j in round_rocks],
             [(j, height - i - 1) for i, j in cube_rocks],
             width,
             height ) 


@cache
def do_cycle(round_rocks: Tuple[Tuple[int, int], ...], 
           cube_rocks: Tuple[Tuple[int, int], ...],
           height: int, width: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], int, int]:
    global first_cycle
    new_round_rocks = list(round_rocks)
    new_cube_rocks = list(cube_rocks)
    for i in range(4):
        new_round_rocks = tilt(tuple(new_round_rocks), tuple(new_cube_rocks))
        if first_cycle and i == 0:
            print(f"part 1: {get_load(new_round_rocks, height)}")
            first_cycle = False
        new_round_rocks, new_cube_rocks, width, height = rotate(tuple(new_round_rocks), tuple(new_cube_rocks), width, height)

    return (new_round_rocks, new_cube_rocks, width, height)

@cache
def do_N_cycles(cycles_count: int, round_rocks: Tuple[Tuple[int, int], ...], 
           cube_rocks: Tuple[Tuple[int, int], ...],
           height: int, width: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]], int, int]:
    print(f"do_N_cycles({cycles_count}, ...)")
    new_round_rocks = list(round_rocks)
    new_cube_rocks = list(cube_rocks)
    if cycles_count <= 10:
        for _ in range(cycles_count):
            new_round_rocks, new_cube_rocks, width, height = do_cycle(tuple(new_round_rocks), tuple(new_cube_rocks), height, width)
    else:
        for _ in range(10):
            new_round_rocks, new_cube_rocks, width, height = do_N_cycles(cycles_count // 10, tuple(new_round_rocks), tuple(new_cube_rocks), height, width)

    return (new_round_rocks, new_cube_rocks, width, height)

def get_load(rocks : List[Tuple[int, int]], height: int) -> int:
    load = 0
    for rock in rocks:
        load += height - rock[0]
    return load

def main():
    round_rocks : List[Tuple[int, int]]= [ ]
    cube_rocks : List[Tuple[int, int]]= [ ]
    with open("14.in") as input:
        row = 0
        width = 0
        for line in input.read().splitlines():
            width = len(line)
            for col, c in enumerate(line):
                if c == '#':
                    cube_rocks.append((row, col))
                elif c == 'O':
                    round_rocks.append((row, col))
            row += 1
        height = row

    round_rocks, cube_rocks, width, height = do_N_cycles(1000000000, tuple(round_rocks), tuple(cube_rocks), width, height)            

    load_part_2 = get_load(round_rocks, height)

    print(f"part 2: {load_part_2}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")