#!/usr/bin/env python3

from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations, permutations, tee
import math
import time
import re
from tracemalloc import start

@dataclass
class Valve:
    index: int
    name: str
    rate: int
    neighbors: list

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
    
def bfs(graph, start, end):
    queue = list([[ start ]])
    visited = list([ start ])
    while queue:
        path = queue.pop(0)
        last = path[-1]
        if last == end:
            return path
        for neighbor in graph[last].neighbors:
            if neighbor not in visited:
                queue.append(path + [ neighbor ])
                visited.append(neighbor)

    return None

def dfs(valves, shortest_paths, path, to_explore, time_left):
    max_pressure = 0
    new_path = path
    for to_valve in to_explore:
        time_left_ = time_left - shortest_paths[(path[-1], to_valve)] - 1
        if time_left_ >= 0:
            pressure_released_by_valve = valves[to_valve].rate * time_left_
            to_pressure, to_path = dfs(valves, shortest_paths, path + [ to_valve ], [ e for e in to_explore if e != to_valve ], time_left_)
            to_pressure += pressure_released_by_valve
            if to_pressure > max_pressure:
                max_pressure = to_pressure
                new_path = to_path

    #print(" -> ".join([valves[v].name for v in new_path]), max_pressure)

    return max_pressure, new_path

def main():
    valves = [ ]
    start = 0
    with open('16.in') as input:
        tunnels = [ ]
        for i, line in enumerate(input.read().splitlines()):
            match = re.match(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+, )*\w+)", line)
            if match:
                valve = Valve(i, match.group(1), int(match.group(2)), [ ])
                if valve.name == 'AA': start = i
                tunnels.append([ m.strip() for m in match.group(3).split(",") ])
                valves.append(valve)

        for i, tunnel in enumerate(tunnels):
            valves[i].neighbors = [ i for t in tunnel for i in range(len(valves)) if valves[i].name == t ]

    useful_valves = [ v.index for v in valves if v.rate != 0 or v.name == 'AA' ]
    shortest_paths = { }
    for pair in permutations(useful_valves, 2):
        shortest_paths[pair] = len(bfs(valves, pair[0], pair[1])) - 1

    for k,v in shortest_paths.items():
        print(k, v)

    max_pressure_released, path = dfs(valves, shortest_paths, [ start ], [ v for v in useful_valves if v != start ], 30)
    print("Best path:", " -> ".join([valves[v].name for v in path]), max_pressure_released)
    print(max_pressure_released)

    my_valves_combinations = combinations(useful_valves, len(useful_valves) // 2)
    together_max_pressure_released = 0
    together_best_paths = ()
    for my_valves in my_valves_combinations:
        # print("me", my_valves)
        my_pressure_released, my_path = dfs(valves, shortest_paths, [ start ], [ v for v in my_valves if v != start ], 26)
        
        elephant_valves = [ v for v in useful_valves if v not in my_valves ]
        # print("elephant", elephant_valves)
        elephant_pressure_released, elephant_path = dfs(valves, shortest_paths, [ start ], [ v for v in elephant_valves if v != start ], 26)
        
        together_pressure_released = my_pressure_released + elephant_pressure_released
        if  together_pressure_released > together_max_pressure_released:
            together_max_pressure_released = together_pressure_released
            together_best_paths = (my_path, elephant_path)
        
    print("Together max pressure released:", together_max_pressure_released)
    print("My best path:", " -> ".join([valves[v].name for v in together_best_paths[0]]))
    print("Elephant best path:", " -> ".join([valves[v].name for v in together_best_paths[1]]))

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")