#!/usr/bin/env python3

from __future__ import unicode_literals
from collections import deque
from copy import deepcopy
import math
from queue import PriorityQueue
import sys
import time

def getHeight(c):
    if c == 'S':
        return getHeight('a')
    if c == 'E':
        return getHeight('z')
    return ord(c) - ord('a')

def main():
    map = [ ]
    with open('12.in') as input:
        for line in input.read().splitlines():
            map.append(list(line))

    height = len(map)
    width = len(map[0])

    graph = { }
    directions = [ [ 0, -1 ], [ 1, 0 ], [ 0, 1 ], [ -1, 0 ] ]
    part2_starts = [ ]
    for x in range(width):
        for y in range(height):
            coords = (x, y)
            if map[coords[1]][coords[0]] == 'S':
                part1_start = coords
                part2_starts.append(coords)
            if map[coords[1]][coords[0]] == 'a':
                part2_starts.append(coords)
            if map[coords[1]][coords[0]] == 'E':
                end = coords
            current_height = getHeight(map[coords[1]][coords[0]])
            graph[coords] = list()
            for direction in directions:
                neighbor = (x + direction[0], y + direction[1])
                if neighbor[0] >= 0 and neighbor[0] < width and neighbor[1] >= 0 and neighbor[1] < height:
                    neighbor_height = getHeight(map[neighbor[1]][neighbor[0]])
                    if neighbor_height - current_height <= 1:
                        graph[coords].append(neighbor)

    print("Part 1")
    shortest_path = computeShortestPath(graph, part1_start, end)
    printPath(map, shortest_path)
    print(len(shortest_path))

    print("Part 2")
    part2_paths = [ ]
    for _, start in enumerate(part2_starts):
        part2_paths.append(computeShortestPath(graph, start, end))
    part2_paths = sorted(part2_paths, key = lambda p: len(p) if p is not None else math.inf)
    printPath(map, part2_paths[0])
    print(len(part2_paths[0]))


def printPath(map, path):
    grid = deepcopy(map)
    for i, cell in enumerate(path):
        if i < len(path) - 1:
            direction = ( path[i + 1][0] - cell[0], path[i + 1][1] - cell[1])
            if direction == (0,1):
                grid[cell[1]][cell[0]] = "\33[41mv\033[0m"
            elif direction == (0,-1):
                grid[cell[1]][cell[0]] = "\33[41m^\033[0m"
            elif direction == (1,0):
                grid[cell[1]][cell[0]] = "\33[41m>\033[0m"
            elif direction == (-1,0):
                grid[cell[1]][cell[0]] = "\33[41m<\033[0m"

    grid[path[0][1]][path[0][0]] = "\33[41mS\033[0m"
    grid[path[len(path) - 1][1]][path[len(path) - 1][0]] = "\33[41mE\033[0m"

    for line in grid:
        print(''.join(line))


def computeShortestPath(graph, start, end):
    queue = list([[ start ]])
    visited = set([ start ])
    while queue:
        path = queue.pop(0)
        last = path[-1]
        if last == end:
            return path
        for neighbor in graph[last]:
            if neighbor not in visited:
                queue.append(path + [ neighbor ] )
                visited.add(neighbor)

    return None

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")