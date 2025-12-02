import time

def main():
    part1 = 0
    part2 = 0
    current = 50
    with open("01.in") as input:
        for line in input.read().splitlines():
            dist = int(line[1:])
            while dist > 0:
                if line[0] == 'R':
                    step = min(100 - current, dist)
                    current += step
                else:
                    step = min(100 if current == 0 else current, dist)
                    current -= step

                current = current % 100

                if current == 0:
                    part2 += 1

                dist -= step
            
            if current == 0:
                part1 += 1
            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")