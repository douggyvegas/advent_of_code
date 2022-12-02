#!/usr/bin/env python3

def opponentMove(m):
    return ord(m) - ord('A')

def myMove(m):
    return ord(m) - ord('X')

def roundScorePart1(opponent, me):
    return (me - opponent + 1) % 3 * 3 + me + 1

def roundScorePart2(opponent, objective):
    myMove = (opponent + objective + 2) % 3
    return roundScorePart1(opponent, myMove)

def main():
    score_part1 = 0
    score_part2 = 0
    with open('02.in') as input:
        for round in input.read().splitlines():
            opponent = opponentMove(round.split(' ')[0])
            me = myMove(round.split(' ')[1])
            score_part1 += roundScorePart1(opponent, me)
            score_part2 += roundScorePart2(opponent, me)

    print(score_part1)
    print(score_part2)

__name__ == "__main__" and main()
