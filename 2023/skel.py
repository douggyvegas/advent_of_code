import time
import re

def main():
    with open("xx.ex") as input:
        for line in input.read().splitlines():
            print("letsgo")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")