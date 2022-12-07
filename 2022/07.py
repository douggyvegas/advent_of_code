#!/usr/bin/env python3

import re

class Tree:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.size = 0
        self.children = []

    def getParent(self):
        if self.parent == None:
            return self
        return self.parent

    def getChild(self, dir):
        for child in self.children:
            if child.name == dir:
                return child
        child = Tree(dir, self)
        self.children.append(child)
        return child

    def setSize(self, size):
        self.size += size
        if self.parent:
            self.parent.setSize(size)

    def sumNodesLesserThan(self, size):
        total = 0
        if self.size <= size:
            total += self.size
        for child in self.children:
            total += child.sumNodesLesserThan(size)
        return total

    def findSmallestDirectoryGreaterThan(self, selected_size, min_size):
        if self.size >= min_size and self.size < selected_size:
            selected_size = self.size
        for child in self.children:
            selected_size = child.findSmallestDirectoryGreaterThan(selected_size, min_size)
        return selected_size

def main():
    root = Tree("/", None)
    current = root
    with open('07.in') as input:
        for line in input.read().splitlines():
            if line == "$ cd /":
                current = root
            elif line == "$ cd ..":
                current = current.getParent()
            else:
                match = re.match("\$ cd (\w+)", line)
                if match:
                    current = current.getChild(match.group(1))
                else:
                    match = re.match("(\d+) \w+", line)
                    if match:
                        current.setSize(int(match.group(1)))

    print(root.sumNodesLesserThan(100000))
    required_free_space = 30000000 - (70000000 - root.size)
    print(root.findSmallestDirectoryGreaterThan(root.size, required_free_space))

__name__ == "__main__" and main()