import time
import re
import math

def solve(data):
    s = 1
    for i in range(len(data[0])):
        T = data[0][i]
        D = data[1][i]
        r = math.sqrt(T*T - 4*D)
        p1 = -0.5*(-T-r)
        p2 = -0.5*(-T+r)
        lower = math.ceil(min(p1, p2))
        lower += 1 if lower == p1 or lower == p2 else 0
        upper = math.floor((max(p1, p2)))
        upper += 1 if upper == p1 or upper == p2 else 0
        s *= len(range(lower, upper + 1))
    return s

def main():
    with open("06.in") as input:
        data_part1 = []
        data_part2 = []
        for line in input.read().splitlines():
            data_part1.append([ int(n) for n in re.findall(r'\d+', line) ])
            data_part2.append([ int(''.join(re.findall(r'\d+', line))) ])
        
        print(f"part 1: {solve(data_part1)}")
        print(f"part 2: {solve(data_part2)}")


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")