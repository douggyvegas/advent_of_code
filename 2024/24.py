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
    wrong_gates: list[str] = []
    for bit in range(wrong_bits.bit_length()):
        if wrong_bits & (1 << bit) != 0:
            out = "z" + "{:02d}".format(bit)
            gate = gates[out]
            if gate is not None:
                swap_candidates |= gate.getAncestors(gates)
                wrong_gates.append(out)

    print(wrong_gates)
    print(len(swap_candidates))    

    # identify culprit for each wrong bit
    
    
    # swap frenzy
    swap_candidates_array = list([ n.out for n in swap_candidates ])
    for i1, out_i1 in enumerate(swap_candidates_array[:-1]):
        for j1 in range(i1+1, len(swap_candidates_array)):
            out_j1 = swap_candidates_array[j1]
            if len(gates[out_i1].getAncestors(gates).intersection(gates[out_j1].getAncestors(gates))) == 0:
                for i2 in range(i1+1, len(swap_candidates_array) - 1):
                    if i2 != j1:
                        out_i2 = swap_candidates_array[i2]
                        for j2 in range(i2+1, len(swap_candidates_array)):
                            if j2 != j1:
                                out_j2 = swap_candidates_array[j2]
                                if len(gates[out_i2].getAncestors(gates).intersection(gates[out_j2].getAncestors(gates))) == 0:
                                    for i3 in range(i2+1, len(swap_candidates_array) - 1):
                                        if i3 != j1 and i3 != j2:
                                            out_i3 = swap_candidates_array[i3]
                                            for j3 in range(i3+1, len(swap_candidates_array)):
                                                if j3 != j1 and j3 != j2:
                                                    out_j3 = swap_candidates_array[j3]
                                                    if len(gates[out_i3].getAncestors(gates).intersection(gates[out_j3].getAncestors(gates))) == 0:
                                                        for i4 in range(i3+1, len(swap_candidates_array) - 1):
                                                            if i4 != j1 and i4 != j2 and i4 != j3:
                                                                out_i4 = swap_candidates_array[i4]
                                                                for j4 in range(i4+1, len(swap_candidates_array)):
                                                                    if j4 != j1 and j4 != j2 and j4 != j3:
                                                                        out_j4 = swap_candidates_array[j4]
                                                                        if len(gates[out_i4].getAncestors(gates).intersection(gates[out_j4].getAncestors(gates))) == 0:
                                                                            swapped_gates: dict[str, str] = {}
                                                                            swapped_gates[out_i1] = out_j1
                                                                            swapped_gates[out_j1] = out_i1
                                                                            swapped_gates[out_i2] = out_j2
                                                                            swapped_gates[out_j2] = out_i2
                                                                            swapped_gates[out_i3] = out_j3
                                                                            swapped_gates[out_j3] = out_i3
                                                                            swapped_gates[out_i4] = out_j4
                                                                            swapped_gates[out_j4] = out_i4
                                                                            z = good_bits
                                                                            for out in wrong_gates:
                                                                                z += gates[out].compute(gates, swapped_gates) << int(out[1:])
                                                                            #print(i1, j1, i2, j2, i3, j3, i4, j4, z, expected)
                                                                            if z == expected:
                                                                                part2 = ",".join(sorted(swapped_gates.keys()))
                                                                
            

    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")