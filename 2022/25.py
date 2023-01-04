#!/usr/bin/env python3

import time

def snafuToDecimal(snafu: str) -> int:
    n = 0
    for p, c in enumerate(reversed(snafu)):
        if c == "=":
            num = -2
        elif c == "-":
            num = -1
        else:
            num = int(c)
        n += num * (5 ** p)
    return n

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(n % b)
        n //= b
    return digits[::-1]

def decimalToSnafu(dec: int) -> str:
    digits = [ int(n) for n in numberToBase(dec, 5) ]
    i = len(digits)
    while i != 0:
        i -= 1
        if digits[i] > 2:
            digits[i] -= 5
            if i > 0:
                digits[i - 1] += 1
            else:
                digits.insert(0, 1)
                i += 1
    
    snafu = ""
    for d in digits:
        if d == -2:
            snafu += "="
        elif d == -1:
            snafu += "-"
        else:
            snafu += str(d)

    return snafu

def main():
    with open('25.in') as input:
        snafus = input.read().splitlines()

    total = decimalToSnafu(sum([ snafuToDecimal(snafu) for snafu in snafus ]))
    print(total)    
    

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")