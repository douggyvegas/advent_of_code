import time
import re
from typing import Dict, Tuple
import math

index = { 'L': 0, 'R': 1 }

def go_to_next_Z(instructions: str, network: Dict[str, Tuple[str, str]], current: str, count: int) -> Tuple[int, str]:
    current  = network[current][index[instructions[count % len(instructions)]]]
    count += 1
    while not current.endswith('Z'):
        current  = network[current][index[instructions[count % len(instructions)]]]
        count += 1
    return (count, current)


def main():
    network = { }
    with open("08.in") as input:
        instructions = input.readline()[0:-1]
        for line in input.read().splitlines():
            if len(line) > 0:
                cells = re.findall(r'\w+', line)
                network[cells[0]] = (cells[1], cells[2])

    # i = 0
    # next = 'AAA'
    # while next != 'ZZZ':
    #     next = network[next][index[instructions[i % len(instructions)]]]
    #     i += 1

    # print(f"part 1: {i}")

    paths = [ c for c in network.keys() if c.endswith('A') ]
    paths_counts = [ 0 ] * len(paths)

    for path_index in range(len(paths)):
        paths_counts[path_index], paths[path_index] = go_to_next_Z(instructions, network, paths[path_index], paths_counts[path_index])

    lcm = 1
    for i in paths_counts:
        lcm = lcm * i // math.gcd(lcm, i)

    print(f"part 2: {lcm} {paths}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")