#!/usr/bin/env python3

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
import logging
import time

class Node:
    def __init__(self, data) -> None:
        self.next = None
        self.prev = None
        self.data = data

    def __str__(self):
        return str(self.data)

@dataclass
class Sequence:
    head: Node = None
    last: Node = None
    size: int = 0

    def append(self, data) -> Node:
        node = Node(data)
        
        if self.size == 0:
            self.head = node
            self.last = node
        
        node.prev = self.last
        self.last.next = node
        self.last = node
        node.next = self.head
        self.head.prev = node
        self.size += 1
        return node

    def move(self, node):
        if node.data == 0:
            return

        if node == self.head:
            self.head = node.next

        node.prev.next = node.next
        node.next.prev = node.prev

        for _ in range(abs(node.data) % (self.size - 1)):
            if node.data > 0:
                node.prev = node.next
                node.next = node.next.next
            elif node.data < 0:
                node.next = node.prev
                node.prev = node.prev.prev

        node.prev.next = node
        node.next.prev = node

        if node.prev == self.last and node != self.head:
            self.last = node

    def __str__(self):
        curr = self.head
        s = [ ]
        while curr != self.last:
            s += [ str(curr) ]
            curr = curr.next
        s += [ str(self.last) ]
        forward =  ",".join(s)
        return '[ ' + forward + ' ]'

def groveCoordinates(sequence):
    curr = sequence.head
    sum = 0
    while curr.data != 0:
        curr = curr.next
    for i in range(1, 3001):
        curr = curr.next
        if i == 1000 or i == 2000 or i == 3000:
            sum += curr.data
    return sum

def main():

    logging.basicConfig(level=logging.INFO)

    sequence = Sequence()
    initial = list()
    with open('20.in') as input:
        for line in input.read().splitlines():
            node = sequence.append(int(line))
            initial.append(node)

    for n in initial:
        sequence.move(n)
    print("part 1:", groveCoordinates(sequence))

    sequence = Sequence()
    initial = list()
    with open('20.in') as input:
        for line in input.read().splitlines():
            node = sequence.append(int(line) * 811589153)
            initial.append(node)
        
    for i in range(10):
        for n in initial:
            sequence.move(n)

    print("part 2:", groveCoordinates(sequence))

start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")