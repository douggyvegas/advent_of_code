
from heapq import heappush, heappop
import time

directions = [(1,0),(0,1),(-1,0),(0,-1)]

def dijkstra(maze: list[str], pos: tuple[int, int], dir: int, part2: bool) -> tuple[int, set[tuple[int, int]]]:
    queue: list[tuple[int, tuple[int, int], int, set[tuple[tuple[int, int], int]]]] = [ (0, pos, dir, {(pos, dir)}) ]
    paths: set[tuple[int, int]] = set()
    visited: dict[tuple[tuple[int, int], int], int] =  dict()
    best: int = -1
    
    while queue:
        current_score, current_position, current_direction, path = heappop(queue)
        if (current_position, current_direction) not in visited or visited[(current_position, current_direction)] >= current_score:
            visited[(current_position, current_direction)] = current_score
            if maze[current_position[1]][current_position[0]] == "E":
                if best < 0 or current_score < best:
                    best = current_score
                    paths = set([ (c,r) for ((c,r), d) in path ])
                    print("best = ", best)
                elif current_score == best and part2:
                    paths |= set([ (c,r) for ((c,r), d) in path ])
                continue
            for d, direction in enumerate(directions):
                if d != (current_direction + 2) % 4:
                    neighbor_position = (current_position[0] + direction[0], current_position[1] + direction[1])
                    if maze[neighbor_position[1]][neighbor_position[0]] != "#":
                        mul = 0 if abs(current_direction - d) == 0 else 1
                        neighbor_score = current_score + 1 + mul * 1000
                        if best == -1 or neighbor_score <= best:
                            heappush(queue, (neighbor_score, neighbor_position, d, path | { (neighbor_position, d) }))

    return (best, paths)


def printMaze(maze: list[str], paths: set[tuple[int, int]]):
    for row, line in enumerate(maze):
        p = ""
        for col, char in enumerate(line):
            if (col, row) in paths:
                p += "█"
            elif char == ".":
                p += " "
            else:
                p += char
        print(p)

def main():
    part1 = 0
    part2 = 0
    maze: list[str] = []
    start: tuple[int, int]
    with open("16.in") as input:
        for row, line in enumerate(input.read().splitlines()):
            maze.append(line)
            if 'S' in line:
                start = (line.find('S'), row)

    part1, paths = dijkstra(maze, start, 0, True)
    printMaze(maze, paths)
    part2 = len(paths)
    
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")