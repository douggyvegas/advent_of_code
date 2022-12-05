#!/usr/bin/env python3

from collections import deque
import re

def main():
    instructions = False
    part1_stack = [deque() for i in range(9)]
    part2_stack = [deque() for i in range(9)]
    with open('05.in') as input:
        for line in input.read().splitlines():
            if len(line) >= 2 and line[1] == '1':
                instructions = True

            if not instructions:
                for column in range(9):
                    index = column * 4 + 1
                    if index < len(line):
                        if line[index] != " ":
                            part1_stack[column].append(line[index])
                            part2_stack[column].append(line[index])
            else:
                match = re.match("move (\d+) from (\d+) to (\d+)", line)
                if match:
                    count = int(match.group(1))
                    from_stack = int(match.group(2)) - 1
                    to_stack = int(match.group(3)) - 1

                    part2_picked = []
                    for i in range(count):
                        box = part1_stack[from_stack].popleft()
                        part1_stack[to_stack].appendleft(box)
                        part2_picked += part2_stack[from_stack].popleft()

                    for i in range(len(part2_picked)):
                        part2_stack[to_stack].appendleft(part2_picked[len(part2_picked) - i - 1])

    print(''.join([ str(s[0]) for s in part1_stack if len(s) > 0]))
    print(''.join([ str(s[0]) for s in part2_stack if len(s) > 0]))

__name__ == "__main__" and main()
