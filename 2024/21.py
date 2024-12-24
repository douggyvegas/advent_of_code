from functools import lru_cache
import time

@lru_cache(maxsize=None)
def move_from_to(from_key: str, to_key: str) -> str:
    keypad = {'7':(0,0), '8':(1,0), '9':(2,0),
              '4':(0,1), '5':(1,1), '6':(2,1),
              '1':(0,2), '2':(1,2), '3':(2,2),
              ' ':(0,3), '0':(1,3), 'A':(2,3)}
    x1, y1 = keypad[from_key]
    x2, y2 = keypad[to_key]
    mx, my = keypad[' ']
    keys = ''
    while (x1, y1) != (x2, y2):
        if x2 < x1:
            if (y1 == my) and (x2 == mx):
                keys += '^' * abs(y2 - y1)
                y1 = y2
            else:
                keys += '<'
                x1 -= 1
        elif y2 < y1:
            keys += '^'
            y1 -= 1
        elif y2 > y1:
            if (x1 == mx) and (y2 == my):
                keys += '>' * abs(x2 - x1)
                x1 = x2
            else:
                keys += 'v'
                y1 += 1
        elif x2 > x1:
            keys += '>'
            x1 += 1
    return keys

def main():
    part1 = 0
    part2 = 0
    combinations: list[str] = []
    with open("21.in") as input:
        for line in input.read().splitlines():
            combinations += [ line ]

    print(combinations)

    keymap: dict[tuple[str, str], str] = {}
    keymap[('<','<')] = ''
    keymap[('<','>')] = '>>'
    keymap[('<','^')] = '>^'
    keymap[('<','v')] = '>'
    keymap[('<','A')] = '>>^'
    keymap[('>','<')] = '<<'
    keymap[('>','>')] = ''
    keymap[('>','^')] = '<^'
    keymap[('>','v')] = '<'
    keymap[('>','A')] = '^'
    keymap[('^','>')] = 'v>'
    keymap[('^','<')] = 'v<'
    keymap[('^','^')] = ''
    keymap[('^','v')] = 'v'
    keymap[('^','A')] = '>'
    keymap[('v','<')] = '<'
    keymap[('v','>')] = '>'
    keymap[('v','^')] = '^'
    keymap[('v','v')] = ''
    keymap[('v','A')] = '>^'
    keymap[('A','<')] = 'v<<'
    keymap[('A','>')] = 'v'
    keymap[('A','^')] = '<'
    keymap[('A','v')] = '<v'
    keymap[('A','A')] = ''
    
    part1 = solve(combinations, keymap, 3)
    print('part 1:', part1)
                
    part2 = solve(combinations, keymap, 26)
    print('part 2:', part2)

def solve(combinations, keymap, number_of_keypads):
    res = 0
    for combination in combinations:
        print(combination)
        keys: list[str] = [ "" ] * number_of_keypads
        from_key = 'A'
        keys[0] = ""
        for to_key in combination:
            keys[0] += move_from_to(from_key, to_key)
            keys[0] += 'A'
            from_key = to_key
    
        for keypad in range(1, number_of_keypads):
            from_key = 'A'
            for to_key in keys[keypad - 1]:
                keys[keypad] += keymap[(from_key, to_key)]
                keys[keypad] += 'A'
                from_key = to_key
       
        for keypad in range(0, number_of_keypads):
            print(keys[keypad])
                
        res += len(keys[2]) * int(combination[:-1])
    
    return res

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")