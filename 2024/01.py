import time
import re

def main():
    left:list[int] = []
    right:list[int] = []
    with open("01.in") as input:
         for line in input.read().splitlines():
            tokens = line.split("   ")
            left.append(int(tokens[0]))
            right.append(int(tokens[1]))
    left.sort()
    right.sort()
    
    counts = dict(zip(right, map(lambda r: right.count(r), right)))

    dist = 0
    similarity = 0
    for i, l in enumerate(left):
        dist += abs(l - right[i])
        similarity += l * counts.get(l, 0)

    print('part 1:', dist)
    print('part 2:', similarity)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")