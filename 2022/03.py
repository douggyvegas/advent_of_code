#!/usr/bin/env python3

def getPriority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 27
    print("ERROR")
    return 0

def main():
    common_priorities = 0
    badge_priorities = 0
    with open("03.in") as input:
        group = []
        for content in input.read().splitlines():
            group.append(set(content))
            if len(group) == 3:
                badge = set.intersection(group[0], group[1], group[2])
                badge_priorities += getPriority(badge.pop())
                group = []

            compartment1, compartment2 = set(content[:len(content)//2]), set(content[len(content)//2:])
            common = compartment1.intersection(compartment2)
            common_priorities += getPriority(common.pop())
    
    print("common priorities = ", common_priorities)
    print("badge priorities = ", badge_priorities)



__name__ == "__main__" and main()