#!/usr/bin/env python3

def main():
    with open('01.in') as input:
        sorted_cals = sorted(map(lambda group: sum([ int(cals) for cals in group.split('\n') if cals != "" ]), input.read().split('\n\n')), reverse=True)
    
    print(sorted_cals[0])
    print(sum(sorted_cals[:3]))


__name__ == "__main__" and main()
