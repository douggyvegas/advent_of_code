from functools import lru_cache
import time

def getComboOperandValue(o: int, A: int, B: int, C: int) -> int:
    match o:
        case o if 0 <= o < 4:
            return o
        case 4:
            return A
        case 5:
            return B
        case 6:
            return C
        case 7:
            print("INVALID OPERAND:", o)
    return 0

@lru_cache(maxsize=1000000)
def execute(i: int, o: int, A: int, B: int, C: int) -> tuple[int, int, int, int | None, int | None]:
    match i:
        case 0: # adv/cmb
            A = A >> getComboOperandValue(o, A, B, C)
        case 1: # bxl/lit
            B = B ^ o
        case 2: # bst/cmb
            B = getComboOperandValue(o, A, B, C) & 7
        case 3: # jnz/lit
            if A != 0:
                return (A, B, C, o, None)
        case 4: # bxc
            B = B ^ C
        case 5: # out/cmb
            return (A, B, C, None, getComboOperandValue(o, A, B, C) & 7)
        case 6: #bdv/cmb
            B = A >> getComboOperandValue(o, A, B, C)
        case 7: #cdv/cmb
            C = A >> getComboOperandValue(o, A, B, C)
    
    return (A, B, C, None, None)

def solve(program: list[int], A: int, B: int, C: int) -> list[int]:
    output: list[int] = []
    ip: int = 0
    while 0 <= ip < len(program) - 1:
        i = program[ip]
        o = program[ip + 1]
        A, B, C, new_ip, value = execute(i, o, A, B, C)
        if value is not None:
            output.append(value)
        if new_ip is not None:
            ip = new_ip
        else:
            ip += 2

    return output


def solvePart2(memory: dict[int, set[int]], program: list[int], pos: int, number: int) -> int:
    if pos < 0:
        return number

    number <<= 3
    for candidate in memory[program[pos]]:
        if (candidate & 1016) == (number & 1016):
            A = solvePart2(memory, program, pos - 1, number | candidate)
            if A != -1:
                return A
    
    return -1

def main():
    part1 = 0
    part2 = 0
    A: int = 0
    B: int = 0
    C: int = 0
    program: list[int] = []
    with open("17.in") as input:
        for line in input.read().splitlines():
            if line.startswith("Register A:"):
                A = int(line.split(": ")[1])
            elif line.startswith("Register B:"):
                B = int(line.split(": ")[1])
            elif line.startswith("Register C:"):
                C = int(line.split(": ")[1])
            elif line.startswith("Program: "):
                program = list(map(int, line.split(": ")[1].split(",")))
    
    print(A, B, C, program)
    
    part1 = ','.join(list(map(str, solve(program, A, B, C))))
    print('part 1:', part1)
    
    memory: dict[int, set[int]] = dict()
    for a in range(1024): # 10 bits
        s = solve(program, a, 0, 0)[0]
        if s not in memory:
            memory[s] = set()
        memory[s].add(a)
    part2 = solvePart2(memory, program, len(program) - 1, 0)
    print(solve(program, part2, 0, 0))
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")