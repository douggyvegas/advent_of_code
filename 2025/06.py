from functools import reduce
from itertools import groupby
import operator
import re
import time

def main():
    part1 = 0
    part2 = 0
    with open("06.in") as input:
        lines = input.read().splitlines()

    problems1 = list(map(list, zip(*[ re.split(r"\s+", line.strip()) for line in lines ])))
    part1 = sum([ reduce(operator.mul if p[-1] == '*' else operator.add, [ int(n) for n in p[:-1] ]) for p in problems1 ])

    problems2 = [ list(g) for k, g in groupby([ (''.join(p[:-1]).strip(), p[-1]) for p in list(map(list, zip(*[ list(line) for line in lines ]))) ], lambda t: len(t[0]) == 0 ) if not k ]
    for p in problems2:
        part2 += reduce(operator.mul if p[0][1] == '*' else operator.add, [ int(s[0]) for s in p ])

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")