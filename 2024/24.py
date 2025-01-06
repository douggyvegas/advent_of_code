import time
import re
from typing import Self

class Node:
    i1: Self | str
    op: str
    i2: Self | str

    out: str
    init: bool

    def __init__(self: Self, i1: Self | str, op: str, i2: Self | str, out: str, init: bool = False):
        self.i1 = i1
        self.op = op
        self.i2 = i2
        self.out = out
        self.init = init

    def resolve(self: Self, gates: dict[str, Self]):
        if isinstance(self.i1, str) and self.i1 != "":
            self.i1 = gates[self.i1]
        if isinstance(self.i2, str) and self.i2 != "":
            self.i2 = gates[self.i2]

    def compute(self: Self) -> bool:
        out: bool
        if isinstance(self.i1, Node) and isinstance(self.i2, Node):
            i1 = self.i1.compute()
            i2 = self.i2.compute()
            if self.op == "AND":
                out = i1 & i2
            if self.op == "OR":
                out = i1 | i2
            if self.op == "XOR":
                out = i1 ^ i2
            #print(i1, self.op, i2)
        else:
            out = self.init

        #print(self.out, out)
        return out

def main():
    part1 = 0
    part2 = 0
    gates: dict[str, Node] = {}
    init = True
    with open("24.in") as input:
        for line in input.read().splitlines():
            if len(line) == 0:
                init = False
            elif init:
                tokens: list[str] = line.split(": ")
                gates[tokens[0]] = Node("", "", "", tokens[0], bool(int(tokens[1])))
                #print(tokens[0], tokens[1])
            else:
                pattern = re.compile(r'([\w\d]+) (XOR|OR|AND) ([\w\d]+) \-> ([\w\d]+)')
                matches = pattern.match(line)
                if matches is not None:
                    groups = matches.groups()
                    #print(groups)
                    gates[groups[3]] = Node(groups[0], groups[1], groups[2], groups[3])
            
    for gate in gates.values():
        gate.resolve(gates)
            
    #print(gates)

    for out, gate in gates.items():
        if out.startswith("z"):
            part1 |= gate.compute() << int(out[1:])
            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")