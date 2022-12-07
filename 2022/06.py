#!/usr/bin/env python3

def f(message, size):
    for end in range(size, len(message)):
        part = message[end - size:end]
        if len(set(part)) == len(part):
            return end

def main():
    with open('06.in') as input:
        for line in input.read().splitlines():
            print(f(list(line), 4))
            print(f(list(line), 14))

__name__ == "__main__" and main()