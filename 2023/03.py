import time
import re

def main():
    with open("03.in") as input:
        numbers_spans = { }
        symbols = [ ]
        for row, line in enumerate(input.read().splitlines()):
            matches = re.finditer(r'\d+', line)
            for match in matches:
                span = match.span()
                number= match.group()
                number_spans = numbers_spans.get(row, [])
                number_spans.append((span, int(number)))
                numbers_spans[row] = number_spans
            for x, ch in enumerate(line):
                if not ch.isalnum() and ch != '.':
                    symbols.append((row, x, ch))
        
        part_numbers = [ ]
        gear_ratios = []
        for row, x, ch in symbols:
            gear_numbers = [ ]
            for r in range(row - 1, row + 2):
                row_number_spans = numbers_spans[r]
                for number_span in row_number_spans:
                    span = number_span[0]
                    if span[0] <= x + 1 and span[1] - 1 >= x - 1:
                        part_numbers.append(number_span[1])
                        if ch == '*':
                            gear_numbers.append(number_span[1])

            if len(gear_numbers) == 2:
                gear_ratio = gear_numbers[0] * gear_numbers[1]
                gear_ratios.append(gear_ratio)

    print(f"part 1: {sum(part_numbers)}")
    print(f"part 2: {sum(gear_ratios)}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")