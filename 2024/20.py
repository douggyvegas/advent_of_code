import re
import time


def main():
    part1 = 0
    part2 = 0
    track: list[str] = []
    start: tuple[int, int]
    total_picos = 0
    with open("20.in") as input:
        for row, line in enumerate(input.read().splitlines()):
            track.append(line)
            total_picos += line.count(".")
            total_picos += line.count("E")
            if "S" in line:
                start = (line.find("S"), row)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    picos: dict[tuple[int, int], tuple[int, int]] = {}
    pos = start
    previous_dir = -1
    spent_picos = 0
    remaining_picos = total_picos
    picos[start] = (spent_picos, remaining_picos)
    while track[pos[1]][pos[0]] != "E":
        for d, direction in enumerate(directions):
            if previous_dir == -1 or d != (previous_dir + 2) % 4:
                next_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if (
                    track[next_pos[1]][next_pos[0]] == "."
                    or track[next_pos[1]][next_pos[0]] == "E"
                ):
                    spent_picos += 1
                    remaining_picos -= 1
                    picos[next_pos] = (spent_picos, remaining_picos)
                    pos = next_pos
                    previous_dir = d
                    break

    for row, line in enumerate(track):
        for m in re.finditer(r"\.", line):
            pos = (m.start(), row)
            for direction in directions:
                cheat_pos = (pos[0] + direction[0] * 2, pos[1] + direction[1] * 2)
                if (
                    0 <= cheat_pos[0] < len(track[0])
                    and 0 <= cheat_pos[1] < len(track)
                    and (
                        track[cheat_pos[1]][cheat_pos[0]] == "."
                        or track[cheat_pos[1]][cheat_pos[0]] == "E"
                    )
                ):
                    cheat_picos = picos[pos][0] + 2 + picos[cheat_pos][1]
                    saved_picos = total_picos - cheat_picos
                    if saved_picos >= 100:
                        part1 += 1

    max_picos = 20
    cheats: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    for row, line in enumerate(track):
        for m in re.finditer(r"\.|S", line):
            pos = (m.start(), row)
            for dx in range(-max_picos, max_picos + 1):
                for dy in range(-max_picos + abs(dx), max_picos - abs(dx) + 1):
                    cheat_pos = (pos[0] + dx, pos[1] + dy)
                    if (
                        0 <= cheat_pos[0] < len(track[0])
                        and 0 <= cheat_pos[1] < len(track)
                        and (
                            track[cheat_pos[1]][cheat_pos[0]] == "."
                            or track[cheat_pos[1]][cheat_pos[0]] == "E"
                        )
                    ):
                        cheat_picos = picos[pos][0] + abs(dx) + abs(dy) + picos[cheat_pos][1]
                        saved_picos = total_picos - cheat_picos
                        cheats[(pos, cheat_pos)] = saved_picos 
    
    part2 = len([ cheat for cheat, saved_picos in cheats.items() if saved_picos >= 100 ])

    print("part 1:", part1)
    print("part 2:", part2)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
