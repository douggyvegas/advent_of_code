import time


def main():
    part1 = 0
    part2 = 0
    secret_numbers: list[int] = []
    with open("22.in") as input:
        secret_numbers = list(map(int, input.read().splitlines()))

    deltas_price: dict[tuple[int, int, int, int], list[int]] = {}
    for buyer, secret_number in enumerate(secret_numbers):
        previous_price = None
        deltas: list[int] = []
        for _ in range(2000):
            secret_number = ((secret_number << 6) ^ secret_number) % (1 << 24)
            secret_number = ((secret_number >> 5) ^ secret_number) % (1 << 24)
            secret_number = ((secret_number << 11) ^ secret_number) % (1 << 24)
            price = secret_number % 10
            if previous_price is not None:
                deltas.append(price - previous_price)
            if len(deltas) >= 4:
                d = (deltas[-4], deltas[-3], deltas[-2], deltas[-1])
                if d not in deltas_price:
                    deltas_price[d] = [-1] * len(secret_numbers)
                if deltas_price[d][buyer] == -1:
                    deltas_price[d][buyer] = price
            previous_price = price
        part1 += secret_number

    for _, prices in deltas_price.items():
        gain = sum([p for p in prices if p != -1])
        part2 = max(part2, gain)

    print("part 1:", part1)
    print("part 2:", part2)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
