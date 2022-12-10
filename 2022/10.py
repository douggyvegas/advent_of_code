#!/usr/bin/env python3

import time

def main():
    with open('10.in') as input:
        program = input.read().splitlines()

    cycle = 0
    x = 1
    add_x = 0
    next_instruction_cycle = 1
    signal_strength = 0
    screen = [ ]
    screen_line = ""
    while len(program) > 0 or cycle != next_instruction_cycle:

        cycle += 1
        
        if next_instruction_cycle == cycle:
            if add_x:
                x += add_x
                add_x = None
            if len(program) > 0:
                current_instruction = program.pop(0)

        if current_instruction:
            if current_instruction.startswith("addx"):
                next_instruction_cycle = cycle + 2
                add_x = int(current_instruction.split(" ")[1])
            elif current_instruction == "noop":
                next_instruction_cycle = cycle + 1
            current_instruction = None

        # signal strength
        if cycle % 40 == 20:
            signal_strength += cycle * x

        # draw pixels
        if x - 1 <= (cycle - 1) % 40 < x + 2:
            screen_line += '#'
        else:
            screen_line += ' '
        if cycle % 40 == 0:
            screen.append(screen_line)
            screen_line = ""
        
    print("signal_strength =", signal_strength)

    for line in screen:
        print(line)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
