import re
import time

def main():
    part1 = 0
    part2 = 0
    with open("02.in") as input:
        ranges = []
        for line in input.read().splitlines():
            ranges += line.split(",")

    print(ranges)

    for r in ranges:
        ids = r.split("-")
        print(r)
        start = int(ids[0])
        end = int(ids[1])
        for n in range(start, end + 1):
            if re.match(r"^(\d+)\1$", str(n)) is not None:
                part1 += n
            if re.match(r"^(\d+)\1+$", str(n)) is not None:
                part2 += n

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")