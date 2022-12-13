#!/usr/bin/env python3

import functools
import operator
import time
import json

def compare(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0
    
    if type(left) == list and type(right) == list:
        index = 0
        while index < len(left):
            if index == len(right):
                return -1
            result = compare(left[index], right[index])
            if result == 1:
                return 1
            if result == -1:
                return -1
            if result == 0:
                index += 1
        if len(left) == len(right):
            return 0
        else:
            return 1

    if type(left) == list and type(right) == int:
        return compare(left, [ right ])
    if type(left) == int and type(right) == list:
        return compare([ left ], right)

def main():
    counter = 1
    part1 = 0
    lines = []
    with open('13.in') as input:
        for line in input.read().splitlines():
            if line != "":
                parsed_line = json.loads(line)
                lines.append(parsed_line)
            else:
                if compare(lines[::-2], lines[::-1]) == 1:
                    part1 += counter
                counter += 1

    print(part1)

    lines.append([[2]])
    lines.append([[6]])
    lines = sorted(lines, key = functools.cmp_to_key(compare), reverse = True)
    print(functools.reduce(operator.mul, [ index + 1 for index, line in enumerate(lines) if line == [[2]] or line == [[6]] ]))

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
