#!/usr/bin/env python3

from dataclasses import dataclass, field
import time
import re
import copy

@dataclass
class Monkey:
    id: int = -1
    items: list[int] = field(default_factory=list)
    op: str = ""
    test_divider: int = -1
    next_monkey_id: list[int] = field(default_factory=list)
    inspected_items_counter: int = 0

def monkey_business(monkeys, number_of_rounds: int, worry_divider: int, lcm: int):
    for round in range(number_of_rounds):
        if round % 100 == 0:
            print(round)
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspected_items_counter += 1
                old = monkey.items.pop(0)
                new = eval(monkey.op) // worry_divider % lcm
                if new % monkey.test_divider == 0:
                    monkeys[monkey.next_monkey_id[0]].items.append(new)
                else:
                    monkeys[monkey.next_monkey_id[1]].items.append(new)

    monkeys = sorted(monkeys, key = lambda m: m.inspected_items_counter, reverse=True)
    monkey_business = monkeys[0].inspected_items_counter * monkeys[1].inspected_items_counter
    return monkey_business


def main():
    monkeys = [ ]
    lcm = 1
    with open('11.in') as input:
        current_monkey = None
        for line in input.read().splitlines():
            match = re.match("Monkey (\d+):", line)
            if match:
                if current_monkey:
                    monkeys.append(current_monkey)
                current_monkey = Monkey()
                current_monkey.id = int(match.group(1))
                current_monkey.next_monkey_id = [ -1, -1 ]
            else:
                match = re.match("\s*Starting items: (((\d+),*\s*)+)", line)
                if match:
                    for item in match.group(1).split(","):
                        current_monkey.items.append(int(item))
                else:
                    match = re.match("\s*Operation: ([\w\+\*= ]+)", line)
                    if match:
                        current_monkey.op = match.group(1).replace("new = ", "")
                    else:
                        match = re.match("\s*Test: divisible by (\d+)", line)
                        if match:
                            current_monkey.test_divider = int(match.group(1))
                            lcm *= current_monkey.test_divider
                        else:
                            match = re.match("\s*If true: throw to monkey (\d+)", line)
                            if match:
                                current_monkey.next_monkey_id[0] = int(match.group(1))
                            else:
                                match = re.match("\s*If false: throw to monkey (\d+)", line)
                                if match:
                                    current_monkey.next_monkey_id[1] = int(match.group(1))

    monkeys.append(current_monkey)

    print(monkey_business(copy.deepcopy(monkeys), 20, 3, lcm))
    print(monkey_business(copy.deepcopy(monkeys), 10000, 1, lcm))


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
