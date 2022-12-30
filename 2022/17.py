#!/usr/bin/env python3

from copy import deepcopy
from itertools import cycle
import time

def getSlice(s: int):
    return "{0:09b}".format(s).replace("0", " ").replace("1", "#")

def main():
    
    with open('17.ex') as input:
        for line in input.read().splitlines():
            gas_jets = list(line)

    rocks = [ ] # horizontal slices (bitmasks) bottom to top
    rocks.append([ 15 << 2 ])
    rocks.append([ 2 << 3, 7 << 3, 2 << 3 ])
    rocks.append([ 7 << 3, 1 << 3, 1 << 3 ])
    rocks.append([ 1 << 5, 1 << 5, 1 << 5, 1 << 5 ])
    rocks.append([ 3 << 4, 3 << 4 ])

    cave = [ ]

    known_configurations = { }
    current_gas_jet_index = 0
    cycle = 0
    target = 2022
    cycle_length = target
    cycle_height = 0
    cycle_count = 0
    highest = 0
    dropped_lines = 0
    while cycle < target:
        current_rock_index = cycle % len(rocks)
        rock_y = highest + 4
        next_rock = deepcopy(rocks[current_rock_index])
        if len(cave) < rock_y + len(next_rock):
            cave += [ 257 ] * (rock_y + len(next_rock) - len(cave))

        # if cycle % 100000 == 0:
        #     print("==== STEP", cycle, "====")
        #     for c in reversed(cave):
        #         print(getSlice(c))
        #     print("")
        # # if cycle == 3:
        # #     exit()

        while True:
            gas_jet = gas_jets[current_gas_jet_index]
            current_gas_jet_index = (current_gas_jet_index + 1) % len(gas_jets)
            previous_rock = deepcopy(next_rock)
            next_rock = [ s << 1 if gas_jet == "<" else s >> 1 for s in next_rock ]
            # print("gj,r,nr =", gas_jet, [ getSlice(s) for s in previous_rock ], [ getSlice(s) for s in next_rock ])
            if any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                next_rock = previous_rock
            rock_y -= 1
            if rock_y < 0 or any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                for i, s in enumerate(next_rock):
                    cave[ rock_y + 1 + i ] |= s
                break

        # remove unecessary lines
        acc = 0
        lowest = 0
        for i in range(len(cave) - 1, 0, -1):
            acc |= cave[i]
            if acc == 511:
                lowest = i
                break
        
        if lowest != 0:
            cave = cave[lowest::]
            dropped_lines += lowest

        highest = max([ i for i in range(len(cave)) if cave[i] & 254 != 0 ])

        if known_configurations is not None:
            #print(known_configurations)
            known_caves = known_configurations.get((current_rock_index, current_gas_jet_index), [])
            # print("============ STEP", cycle, "highest", highest, "dropped_lines", dropped_lines, "known caves", len(known_caves), "current_rock_index", current_rock_index, "current_gas_jet_index", current_gas_jet_index)

            for kc, c, h, d in known_caves:
                if kc == cave: 
                    print("Found an identical configuration!!!")
                    print("============ STEP", cycle, "highest", highest, "dropped_lines", dropped_lines, "current_rock_index", current_rock_index, "current_gas_jet_index", current_gas_jet_index)
                    print("c", c, "h", h, "d", d)
                    for s in range(max([ len(c) for c in [ cave ] + known_caves ])):
                        line = ""
                        for k in [ cave ] + [ kc ]:
                            if 0 <= len(k) - 1 - s < len(k):
                                line += getSlice(k[len(k) - 1 - s])
                            else:
                                line += "         "
                            line += "  "
                        print(line)
                    cycle_length = cycle - c
                    cycle_count = (target - c) // cycle_length
                    cycle_height = highest + dropped_lines - h - d
                    target = (target - c) % cycle_length
                    print("cycle_length", cycle_length, "cycle_count", cycle_count, "cycle_height", cycle_height, "highest", highest, "dropped_lines", dropped_lines, "target", target)
                    dropped_lines = d
                    cycle = 0
                    known_configurations = None
                    break
            else:
                known_caves.append((deepcopy(cave), cycle, highest, dropped_lines))
                known_configurations[(current_rock_index, current_gas_jet_index)] = known_caves
                #print(known_caves)

        cycle += 1


    highest = max([ i for i in range(len(cave)) if cave[i] & 254 != 0 ])
    highest = dropped_lines + highest + cycle_count * cycle_height
    print("highest", highest)
    print(1514285714288 - highest)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")