#!/usr/bin/env python3

def getSection(section):
    range_section = range(int(section.split('-')[0]), int(section.split('-')[1]) + 1)
    return set(range_section)

def main():
    part1_count = 0
    part2_count = 0
    with open("04.in") as input:
        for sections in input.read().splitlines():
            section1, section2 = getSection(sections.split(',')[0]), getSection(sections.split(',')[1])
            common = section1.intersection(section2)

            if len(common) > 0:
                part2_count += 1
                if common == section1 or common == section2:
                    part1_count += 1

    print(part1_count)
    print(part2_count)
    

__name__ == "__main__" and main()