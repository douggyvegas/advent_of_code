#!/usr/bin/env python3

import time

def main():
    directions = { "U": [ 0, -1 ], "R": [ 1, 0 ], "D": [ 0, 1 ], "L": [ -1, 0 ] }
    knots = [ [ 0, 0 ] for i in range(10) ]
    visited_coordinates = [ set() for i in range(10) ]
    with open('09.in') as input:
        for heading, steps in [ line.split() for line in input.read().splitlines() ]:
            direction = directions[heading]
            for _ in range(int(steps)):
                knots[0][0] += direction[0]
                knots[0][1] += direction[1]
                visited_coordinates[0].add(tuple(knots[0]))
                for knot_index in range(1, len(knots)):
                    head = knots[knot_index - 1]
                    knot = knots[knot_index]
                    if max(abs(knot[0] - head[0]), abs(knot[1] - head[1])) > 1:
                        if knot[0] == head[0]:
                            knot[1] += int((head[1] - knot[1]) / 2)
                        elif knot[1] == head[1]:
                            knot[0] += int((head[0] - knot[0]) / 2)
                        else:
                            knot[0] += (1 if knot[0] < head[0] else -1)
                            knot[1] += (1 if knot[1] < head[1] else -1)

                    visited_coordinates[knot_index].add(tuple(knot))

    print(len(visited_coordinates[1]))
    print(len(visited_coordinates[-1]))

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")