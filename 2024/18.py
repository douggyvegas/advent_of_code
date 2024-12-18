from heapq import heappop, heappush
import time

directions = [(1,0),(0,1),(-1,0),(0,-1)]

def dijkstra(corrupted_bytes: set[tuple[int, int]], 
            dim: tuple[int, int],
            pos: tuple[int, int], 
            end: tuple[int, int]) -> set[tuple[int, int]]:
    
    queue: list[tuple[tuple[int, int], set[tuple[int, int]]]] = [ (pos, {pos}) ]
    visited: dict[tuple[int, int], int] =  dict()
    best: set[tuple[int, int]] = set()
    
    while queue:
        pos, path = heappop(queue)
        if pos not in visited or len(path) < visited[pos]:
            visited[pos] = len(path)
            if pos == end:
                if len(best) == 0 or len(path) < len(best):
                    best = path
                continue
            for direction in directions:
                neighbor_position: tuple[int, int] = (pos[0] + direction[0], pos[1] + direction[1])
                if 0 <= neighbor_position[0] < dim[0] and 0 <= neighbor_position[1] < dim[1] and neighbor_position not in corrupted_bytes:
                    heappush(queue, (neighbor_position, path | { neighbor_position }))

    return best

def main():
    part1 = 0
    part2 = 0
    corrupted_bytes: set[tuple[int, int]] = set()
    next_bytes: list[tuple[int, int]] = []
    INIT = ["18.in", 1024, 71, 71]
    #INIT = ["18.ex", 12, 7, 7]
    with open(INIT[0]) as input:
        for row, line in enumerate(input.read().splitlines()):
            coords = list(map(int, line.split(",")))
            if len(corrupted_bytes) < INIT[1]:
                corrupted_bytes.add((coords[0], coords[1]))
            else:
                next_bytes.append((coords[0], coords[1]))
            
    path = dijkstra(corrupted_bytes, (INIT[2], INIT[3]), (0, 0), (INIT[2] - 1, INIT[3] - 1))
    printPath(corrupted_bytes, INIT, path)
    part1 = len(path) - 1
    print('part 1:', part1)

    other_path = path
    for next_byte in next_bytes:
        corrupted_bytes.add(next_byte)
        if next_byte in other_path:
            other_path = dijkstra(corrupted_bytes, (INIT[2], INIT[3]), (0, 0), (INIT[2] - 1, INIT[3] - 1))
            printPath(corrupted_bytes, INIT, other_path)
            if len(other_path) < INIT[2] + INIT[3] - 2:
                part2 = str(next_byte[0]) + "," + str(next_byte[1])
                break
    
    print('part 2:', part2)

def printPath(corrupted_bytes, INIT, path):
    for row in range(INIT[3]):
        line = ""
        for col in range(INIT[2]):
            if (col, row) in corrupted_bytes:
                line += "#"
            elif (col, row) in path:
                line += "█"
            else:
                line += "."
        print(line)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")