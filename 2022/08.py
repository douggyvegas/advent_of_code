#!/usr/bin/env python3

import time
from functools import reduce
import operator

directions = [ [ 0, -1, 0, 1 ], [ 1, 0, 0, 0 ], [ 0, 1, 0, 0 ], [ -1, 0, 1, 0 ] ]

def main():
    forest = []
    visible = []
    scenic_score = []

    with open('08.in') as input:
        for line in input.read().splitlines():
            trees = [ int(height) for height in list(line) ]
            forest.append(trees)
            visible.append([ False ] * len(trees))
            scenic_score.append([ 0 ] * len(trees))

        rows = len(forest)
        columns = len(forest[0])

        for x in range(columns):
            for y in range(rows):
                tree_scenic_score = [ 0 ] * 4
                for d, direction in enumerate(directions):
                    view_is_blocked = False
                    look_x = x + direction[0]
                    look_y = y + direction[1]
                    while look_x >= 0 and look_x < columns and look_y >= 0 and look_y < rows:
                        if not view_is_blocked:
                            tree_scenic_score[d] += 1
                            if forest[look_x][look_y] >= forest[x][y]:
                                view_is_blocked = True
                        look_x += direction[0]
                        look_y += direction[1]

                    visible[x][y] |= not view_is_blocked
                    
                scenic_score[x][y] = reduce(operator.mul, tree_scenic_score)

    print("part1:", len([ v for row in visible for v in row if v == True ]))
    print("part2:", max([ s for row in scenic_score for s in row ]))


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
