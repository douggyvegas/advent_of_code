import time

def main():
    part1 = 0
    part2 = 0
    with open("05.in") as input:
        lines = input.read().splitlines()
        blank = lines.index('')
        ranges: list[list[int]] = [ [ int(i) for i in r.split('-') ] for r in lines[:blank] ]
        ingredients: list[int] = [ int(s) for s in lines[blank + 1:] ]
        part1 = len([ i for i in ingredients if any(list(map(lambda r : i in range(r[0], r[1] + 1), ranges)))])

        ranges.sort(key=lambda r: r[0])
        merged = []
        for r in ranges:
            if not merged or merged[-1][1] < r[0]:
                merged.append(r)
            else:
                merged[-1][1] = max(merged[-1][1], r[1])

        part2 = sum([ len(range(r[0], r[1] + 1)) for r in merged ])

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")