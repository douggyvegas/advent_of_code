import math
import re
import time


def checkTree(robots: list[tuple[int, int, int, int]], width: int, height: int) -> bool:
    pos = [(r[0], r[1]) for r in robots]
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in pos:
                line += "X"
            else:
                line += " "
        if "XXXXXXXXXXXX" in line:
            return True
    return False


def printRobots(
    robots: list[tuple[int, int, int, int]], width: int, height: int, elapsed: int
):
    with open("14/" + str(elapsed) + ".txt", "w") as out:
        pos = [(r[0], r[1]) for r in robots]
        for y in range(height):
            line = ""
            for x in range(width):
                if (x, y) in pos:
                    line += "X"
                else:
                    line += " "

            out.write(line + "\n")


def main():
    part1 = 0
    part2 = 0
    pattern = re.compile(r"p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)")
    robots: list[tuple[int, int, int, int]] = []
    with open("14.in") as input:
        for line in input.read().splitlines():
            matches = pattern.findall(line)
            robot = (
                int(matches[0][0]),
                int(matches[0][1]),
                int(matches[0][2]),
                int(matches[0][3]),
            )
            robots.append(robot)

    width = 101
    height = 103
    time = 10000

    updated_robots: list[tuple[int, int, int, int]] = []
    for elapsed in range(1, time + 1):
        updated_robots = []
        for robot in robots:
            updated_robots.append(
                (
                    (robot[0] + elapsed * robot[2]) % width,
                    (robot[1] + elapsed * robot[3]) % height,
                    robot[2],
                    robot[3],
                )
            )

        if elapsed == 100:
            part1 = (
                len(
                    [
                        1
                        for r in updated_robots
                        if r[0] < width // 2 and r[1] < height // 2
                    ]
                )
                * len(
                    [
                        1
                        for r in updated_robots
                        if r[0] > width // 2 and r[1] < height // 2
                    ]
                )
                * len(
                    [
                        1
                        for r in updated_robots
                        if r[0] < width // 2 and r[1] > height // 2
                    ]
                )
                * len(
                    [
                        1
                        for r in updated_robots
                        if r[0] > width // 2 and r[1] > height // 2
                    ]
                )
            )

        if checkTree(updated_robots, width, height):
            printRobots(updated_robots, width, height, elapsed)
            part2 = elapsed
            break

    print("part 1:", part1)
    print("part 2:", part2)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
