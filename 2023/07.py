import functools
import time
from typing import Dict

cards_no_joker = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
cards_with_joker = ['A','K','Q','T','9','8','7','6','5','4','3','2','J']

def get_kind(cards_count: Dict[str, int], with_joker: bool) -> int:
    number_of_jokers = 0
    if with_joker:
        number_of_jokers = cards_count.pop('J')  
    counts = sorted(cards_count.values(), reverse=True)
    counts[0] += number_of_jokers
    if counts[0] == 5:
        return 6
    if counts[0] == 4:
        return 5
    if counts[0] == 3 and counts[1] == 2:
        return 4
    if counts[0] == 3:
        return 3
    if counts[0] == 2 and counts[1] == 2:
        return 2
    if counts[0] == 2:
        return 1
    return 0

def compare_hands_and_bids(hab1: tuple, hab2: tuple, with_joker) -> int:
    h1 = hab1[0]
    h2 = hab2[0]
    h1_cards_count = dict(zip(cards_no_joker, [ h1.count(c) for c in cards_no_joker ]))
    h2_cards_count = dict(zip(cards_no_joker, [ h2.count(c) for c in cards_no_joker ]))

    kind_h1 = get_kind(h1_cards_count, with_joker)
    kind_h2 = get_kind(h2_cards_count, with_joker)

    if kind_h1 > kind_h2:
        return 1
    if kind_h2 > kind_h1:
        return -1
    if kind_h1 == kind_h2:
        for c in range(len(h1)):
            if with_joker:
                diff = cards_with_joker.index(h2[c]) - cards_with_joker.index(h1[c])
            else:
                diff = cards_no_joker.index(h2[c]) - cards_no_joker.index(h1[c])
            if diff > 0:
                return 1
            if diff < 0:
                return -1
    return 0

def compare_hands_and_bids_with_joker(hab1: tuple, hab2: tuple) -> int:
    return compare_hands_and_bids(hab1, hab2, True)

def compare_hands_and_bids_no_joker(hab1: tuple, hab2: tuple) -> int:
    return compare_hands_and_bids(hab1, hab2, False)

def solve(hands_and_bids, with_joker):
    if with_joker:
        hands_and_bids.sort(key=functools.cmp_to_key(compare_hands_and_bids_with_joker))
    else:
        hands_and_bids.sort(key=functools.cmp_to_key(compare_hands_and_bids_no_joker))
    winnings = 0
    for i, hand_and_bid in enumerate(hands_and_bids):
        winnings += (i + 1) * int(hand_and_bid[1])
    return winnings

def main():
    hands_and_bids = [ ]
    with open("07.in") as input:
        for line in input.read().splitlines():
            hands_and_bids.append(tuple(line.split(" ")))
        
    print(f"part 1: {solve(hands_and_bids, False)}")
    print(f"part 2: {solve(hands_and_bids, True)}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")