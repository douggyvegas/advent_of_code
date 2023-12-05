import time
import re

def main():
    total = 0
    points_and_instances_by_card = { }
    with open("04.in") as input:
        for line in input.read().splitlines():
            parts = re.split("[:|]", line)
            card_id = int(re.findall(r'\d+', parts[0])[0])
            winning = set([ int(n) for n in re.findall(r'\d+', parts[1]) ])
            own = set([ int(n) for n in re.findall(r'\d+', parts[2]) ])
            matching_numbers = len(winning.intersection(own))
            points_and_instances_by_card[card_id] = (matching_numbers, 1)
            if matching_numbers > 0:
                game_points = pow(2, matching_numbers - 1)
                total += game_points

    for card, points_and_instances in points_and_instances_by_card.items():
        for next_card in range(card + 1, card + 1 + points_and_instances[0]):
            next_card_points_and_instances = points_and_instances_by_card[next_card]
            points_and_instances_by_card[next_card] = ( next_card_points_and_instances[0], next_card_points_and_instances[1] + points_and_instances[1] )

    scratchcards = sum([ pi[1] for pi in points_and_instances_by_card.values() ])

    print(f"part 1: {total}")
    print(f"part 2: {scratchcards}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")