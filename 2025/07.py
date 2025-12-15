from functools import lru_cache
import time

def main():
    part1 = 0
    part2 = 0
    grid: list[frozenset[int]] = []
    beams: set[int] = set()
    start: tuple[int, int]
    with open("07.in") as input:
        lines = input.read().splitlines()
        for line in lines[1:]:
            grid.append(frozenset([ int(col) for col, c in enumerate(line) if c == '^' ]))
        start = (0, lines[0].index('S')) 
        beams.add(start[1])

    for splitters in grid:
        next_beams = set()
        for beam in beams:
            if beam in splitters:
                part1 += 1
                next_beams.add(beam - 1)
                next_beams.add(beam + 1)
            else:
                next_beams.add(beam)
        beams = next_beams

    print('part 1:', part1)

    @lru_cache
    def getTimeLines(pos: tuple[int, int]) -> int:
        if pos[0] == len(grid):
            return 1
        if pos[1] not in grid[pos[0]]:
            return getTimeLines((pos[0] + 1, pos[1]))
        else:
            return getTimeLines((pos[0] + 1, pos[1] - 1)) + getTimeLines((pos[0] + 1, pos[1] + 1))

    part2 = getTimeLines(start)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")