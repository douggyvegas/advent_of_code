import copy
from functools import cmp_to_key
import time
import re
from typing import Self

class Node:
    i1: str
    op: str
    i2: str
    out: str
    init: bool

    def __init__(self: Self, i1: str, op: str, i2: str, out: str, init: bool = False):
        self.i1 = i1 if i1 <= i2 else i2
        self.op = op
        self.i2 = i2 if i1 <= i2 else i1
        self.out = out
        self.init = init

    def compute(self: Self, gates: dict[str, Self], swapped_gates: dict[str, str] = {}) -> bool:
        out: bool
        if len(self.i1) != 0 and len(self.i2) != 0:
            n1 = gates[swapped_gates[self.i1]] if self.i1 in swapped_gates else gates[self.i1]
            n2 = gates[swapped_gates[self.i2]] if self.i2 in swapped_gates else gates[self.i2]
            v1 = n1.compute(gates, swapped_gates)
            v2 = n2.compute(gates, swapped_gates)
            if self.op == "AND":
                out = v1 & v2
            if self.op == "OR":
                out = v1 | v2
            if self.op == "XOR":
                out = v1 ^ v2
            #print(i1, self.op, i2)
        else:
            out = self.init

        #print(self.out, out)
        return out

    def getAncestors(self, gates:dict[str, Self]) -> set[Self]:
        if len(self.i1) == 0 or len(self.i2) == 0:
            return set()
        else:
            a1 = gates[self.i1].getAncestors(gates)
            a2 = gates[self.i2].getAncestors(gates)
            return set([self]) | a1 | a2

def compareGates(g1: Node, g2: Node):
    BEFORE=-1
    AFTER=1
    res = 0
    if g1.i1.startswith("x"):
        if g2.i1.startswith("x"):
            if g1.i1 < g2.i1:
                res = BEFORE
            elif g1.i1 > g2.i1:
                res = AFTER
        else:
            res = BEFORE
    elif g1.i1.startswith("y"):
        if g2.i1.startswith("x"):
            res = AFTER
        elif g2.i1.startswith("y"):
            if g1.i1 < g2.i1:
                res = BEFORE
            elif g1.i1 > g2.i1:
                res = AFTER
        else:
            res = BEFORE
    else:
        if g1.i1 < g2.i1:
            res = BEFORE
        elif g1.i1 > g2.i1:
            res = AFTER
    print(g1.i1, g2.i1, res)
    return res

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
            
    #print(gates)

    for out, gate in gates.items():
        if out.startswith("z"):
            part1 += gate.compute(gates, {}) << int(out[1:])

    print('part 1:', part1)

    with open("24.mmd", "w") as out:
        out.write("flowchart TD\n")
        for gate in sorted(list(gates.values()), key=cmp_to_key(compareGates)):
            if gate.i1 != "":
                out.write(f"\t{gate.i1}{{{gate.i1}}} --> {id(gate)}[{gate.op}]\n")
                out.write(f"\t{gate.i2}{{{gate.i2}}} --> {id(gate)}[{gate.op}]\n")
                out.write(f"\t{id(gate)}[{gate.op}] --> {gate.out}{{{gate.out}}}\n")

    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")