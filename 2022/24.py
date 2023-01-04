#!/usr/bin/env python3

from collections import deque
import math
import time

DIRECTIONS = [ [1,0], [0,1], [-1,0], [0,-1] ]
BLIZZARDS = [ ">", "v", "<", "^" ]

def main():

    blizzards_by_elapsed = { }
    with open('24.in') as input:
        lines = input.read().splitlines()

    width = len(lines[0])
    height = len(lines)

    initial_blizzards = { }
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if y == 0 and c == ".":
                start = (x,y)
            if c in BLIZZARDS:
                initial_blizzards[(x,y)] = initial_blizzards.get((x,y), []) + [ DIRECTIONS[BLIZZARDS.index(c)] ]
            if y == height - 1 and c == ".":
                end = (x,y)

    blizzards_by_elapsed[0] = initial_blizzards

    number_of_configurations = lcm(width - 2, height - 2)
    for i in range(1, number_of_configurations):
        previous_blizzards = blizzards_by_elapsed[i - 1]
        blizzards = { }
        for blizzard_pos, blizzard_dirs in previous_blizzards.items():
            for blizzard_dir in blizzard_dirs:
                next_blizzard_pos = ( 1 + (blizzard_pos[0] - 1 + blizzard_dir[0]) % (width - 2), 1 + (blizzard_pos[1] - 1 + blizzard_dir[1]) % (height - 2) )
                blizzards[next_blizzard_pos] = blizzards.get(next_blizzard_pos, []) + [ blizzard_dir ]
        blizzards_by_elapsed[i] = blizzards

    min_elapsed = [ 0, math.inf, math.inf, math.inf ]
    destinations = [ start, end, start, end ]
    for destination_index in range(1, len(destinations)):
        start = destinations[destination_index - 1]
        end = destinations[destination_index]
        print(destination_index, start, end)
        q = [ [ (start , min_elapsed[destination_index - 1]) ] ]
        visited = { }
        while len(q) != 0:
            state = list(q.pop(0))
            pos = state[-1][0]
            next_elapsed = state[-1][1] + 1

            if pos == end:
                if next_elapsed - 1 < min_elapsed[destination_index]:
                    min_elapsed[destination_index] = next_elapsed - 1
                    # path = state
                continue

            if next_elapsed > min_elapsed[destination_index]:
                continue
            
            if pos in visited.get(next_elapsed, [ ]):
                continue

            if next_elapsed + end[0] - pos[0] + end[1] - pos[1] >= min_elapsed[destination_index]:
                # won't be able to reach the end in less time than the min elapsed time
                continue

            blizzards = blizzards_by_elapsed.get(next_elapsed % number_of_configurations, [ ])

            visited[next_elapsed] = visited.get(next_elapsed, []) + [ pos ]

            # enqueue new states
            next_pos = [ pos ] + [ tuple(map(sum, zip(list(pos), DIRECTIONS[d]))) for d in range(4) ]
            next_pos = [ p for p in next_pos if p not in blizzards.keys() and ((p[0] > 0 and p[0] < width - 1 and p[1] > 0 and p[1] < height - 1) or (p == start) or (p == end)) ]

            for p in next_pos:
                new_state = [ state + [ (p, next_elapsed) ] ]
                q += new_state

    # for m in range(min_elapsed + 1):
    #     printConfiguration(width, height, start, end, path[m], blizzards_by_elapsed.get(m % number_of_configurations, [ ]))
    print(min_elapsed)

def printConfiguration(width, height, start, end, state, blizzards):
    print("====", state[1], "====")
    pos = state[0]
    for y in range(height):
        line = ""
        for x in range(width):
            if (x,y) == pos:
                line += "E"
            elif (x,y) == start or (x,y) == end:
                line += "."
            elif x == 0 or x == width - 1 or y == 0 or y == height - 1:
                line += "#"
            else:
                blizzard_directions = blizzards.get((x,y), [ ])
                if len(blizzard_directions) == 0:
                    line += "."
                elif len(blizzard_directions) == 1:
                    if blizzard_directions[0] in DIRECTIONS:
                        line += BLIZZARDS[DIRECTIONS.index(blizzard_directions[0])]
                else:
                    line += str(len(blizzard_directions))
        print(line)

def gcd(x, y):
   while y:
       x, y = y, x % y
   return x

def lcm(x, y):
   lcm = (x * y) // gcd(x, y)
   return lcm

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")