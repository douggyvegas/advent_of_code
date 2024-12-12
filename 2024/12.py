import time

directions = [(0,-1),(1,0),(0,1),(-1,0)]

def border_detected(grid: list[str], pos: tuple[int, int], d: int, borders: dict[tuple[int, int], int], res: list[int]):
    res[1] += 1 # perimeter++
    borders[pos] |= 2 ** d
    # find potential neighbors sharing the same border
    shared: int = 0
    potential_directions = [ (d + 1) % 4, (d - 1) % 4]
    for potential_direction in potential_directions:
        border_candidate = (pos[0] + directions[potential_direction][0], pos[1] + directions[potential_direction][1])
        if 0 <= border_candidate[0] < len(grid[0]) and 0 <= border_candidate[1] < len(grid):
            if border_candidate in borders and borders[border_candidate] & (2 ** d) != 0:
                # sharing border => not new side
                shared += 1
    if shared == 0:
        res[2] += 1 # side++
    elif shared == 2:
        res[2] -= 1 # same side merge 

def solve(grid: list[str], pos: tuple[int, int], visited: set[tuple[int, int]], borders: dict[tuple[int, int], int]) -> list[int]:
    res: list[int] = [0, 0, 0]
    if pos not in visited:
        visited.add(pos)
        borders[pos] = 0
        res[0] = 1 # area = 1
        type = grid[pos[1]][pos[0]]
        for d, direction in enumerate(directions):
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if 0 <= neighbor[0] < len(grid[0]) and 0 <= neighbor[1] < len(grid):
                neighbor_type = grid[neighbor[1]][neighbor[0]]
                if neighbor_type != type:
                    border_detected(grid, pos, d, borders, res)
            else:
                border_detected(grid, pos, d, borders, res)

        for d, direction in enumerate(directions):
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if 0 <= neighbor[0] < len(grid[0]) and 0 <= neighbor[1] < len(grid):
                neighbor_type = grid[neighbor[1]][neighbor[0]]
                if neighbor_type == type:
                    neighbor_res = solve(grid, neighbor, visited, borders)
                    res[0] += neighbor_res[0]
                    res[1] += neighbor_res[1]
                    res[2] += neighbor_res[2]

    return res

def main():
    part1 = 0
    part2 = 0
    grid: list[str] = []
    with open("12.in") as input:
        grid = input.read().splitlines()

    height = len(grid)
    width = len(grid[0])

    visited: set[tuple[int, int]] = set()
    for x in range(width):
        for y in range(height):
            pos = (x,y)
            if pos not in visited:
                borders: dict[tuple[int, int], int] = {}
                res = solve(grid, pos, visited, borders)
                print(pos, grid[pos[1]][pos[0]], res)
                part1 += res[0] * res[1]
                part2 += res[0] * res[2]

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")