import time
import re
import sys

def main():
    max_cubes_by_color = { 'red': 12, 'green': 13, 'blue': 14 }
    with open("02.in") as input:
        possible_sum = 0
        power_sum = 0
        for line in input.read().splitlines():
            possible = True
            power = 1
            min_cubes_by_color = { 'red': 0, 'green': 0, 'blue': 0 }
            game_id = 0
            parts = line.split(':')
            match = re.search(r"Game (\d+)", parts[0])
            if match:
                game_id = int(match.groups()[0])
            sub_games = parts[1].split(';')
            for sub_game in sub_games:
                colors_groups = sub_game.split(',')
                for color_group in colors_groups:
                    match = re.search(r"(\d+) (red|blue|green)", color_group)
                    if match:
                        color_cubes_count = int(match.groups()[0])
                        color = match.groups()[1]
                        possible &= color_cubes_count <= max_cubes_by_color[color]
                        if color_cubes_count > min_cubes_by_color[color]:
                            min_cubes_by_color[color] = color_cubes_count

            power = min_cubes_by_color['red'] * min_cubes_by_color['green'] * min_cubes_by_color['blue']
            power_sum += power

            if possible:
                possible_sum += game_id

        print(f"part 1: {possible_sum}")
        print(f"part 2: {power_sum}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")