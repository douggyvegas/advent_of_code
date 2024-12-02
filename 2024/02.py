import time
import re

def computeUnsafeIndex(levels: list[int]) -> int:
    increasing = True
    for l in range(len(levels)):
        if l > 0:
            diff = levels[l] - levels[l - 1]
            if diff != 0:
                increasing = diff > 0
                break
    
    previous_increasing = None
    for l in range(1, len(levels)):
        diff = levels[l] - levels[l - 1]
        if diff == 0:
            return l
        
        increasing = diff > 0
        if previous_increasing is not None and increasing != previous_increasing:
            return l
        
        previous_increasing = increasing
        if (increasing and not (1 <= diff <= 3)) or (not increasing and not (-3 <= diff <= -1)):
            return l
            
    return -1

def main():
    safe_count_1 = 0
    safe_count_2 = 0
    with open("02.in") as input:
        for line in input.read().splitlines():
            levels = list(map(int, line.split(" ")))
            unsafe_index = computeUnsafeIndex(levels)
            if unsafe_index == -1:
                safe_count_1 += 1
                safe_count_2 += 1
            else:
                for l in range(unsafe_index + 1):
                    dampened_levels = [ level for i, level in enumerate(levels) if i != l ]
                    dampened_levels_unsafe_index = computeUnsafeIndex(dampened_levels)
                    if dampened_levels_unsafe_index == -1:
                        safe_count_2 += 1
                        break

    print('part 1:', safe_count_1)
    print('part 2:', safe_count_2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")