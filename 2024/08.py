import time


def main():
    part1 = 0
    part2 = 0
    antennas: dict[str, list[tuple[int, int]]] = {}
    width = 0
    height = 0
    with open("08.in") as input:
        for row, line in enumerate(input.read().splitlines()):
            width = len(line)
            height += 1
            for col, c in enumerate(line):
                if c != ".":
                    if c not in antennas:
                        antennas[c] = []
                    antennas[c].append((col, row))

    print(antennas)

    antinodes1: set[tuple[int, int]] = set()
    antinodes2: set[tuple[int, int]] = set()

    for key in antennas:
        positions = antennas[key]
        for i, pos1 in enumerate(positions[0:-1]):
            for pos2 in positions[i + 1 :]:
                dx = pos2[0] - pos1[0]
                dy = pos2[1] - pos1[1]
                i = 0
                antinode = (pos1[0] - (dx * i), pos1[1] - (dy * i))
                while 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                    if i == 1:
                        antinodes1.add(antinode)
                    antinodes2.add(antinode)
                    i += 1
                    antinode = (pos1[0] - (dx * i), pos1[1] - (dy * i))

                i = 0
                antinode = (pos2[0] + (dx * i), pos2[1] + (dy * i))
                while 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                    if i == 1:
                        antinodes1.add(antinode)
                    antinodes2.add(antinode)
                    i += 1
                    antinode = (pos2[0] + (dx * i), pos2[1] + (dy * i))

    part1 = len(antinodes1)
    part2 = len(antinodes2)

    print("part 1:", part1)
    print("part 2:", part2)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
