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

        l = len(ids[0]) // 2
        if l == 0:
            l = 1

        start = int(ids[0][:l])
        end = int(ids[1][:len(ids[1]) - len(ids[0]) + l])

        print("start,end =", start, end)

        for i in range(start, end + 1):
            n = int(''.join([ str(i),str(i) ]))

            if n >= int(ids[0]) and n <= int(ids[1]):
                part1 += n


    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")