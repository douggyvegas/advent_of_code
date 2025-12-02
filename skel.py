import time

def main():
    part1 = 0
    part2 = 0
    with open("xx.ex") as input:
        for line in input.read().splitlines():
            print(line)
            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")