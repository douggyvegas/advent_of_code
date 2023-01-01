#!/usr/bin/env python3

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
import logging
import time

def dfs(graph, start, end=None, path=[]):
    q = [start]
    while q:
        v = q.pop(0)
        if v not in path:
            path = [ v ] + path
            q = graph[v] + q
            if v == end:
                return path

    return path

def transformEquation(eq, var):
    tokens = eq.split(" ")
    op = tokens[3]

    if op == "+" or op == "*":
        op = revertOperator(op)
        if var == tokens[2]:
            eq = "{} = {} {} {}".format(var, tokens[0], op, tokens[4])
        elif var == tokens[4]:
            eq = "{} = {} {} {}".format(var, tokens[0], op, tokens[2])
    else:
        if var == tokens[2]:
            op = revertOperator(op)
            eq = "{} = {} {} {}".format(var, tokens[0], op, tokens[4])
        elif var == tokens[4]:
            eq = "{} = {} {} {}".format(var, tokens[2], op, tokens[0])

    return eq

def revertOperator(op):
    match op:
        case '+': return '-'
        case '-': return '+'
        case '*': return '/'
        case '/': return '*'

def computeDependencies(dependencies, lines, line):
    tokens = line.split(" ")
    var = tokens[0]
    if len(tokens) == 3:
        dependencies[var] = [ ]
    else:
        dependencies[var] = [ tokens[2], tokens[4] ]
    lines[var] = line

def main():

    dependencies = { }
    lines = { }

    with open('21.in') as input:
        for line in input.read().splitlines():
            computeDependencies(dependencies, lines, line.replace(":", " ="))

    prog_part1 = ""
    for var in dfs(dependencies, "root"):
        prog_part1 += lines[var] + "\n"
    prog_part1 += "print('part1: root =', root)"
    exec(prog_part1)

    lines['root'] = lines['root'].replace("+", "-")

    # revert equations from humn up to root
    q = deque()
    q.append('humn')
    processed = set()
    while len(q) != 0:
        var = q.pop()
        for next in [ k for k, d in dependencies.items() if var in d ]:
            if next not in processed:
                eq = lines[next]
                tokens = eq.split()
                if next not in processed and len(tokens) == 5:
                    lines.pop(next, None)
                    dependencies[next] = [ ]

                    new_eq = transformEquation(eq, var)
                    tokens = new_eq.split()
                    lines[var] = new_eq
                    dependencies[var] = [ tokens[2], tokens[4] ]
                    processed.add(var)

                    q.append(tokens[2])
                    q.append(tokens[4])

    lines['root'] = 'root = 0'

    prog_part2 = ""
    for var in dfs(dependencies, "humn"):
        prog_part2 += lines[var] + "\n"
    prog_part2 += "print('part2: humn =', humn)"
    exec(prog_part2)


start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")