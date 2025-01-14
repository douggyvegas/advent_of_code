import copy
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
        self.i1 = i1
        self.op = op
        self.i2 = i2
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

    x = 0
    y = 0
    x_pattern = re.compile(r'x\d+')
    y_pattern = re.compile(r'y\d+')
    for gate in gates.values():
        if x_pattern.match(gate.out) is not None:
            x += gate.compute(gates, {}) << int(gate.out[1:])
        elif y_pattern.match(gate.out) is not None:
            y += gate.compute(gates, {}) << int(gate.out[1:])
    expected = x + y
    print(expected, part1)
    wrong_bits = expected ^ part1
    good_bits = ~wrong_bits & ((1 << (expected.bit_length())) - 1)
    swap_candidates: set[Node] = set()
    print("{0:b}".format(wrong_bits))
    print("{0:b}".format(good_bits))
    wrong_gates: list[Node] = []
    for bit in range(wrong_bits.bit_length()):
        if wrong_bits & (1 << bit) != 0:
            out = "z" + "{:02d}".format(bit)
            gate = gates[out]
            if gate is not None:
                swap_candidates |= gate.getAncestors(gates)
                wrong_gates.append(gate)

    print(wrong_gates)
    print(len(swap_candidates))    

    # identify culprit for each wrong bit
    for gate in wrong_gates:
        # check ancestors
        
                                                                
            

    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")