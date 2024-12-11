from functools import lru_cache
import time

@lru_cache(maxsize=None)
def solve(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    elif stone == 0:
        res = solve(1, blinks - 1)
    else:
        stone_str = str(stone)
        nb_digits = len(stone_str)
        if nb_digits % 2 == 0:
            res = solve(int(stone_str[:nb_digits//2]), blinks - 1) + solve(int(stone_str[nb_digits//2:]), blinks - 1)
        else:
            res = solve(stone * 2024, blinks - 1)
    return res

def main():
    part1 = 0
    part2 = 0

    stones: list[int] = []
    with open("11.in") as input:
        stones = list(map(int, input.readline().split()))

    part1 = sum(solve(stone, 25) for stone in stones)
    print('part 1:', part1)
    
    part2 = sum(solve(stone, 75) for stone in stones)        
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")