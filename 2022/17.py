#!/usr/bin/env python3

from copy import deepcopy
from itertools import cycle
import time

def getSlice(s: int):
    return "{0:09b}".format(s).replace("0", " ").replace("1", "#")

def main():
    
    with open('17.in') as input:
        for line in input.read().splitlines():
            gas_jets = list(line)

    rocks = [ ] # horizontal slices (bitmasks) bottom to top
    rocks.append([ 15 << 2 ])
    rocks.append([ 2 << 3, 7 << 3, 2 << 3 ])
    rocks.append([ 7 << 3, 1 << 3, 1 << 3 ])
    rocks.append([ 1 << 5, 1 << 5, 1 << 5, 1 << 5 ])
    rocks.append([ 3 << 4, 3 << 4 ])

    cave = [ 257 ] * 3

    known_configurations = { }
    current_gas_jet_index = 0
    cycle = 0
    base_target = 1E12
    target = base_target
    cycle_length = target
    cycle_height = 0
    highest = 0
    dropped_lines = 0
    while cycle < target:
        if cycle % 100000 == 0:
            print("==== STEP", cycle, "====")
            for c in reversed(cave):
                print(getSlice(c))
            print("")

            if cycle == 3:
                exit()

        current_rock_index = cycle % len(rocks)

        if known_configurations is not None:
            #print(known_configurations)
            known_caves = known_configurations.get((current_rock_index, current_gas_jet_index), [])
            if any([ cave in k for k in known_caves]):
                print("Found an identical configuration!!!")
                cycle_length = cycle
                cycle_height = highest + dropped_lines
                target = cycle - target % cycle
                dropped_lines = 0
                cycle = 0
                known_configurations = None
            else:
                known_caves.append(cave)
                known_configurations[(current_rock_index, current_gas_jet_index)] = known_caves
                #print(known_caves)

        # print(highest)
        rock_y = highest + 4
        next_rock = deepcopy(rocks[current_rock_index])
        if len(cave) < rock_y + len(next_rock):
            cave += [ 257 ] * (rock_y + len(next_rock) - len(cave))
        while True:
            gas_jet = gas_jets[current_gas_jet_index]
            current_gas_jet_index = (current_gas_jet_index + 1) % len(gas_jets)
            previous_rock = deepcopy(next_rock)
            next_rock = [ s << 1 if gas_jet == "<" else s >> 1 for s in next_rock ]
            # print("gj,r,nr =", gas_jet, [ getSlice(s) for s in previous_rock ], [ getSlice(s) for s in next_rock ])
            if any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                next_rock = previous_rock
            rock_y -= 1
            if rock_y == 0 or any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                for i, s in enumerate(next_rock):
                    cave[ rock_y + 1 + i ] |= s
                break

        # remove unecessary lines
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

        highest = max([0] + [ i for i in range(len(cave)) if cave[i] & 254 != 0 ])

        cycle += 1


    highest = max([ i for i in range(len(cave)) if cave[i] & 254 != 0 ])
    print(base_target, cycle_length, cycle_height, highest, dropped_lines)
    highest += dropped_lines + (base_target // cycle_length - 1) * cycle_height
    print(highest)



start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")