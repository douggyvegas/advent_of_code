#!/usr/bin/env python3

import math
import time

directions = [ [-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1] ]

def dfs(start, visited, blocks, outside):
    is_outside = False
    visited += [ start ]
    for direction in directions:
        neighbor = tuple([ sum(t) for t in zip(start, direction) ])
        if neighbor in outside:
            return True, visited
        if neighbor in blocks or neighbor in visited:
            continue
        is_neighbor_outside, visited = dfs(neighbor, visited, blocks, outside)
        is_outside |= is_neighbor_outside
    return is_outside, visited


def main():
    blocks = { }
    with open('18.in') as input:
        for line in input.read().splitlines():
            coords = tuple([ int(c) for c in line.split(",") ])
            blocks[coords] = [ ]
            for direction in directions:
                neighbor = tuple([ sum(t) for t in zip(coords, direction) ])
                n = blocks.get(neighbor, None)
                if n is not None:
                    blocks[coords].append(n)
                    n.append(coords)

        print(sum([ 6 - len(n) for n in blocks.values() ]))
        
        minc = [ math.inf ] * 3
        maxc = [ -math.inf ] * 3
        minc = [ min([ c[a] for c in blocks.keys() ]) for a in range(3) ]
        maxc = [ max([ c[a] for c in blocks.keys() ]) for a in range(3) ]

        outside = [ ]
        for x in range(minc[0], maxc[0] + 1):                
            for y in range(minc[1], maxc[1] + 1):                
                for z in range(minc[2], maxc[2] + 1):
                    coords = (x,y,z)
                    if not coords in blocks.keys():
                        # empty space, is it outside ?
                        blocked_directions = 0
                        for direction in directions:
                            blocked = True
                            for axis in range(3):
                                if direction[axis] < 0:
                                    blocked &= any([ b for b in blocks.keys() if b[axis] < coords[axis] ])
                                elif direction[axis] > 0:
                                    blocked &= any([ b for b in blocks.keys() if b[axis] > coords[axis] ])
                                else:
                                    blocked &= any([ b for b in blocks.keys() if b[axis] == coords[axis] ])
                                
                            if blocked:
                                blocked_directions += 1

                        # print(coords, blocked_directions)
                        if blocked_directions != 6:
                            outside.append(coords)

        for x in range(minc[0], maxc[0] + 1):                
            for y in range(minc[1], maxc[1] + 1):                
                for z in range(minc[2], maxc[2] + 1):
                    coords = (x,y,z)
                    if not coords in blocks.keys() and not coords in outside:
                        # may be inside, try to find a path to the outside
                        is_outside, visited = dfs(coords, [ ], blocks.keys(), outside)
                        if is_outside:
                            outside += visited
                        else:
                            for block in visited:
                                blocks[block] = [ ]
                                for direction in directions:
                                    neighbor = tuple([ sum(t) for t in zip(block, direction) ])
                                    n = blocks.get(neighbor, None)
                                    if n is not None:
                                        blocks[block].append(n)
                                        n.append(block)                                

        print(sum([ 6 - len(n) for n in blocks.values() ]))


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")