from copy import copy
from heapq import heappop, heappush
import time
import re
from typing import Any, Dict, List, Set, Tuple

def neighbors(grid: List[List[int]], cell: Tuple[int, int], delta: Tuple[int, int] | None, min_dist: int, max_dist: int) -> List[Tuple[int, Tuple[int, int], int, Tuple[int, int]]]:
    width: int = len(grid[0])
    height: int = len(grid)
    neighbors: List[Tuple[int, Tuple[int, int], int, Tuple[int, int]]] = [ ]
    
    forbidden_directions = [ ]
    if delta is not None:
        forbidden_directions = [ delta, ( -delta[0], -delta[1] ) ]
    
    for direction in [(0,1),(1,0),(-1,0),(0,-1)]:
        if direction not in forbidden_directions:
            heatloss: int = 0
            for dist in range(1, max_dist + 1):
                neighbor = (cell[0] + direction[0] * dist, cell[1] + direction[1] * dist)
                if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
                    heatloss += grid[neighbor[0]][neighbor[1]]
                    if dist >= min_dist:
                        neighbors.append((heatloss, direction, dist, neighbor))
                else:
                    break
            
    return neighbors

def dijkstra(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int], min_dist: int, max_dist: int) -> Tuple[int, List[Tuple[int, int]]]:
    visited : Set[Tuple[Tuple[int, int] | None, int, Tuple[int, int]]] = set()
    heatloss : Dict[Tuple[Tuple[int, int] | None, int, Tuple[int, int]], int] = { (None, 0, start): 0 }
    queue : List[Tuple[int, Tuple[int, int] | None, int, Tuple[int, int], List[Tuple[int, int]]]] = [ (0, None, 0, start, [ start ]) ]
    best_path : Tuple[int, List[Tuple[int, int]]] | None = None
    while queue:
        current_heatloss, current_direction, current_distance, current_position, path = heappop(queue)
        if (current_direction, current_distance, current_position) not in visited:
            visited.add((current_direction, current_distance, current_position))
            if current_position == end:
                if best_path is None or current_heatloss < best_path[0]:
                    best_path = (current_heatloss, path)
                continue
            for neighbor_heatloss, neighbor_direction, neighbor_distance, neighbor_position in neighbors(grid, current_position, current_direction, min_dist, max_dist):
                if (neighbor_direction, neighbor_distance, neighbor_position) not in visited:
                    next_heatloss : int = current_heatloss + neighbor_heatloss
                    if (neighbor_direction, neighbor_distance, neighbor_position) not in heatloss or heatloss[(neighbor_direction, neighbor_distance, neighbor_position)] > next_heatloss:
                        heatloss[(neighbor_direction, neighbor_distance, neighbor_position)] = next_heatloss
                        heappush(queue, (next_heatloss, neighbor_direction, neighbor_distance, neighbor_position, path + [ neighbor_position ]))

    if best_path is not None:
        return best_path
    
    return (-1, [])

def solve(grid: List[List[int]], min_dist: int, max_dist: int) -> int:
    heatloss, path = dijkstra(grid, (0,0), (len(grid) - 1, len(grid[0]) - 1), min_dist, max_dist)
    for row, line in enumerate(grid):
        disp = [ str(c) for c in line ]
        for col, _ in enumerate(line):
            if (row, col) in path:
                disp[col] = '#'
        print(''.join(disp))
    return heatloss

def main():
    grid : List[List[int]] = [ ]
    with open("17.in") as input:
        for line in input.read().splitlines():
            grid.append([ int(c) for c in line ])

    print(f"part 1: {solve(grid, 1, 3)}")
    print(f"part 2: {solve(grid, 4, 10)}")


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")