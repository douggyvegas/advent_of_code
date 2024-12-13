import time

def main():
    part1 = 0
    part2 = 0
    directions = [(0,-1),(1,0),(0,1),(-1,0)]
    starting_pos = (0,0)
    height = 0
    width = 0
    obstacles: set[tuple[int, int]] = set()
    with open("06.in") as input:
        for row, line in enumerate(input.read().splitlines()):
            width = len(line)
            height += 1
            if '^' in line:
                starting_pos = (line.find('^'), row)
            for col, c in enumerate(line):
                if c == '#':
                    obstacles.add((col, row))

    path: list[tuple[tuple[int, int], int]] = []
    dir: int = 0
    pos = starting_pos
    path.append((pos,dir))
    while True:
        # look ahead
        next_pos = (pos[0] + directions[dir][0], pos[1] + directions[dir][1])
        
        # detect obstacle
        if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
            if next_pos in obstacles:
                dir = (dir + 1) % 4
            else:
                # move
                pos = next_pos
                path.append((pos, dir))
        else:
            break

    all_obstacle_positions = set()
    for obstacle_pos, _ in path[1:]:
        path_with_obstacle = set()
        pos = starting_pos
        dir = 0
        path.append((pos, dir))
        while True:
            # look ahead
            next_pos = (pos[0] + directions[dir][0], pos[1] + directions[dir][1])
            if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
                # detect loop
                if (next_pos, dir) in path_with_obstacle:
                    if obstacle_pos != starting_pos:
                        all_obstacle_positions.add(obstacle_pos)
                    break
                # detect obstacle
                if next_pos in obstacles or next_pos == obstacle_pos:
                    dir = (dir + 1) % 4
                else:
                    # move
                    pos = next_pos
                    path_with_obstacle.add((pos, dir))
            else:
                break

    part1 = len(set([ pos for pos, _ in path]))
    part2 = len(all_obstacle_positions)
    
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")