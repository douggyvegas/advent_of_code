#!/usr/bin/env python3

from copy import deepcopy
import time

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

    for part_target in [ 2022, 1000000000000 ]:
        cave = [ ]
        target = part_target
        known_configurations = { }
        current_gas_jet_index = 0
        fallen_rocks = 0
        cycle_length = target
        cycle_height = 0
        number_of_cycles = 0
        highest = -1
        dropped_lines = 0
        while fallen_rocks < target:
            current_rock_index = fallen_rocks % len(rocks)
            rock_y = highest + 4
            next_rock = deepcopy(rocks[current_rock_index])
            if len(cave) < rock_y + len(next_rock):
                cave += [ 257 ] * (rock_y + len(next_rock) - len(cave))

            while True:
                gas_jet = gas_jets[current_gas_jet_index]
                current_gas_jet_index = (current_gas_jet_index + 1) % len(gas_jets)
                previous_rock = deepcopy(next_rock)
                next_rock = [ s << 1 if gas_jet == "<" else s >> 1 for s in next_rock ]
                if any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                    next_rock = previous_rock
                rock_y -= 1
                if rock_y < 0 or any([ s & cave[ rock_y + i ] for i, s in enumerate(next_rock) ]):
                    for i, s in enumerate(next_rock):
                        cave[ rock_y + 1 + i ] |= s
                    break
            
            fallen_rocks += 1

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
                known_caves = known_configurations.get((current_rock_index, current_gas_jet_index), [])
                for kc, c, d in known_caves:
                    if kc == cave:
                        cycle_length = fallen_rocks - c
                        number_of_cycles = (target - fallen_rocks) // cycle_length
                        cycle_height = dropped_lines - d
                        dropped_lines += number_of_cycles * cycle_height
                        fallen_rocks += number_of_cycles * cycle_length
                        known_configurations = None
                        break
                else:
                    known_caves.append((deepcopy(cave), fallen_rocks, dropped_lines))
                    known_configurations[(current_rock_index, current_gas_jet_index)] = known_caves

        highest = max([ i for i in range(len(cave)) if cave[i] & 254 != 0 ])
        highest = dropped_lines + highest + 1
        print(part_target, highest)
    
start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")