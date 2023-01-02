#!/usr/bin/env python3

from copy import deepcopy
import logging
import time

DIRECTIONS = [ [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1] ]

def main():

    with open('23.in') as input:
        lines = input.read().splitlines()

    elves = { }
    for y, line in enumerate(lines):
        for x ,c in enumerate(line):
            if c == "#":
                elves[(x,y)] = None

    previous_configuration = None
    rounds = [ 0, 4, 6, 2 ]
    round = 0
    while elves != previous_configuration:
        if round % 100 == 0:
            printConfiguration(elves, round)
        previous_configuration = elves.copy()

        round += 1
        proposals = { }
        for elf_pos in elves.keys():
            neighbors = [ tuple(map(sum, zip(list(elf_pos), DIRECTIONS[d]))) for d in range(8) ]
            all_free = all([ pos not in elves.keys() for pos in neighbors ])
            if not all_free:
                for possibility in range(4):
                    d = rounds[(possibility + round - 1) % 4]
                    free = all([ neighbors[n] not in elves.keys() for n in [ (d - 1) % 8, d, (d + 1) % 8 ] ] )
                    if free:
                        proposal = tuple(map(sum, zip(list(elf_pos), DIRECTIONS[d])))
                        if proposal not in proposals.keys():
                            proposals[proposal] = [ ]
                        proposals[proposal] += [ elf_pos ]
                        break

        for proposal, elves_pos in proposals.items():
            if len(elves_pos) == 1:
                del elves[elves_pos[0]]
                elves[proposal] = None
        
        if round == 10:
            min_x = min([ p[0] for p in elves.keys() ])
            max_x = max([ p[0] for p in elves.keys() ])
            min_y = min([ p[1] for p in elves.keys() ])
            max_y = max([ p[1] for p in elves.keys() ])
            printConfiguration(elves, round)
            print((max_x - min_x + 1) * (max_y - min_y + 1) - len(elves.keys()))

    printConfiguration(elves, round)
    print(round)

def printConfiguration(elves, round):
    min_x = min([ p[0] for p in elves.keys() ])
    max_x = max([ p[0] for p in elves.keys() ])
    min_y = min([ p[1] for p in elves.keys() ])
    max_y = max([ p[1] for p in elves.keys() ])
    print("========", round, "========")
    print(min_x, max_x)
    print(min_y, max_y)
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            line += "#" if (x,y) in elves.keys() else "."
        print(line)

start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")