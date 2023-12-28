from collections import OrderedDict
import time
import re
from typing import Dict

def aoc_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

def main():
    conf : Dict[int, OrderedDict[str, int]]= { }
    for i in range(256):
        conf[i] = OrderedDict()
    with open("15.in") as input:
        for line in input.read().splitlines():
            tokens=line.split(',')
            part_1 = sum([ aoc_hash(t) for t in tokens])
            print(f"part 1: {part_1}")

            for token in tokens:
                operator_index = token.find('=')
                if operator_index != -1:
                    lens = token[:operator_index]
                    focal = int(token[operator_index + 1:])
                    box = aoc_hash(lens)
                    conf[box][lens] = focal
                else:
                    operator_index = token.find('-')
                    if operator_index != -1:
                        lens = token[:operator_index]
                        box = aoc_hash(lens)
                        if lens in conf[box].keys():
                            conf[box].pop(lens)

    focusing_power = 0
    for box, lens_conf in conf.items():
        for slot, (lens, focal) in enumerate(lens_conf.items()):
            focusing_power += (box + 1) * (slot + 1) * focal

    print(f"part 2: {focusing_power}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")