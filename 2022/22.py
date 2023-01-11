#!/usr/bin/env python3

import logging
import time
import re
import os

DIRECTIONS = [ [1,0], [0,1], [-1,0], [0,-1] ]
DIRECTIONS_CHARACTERS = [ ">", "V", "<", "Ʌ" ]

def main():

    with open('22.in') as input:
        lines = input.read().splitlines()

    height = [ i for i,l in enumerate(lines, 0) if len(l) == 0 ][0]
    width = max([ len(l) for l in lines[::height] ])

    grid = [ list(line.ljust(width)) for line in lines ]
    grid = [ [ row[i] for row in grid ] for i in range(width) ]

    cube = { 
        ((1,0),2): ((0,2),0),
        ((1,0),3): ((0,3),0),
        ((2,0),0): ((1,2),2),
        ((2,0),1): ((1,1),2),
        ((2,0),3): ((0,3),3),
        ((1,1),0): ((2,0),3),
        ((1,1),2): ((0,2),1),
        ((0,2),2): ((1,0),0),
        ((0,2),3): ((1,1),0),
        ((1,2),0): ((2,0),2),
        ((1,2),1): ((0,3),2),
        ((0,3),0): ((1,2),3),
        ((0,3),1): ((1,0),1),
        ((0,3),2): ((2,0),1),
    }

    positions = { }
    position = [ [ x for x in range(width) if grid[x][0] != ' ' ][0], 0 ]
    facing = 0
    part1 = False
    positions[tuple(position)] = facing
    instructions = re.split("([L|R])", lines[height + 1])
    for i, instruction in enumerate(instructions):
        if instruction == 'L':
            facing = (facing - 1)  % 4
        elif instruction == 'R':
            facing = (facing + 1)  % 4
        else:
            steps = int(instruction)
            for _ in range(steps):
                direction = DIRECTIONS[facing]
                next_position = list(map(sum, zip(position, direction)))
                next_facing = facing
                if next_position[0] < 0 or next_position[1] < 0 or next_position[0] >= width or next_position[1] >= height or grid[next_position[0]][next_position[1]] == " ":
                    if facing == 0:
                        if part1: next_position[0] = 0
                        elif next_position[1] < 50: next_position, next_facing = (99, 149 - next_position[1]), 2 # a (2,0) -> (1,2)
                        elif next_position[1] < 100: next_position, next_facing = (100 + next_position[1] % 50, 49), 3 # b (1,1) -> (2,0)
                        elif next_position[1] < 150: next_position, next_facing = (149, 49 - next_position[1] % 50), 2 # a (1,2) -> (2,0)
                        elif next_position[1] < 200: next_position, next_facing = (50 + next_position[1] % 50, 149), 3 # e (0,3) -> (1,2)
                    elif facing == 1:
                        if part1: next_position[1] = 0
                        elif next_position[0] < 50: next_position, next_facing = (100 + next_position[0], 0), 1 # c (0,3) -> (2,0)
                        elif next_position[0] < 100: next_position, next_facing = (49, 150 + next_position[0] % 50), 2 # e (1,2) -> (0,3)
                        elif next_position[0] < 150: next_position, next_facing = (99, 50 + next_position[0] % 50), 2 # b (2,0) -> (1,1)
                    elif facing == 2:
                        if part1: next_position[0] = width - 1
                        elif next_position[1] < 50: next_position, next_facing = (0, 149 - next_position[1] % 50), 0 # d (1,0) -> (0,2)
                        elif next_position[1] < 100: next_position, next_facing = (next_position[1] % 50, 100), 1 # f (1,1) -> (0,2)
                        elif next_position[1] < 150: next_position, next_facing = (50, 49 - next_position[1] % 50), 0 # d (0,2) -> (1,0)
                        elif next_position[1] < 200: next_position, next_facing = (50 + next_position[1] % 50, 0), 1 # g (0,3) -> (1,0)
                    elif facing == 3:
                        if part1: next_position[1] = height - 1
                        elif next_position[0] < 50: next_position, next_facing = (50, 50 + next_position[0] % 50), 0 # f (0,2) -> (1,1)
                        elif next_position[0] < 100: next_position, next_facing = (0, 150 + next_position[0] % 50), 0 # g (1,0) - >(0,3)
                        elif next_position[0] < 150: next_position, next_facing = (next_position[0] % 50, 199), 3 # c (2,0) -> (0,3)
                    
                    if part1:
                        while grid[next_position[0]][next_position[1]] == " ":
                            next_position = tuple(map(sum, zip(next_position, direction)))

                if grid[next_position[0]][next_position[1]] == "#":
                    positions[tuple(position)] = facing
                    break
                else:
                    position = next_position
                    facing = next_facing
                    positions[tuple(position)] = facing

            if i % 100 == 0 or i == len(instructions) - 1:
                os.system('clear')
                print("    0" + " " * 49 + "50" + " " * 48 + "100" + " " * 47 + "150")
                for y in range(height):
                    line = "{0:03d}".format(y) + " "
                    for x in range(width):
                        f = positions.get((x, y), None)
                        if f == None:
                            line += grid[x][y]
                        else:
                            line += DIRECTIONS_CHARACTERS[f]
                    print(line)

    print(position, facing, 1000 * (position[1] + 1) + 4 * (position[0] + 1) + facing)

start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")