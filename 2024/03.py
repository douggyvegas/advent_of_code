import time
import re

def main():
    part1 = 0
    part2 = 0
    with open("03.in") as input:
        enabled = True
        for line in input.read().splitlines():
            pattern1 = re.compile(r"mul\((\d+),(\d+)\)")
            pattern2 = re.compile(r"don't|do|mul\((\d+),(\d+)\)")
            for match in re.finditer(pattern1, line):
                part1 += int(match.group(1)) * int(match.group(2))

            for match in re.finditer(pattern2, line):
                if match.group(0) == "do":
                    enabled = True
                elif match.group(0) == "don't":
                    enabled = False
                elif enabled:
                    part2 += int(match.group(1)) * int(match.group(2))

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")