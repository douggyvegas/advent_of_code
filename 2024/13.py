import math
import re
import time

class Game:
    buttonA: tuple[int, int]
    buttonB: tuple[int, int]
    prize: tuple[int, int]
    prize2: tuple[int, int]

def main():
    part1 = 0
    part2 = 0
    games: list[Game] = []
    button_pattern = re.compile(r'X\+(\d+), Y\+(\d+)')
    prize_pattern = re.compile(r'X=(\d+), Y=(\d+)')
    with open("13.in") as input:
        game: Game = Game()
        for line in input.read().splitlines():
            if line.startswith("Button "):
                b = line[7]
                matches = button_pattern.findall(line[10:])
                if b == 'A':
                    game.buttonA = (int(matches[0][0]), int(matches[0][1]))
                else:
                    game.buttonB = (int(matches[0][0]), int(matches[0][1]))
            elif line.startswith("Prize: "):
                matches = prize_pattern.findall(line[7:])
                game.prize = (int(matches[0][0]), int(matches[0][1]))
                game.prize2 = (game.prize[0] + 10000000000000, game.prize[1] + 10000000000000)
                games.append(game)
                game = Game()

    for game in games:
        nA = (game.prize[0] * game.buttonB[1] - game.prize[1] * game.buttonB[0]) / (game.buttonB[1] * game.buttonA[0] - game.buttonB[0] * game.buttonA[1])
        nB = (game.prize[1] * game.buttonA[0] - game.prize[0] * game.buttonA[1]) / (game.buttonA[0] * game.buttonB[1] - game.buttonA[1] * game.buttonB[0])
        if nA.is_integer() and nB.is_integer():
            part1 += int(nA) * 3 + int(nB)
        nA = (game.prize2[0] * game.buttonB[1] - game.prize2[1] * game.buttonB[0]) / (game.buttonB[1] * game.buttonA[0] - game.buttonB[0] * game.buttonA[1])
        nB = (game.prize2[1] * game.buttonA[0] - game.prize2[0] * game.buttonA[1]) / (game.buttonA[0] * game.buttonB[1] - game.buttonA[1] * game.buttonB[0])
        if nA.is_integer() and nB.is_integer():
            part2 += int(nA) * 3 + int(nB)

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")