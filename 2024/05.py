from functools import cmp_to_key
import time

def main():
    part1 = 0
    part2 = 0
    rules:dict[int, list[int]] = {}
    updates: list[list[int]] = []
    with open("05.in") as input:
        for line in input.read().splitlines():
            if '|' in line:
                tokens = line.split('|')
                x = int(tokens[0])
                y = int(tokens[1])
                if x not in rules.keys():
                    rules[x] = []
                rules[x].append(y)
            elif len(line) > 0:
                updates.append(list(map(int, line.split(','))))
    
    def compare(x: int, y:int) -> int:
        if x == y:
            return 0
        if x in rules.keys() and y in rules[x]:
            return -1
        return 1
    
    for update in updates:
        sorted_updated = sorted(update, key=cmp_to_key(compare))
        if update == sorted_updated:
            part1 += update[len(update) // 2]
        else:
            part2 += sorted_updated[len(sorted_updated) // 2]
    
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")