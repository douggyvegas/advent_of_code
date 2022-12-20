#!/usr/bin/env python3

from copy import deepcopy
from itertools import cycle
import time

def getSlice(s: int):
    return "{0:09b}".format(s).replace("0", " ").replace("1", "#")

def main():
    
    with open('17.in') as input:
        for line in input.read().splitlines():
            gas_jets = cycle(line)

    rocks = [ ] # horizontal slices (bitmasks) bottom to top
    rocks.append([ 15 << 2 ])
    rocks.append([ 2 << 3, 7 << 3, 2 << 3 ])
    rocks.append([ 7 << 3, 1 << 3, 1 << 3 ])
    rocks.append([ 1 << 5, 1 << 5, 1 << 5, 1 << 5 ])
    rocks.append([ 3 << 4, 3 << 4 ])

    rocks = cycle(rocks)

    cave = [ 257 ] * 3

    dropped_lines = 0
    for count in range(1000000000000):
        # print("==== STEP", count, "====")
        # print(dropped_lines)
        # for c in reversed(cave):
        #     print(getSlice(c))
        # print("")

        acc = 0
        lowest = 0
        for i in range(len(cave)):
            acc |= cave[len(cave) - 1 - i]
            if acc == 511:
                lowest = len(cave) - 1 - i
                break
        
        if lowest != 0:
            cave = cave[lowest::]
            dropped_lines += lowest

        highest = max([ 0 ] + [ i for i in range(len(cave)) if cave[i] & 254 != 0 ])

        # print(highest)
        rock_y = highest + 4
        next_rock = deepcopy(next(rocks))
        if len(cave) < rock_y + len(next_rock):
            cave += [ 257 ] * (rock_y + len(next_rock) - len(cave))
        while True:
            gas_jet = next(gas_jets)
            # print("gas_jet", gas_jet)
            previous_rock = deepcopy(next_rock)
            next_rock = [ s << 1 if gas_jet == "<" else s >> 1 for s in next_rock ]
            # print("r,nr =", [ getSlice(s) for s in previous_rock ], [ getSlice(s) for s in next_rock ])
            if any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                next_rock = previous_rock
            rock_y -= 1
            if rock_y == 0 or any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                for i, s in enumerate(next_rock):
                    cave[ rock_y + 1 + i ] |= s
                break
            
    highest = dropped_lines + max([ i for i in range(len(cave)) if cave[i] & 254 != 0 ])
    print(highest)



start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")