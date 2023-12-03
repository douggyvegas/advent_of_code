import time
import re

wordToNum = [ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" ]

def str_to_num(s: str) -> int:
    try:
        v = wordToNum.index(s) + 1
    except ValueError:
        v = int(s)
    return v

def str_reversed_to_num(s: str) -> int:
    try:
        v = [ s[::-1] for s in wordToNum ].index(s) + 1
    except ValueError:
        v = int(s)
    return v


def main():
    sum = 0
    with open("01.in") as input:
         for line in input.read().splitlines():

            first = 0
            last = 0

            re_forward = r'(\d|' + '|'.join(wordToNum) + ')'
            first_match = re.findall(re_forward, line)
            if first_match is not None:
                first = str_to_num(first_match[0])
            
            re_backward = r'(\d|' + '|'.join([ s[::-1] for s in wordToNum ]) + ')'
            last_match = re.findall(re_backward, line[::-1])
            if last_match is not None:
                last = str_reversed_to_num(last_match[0])

            num = int(str(first) + str(last))
            print(line, str(first), str(last), str(num))
            sum += num
            print(str(sum))

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")