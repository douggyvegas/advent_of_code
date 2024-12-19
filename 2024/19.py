from functools import lru_cache
import time

@lru_cache(maxsize=None)
def createDesign(design: str, towels: tuple[str]) -> int:
    arrangements: int = 0
    for towel in towels:
        if design.startswith(towel):
            if len(towel) == len(design):
                arrangements += 1
            arrangements += createDesign(design[len(towel):], towels)

    return arrangements

def main():
    part1 = 0
    part2 = 0
    towels: list[str] = []
    designs: list[str] = []
    with open("19.in") as input:
        for row, line in enumerate(input.read().splitlines()):
            if row == 0:
                towels = line.split(', ')
            elif len(line) > 0:
                designs.append(line)
                
    for design in designs:
        a = createDesign(design, tuple(towels))
        part1 += 1 if a > 0 else 0
        part2 += a
                
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")