#!/usr/bin/env python3

import logging
import time
import re
import os

DIRECTIONS = [ [1,0], [0,1], [-1,0], [0,-1] ]
DIRECTIONS_CHARACTERS = [ ">", "V", "<", "Ʌ" ]

def main():

    with open('22.ex') as input:
        lines = input.read().splitlines()

    width = max([ len(l) for l in lines ])
    height = [ i for i,l in enumerate(lines, 0) if len(l) == 0 ][0]

    print(width, height)

    grid = [ list(line.ljust(width)) for line in lines ]
    grid = [ [ row[i] for row in grid ] for i in range(width) ]

    positions = { }
    position = [ [ x for x in range(width) if grid[x][0] != ' ' ][0], 0 ]
    facing = 0
    positions[tuple(position)] = facing
    instructions = re.split("([L|R])", lines[height + 1])
    for instruction in instructions:
        if instruction == 'L':
            facing = (facing - 1)  % 4
        elif instruction == 'R':
            facing = (facing + 1)  % 4
        else:
            steps = int(instruction)
            direction = DIRECTIONS[facing]
            for _ in range(steps):
                next_position = list(map(sum, zip(position, direction)))
                if grid[next_position[0]][next_position[1]] == " ":
                    match facing:
                        case 0: next_position[0] = 0
                        case 1: next_position[1] = 0
                        case 2: next_position[0] = width - 1
                        case 3: next_position[1] = height - 1
                    
                    while grid[next_position[0]][next_position[1]] == " ":
                        next_position = tuple(map(sum, zip(next_position, direction)))

                if grid[next_position[0]][next_position[1]] == "#":
                    positions[tuple(position)] = facing
                    break
                else:
                    position = next_position
                    positions[tuple(position)] = facing

            os.system('clear')
            print(instruction)
            for y in range(height):
                line = ""
                for x in range(width):
                    f = positions.get((x, y), None)
                    if f == None:
                        line += grid[x][y]
                    else:
                        line += DIRECTIONS_CHARACTERS[f]
                print(line)

    print("part 1:", 1000 * (position[1] + 1) + 4 * (position[0] + 1) + facing)

start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")