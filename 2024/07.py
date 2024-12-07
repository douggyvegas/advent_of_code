import time
import re

def has_solution(equation: tuple[int, list[int]], part2: bool) -> bool:
    solution = equation[0]
    operands = equation[1]

    # try addition
    add = operands[0] + operands[1]
    if len(operands) == 2:
        if add == solution:
            return True
    else:
        if has_solution((solution, [add] + operands[2:]), part2):
            return True

    # try multiplication
    mul = operands[0] * operands[1]
    if len(operands) == 2:
        if mul == solution:
            return True
    else:
        if has_solution((solution, [mul] + operands[2:]), part2):
            return True
    
    # try concat
    concat = int(str(operands[0]) + str(operands[1]))
    if len(operands) == 2:
        if concat == solution:
            return True
    else:
        if has_solution((solution, [concat] + operands[2:]), part2):
            return True
        
    return False


def main():
    part1 = 0
    part2 = 0
    equations: list[tuple[int, list[int]]] = []
    with open("07.in") as input:
        for line in input.read().splitlines():
            tokens = line.split(": ")
            operands = tokens[1].split(' ')
            equations.append((int(tokens[0]), list(map(int, operands))))
    
    for equation in equations:
        if has_solution(equation, False):
            part1 += equation[0]
        if has_solution(equation, True):
            part2 += equation[0]

            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")