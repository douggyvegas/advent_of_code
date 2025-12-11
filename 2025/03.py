import time

def main():
    part1 = 0
    part2 = 0
    with open("03.in") as input:
        for line in input.read().splitlines():
            max_i = 0
            max_l = '0'
            for i in range(len(line) - 1):
                if line[i] > max_l:
                    max_l = line[i]
                    max_i = i
            max_r = '0'
            for i in range(len(line) - 1, max_i, -1):
                if line[i] > max_r:
                    max_r = line[i]
            part1 += int("".join([ max_l, max_r ]))

            max_n = [ '0' ] * 12
            max_in = [ 0 ] * 12
            for n in range(12):
                start = (max_in[n - 1] + 1) if n > 0 else 0
                end = len(line) - 11 + n
                for i in range(start, end):
                    if line[i] > max_n[n]:
                        max_n[n] = line[i]
                        max_in[n] = i
            part2 += int("".join(max_n))
            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")