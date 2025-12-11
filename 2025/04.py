import time

def main():
    part1 = 0
    part2 = 0
    with open("04.in") as input:
        directions: list[list[int]] = [ [ 1, 0 ], [ 1, 1], [ 0, 1 ], [ -1, 1], [ -1, 0], [ -1, -1 ], [ 0, -1 ], [ 1, -1 ] ]
        grid: list[str] = input.read().splitlines()

        count: dict[tuple[int, int], int] = {}
        while part1 == 0 or len([ c for c in count.values() if c < 4 ]) > 0:
            
            for pos in [ p for p,v in count.items() if v < 4]:
                grid[pos[0]] = grid[pos[0]][:pos[1]] + '.' + grid[pos[0]][pos[1] + 1:]
            
            count.clear()

            for row, line in enumerate(grid):
                for col, c in enumerate(line):   
                    if c == '@':
                        nb_rolls = 0
                        for _, dir in enumerate(directions):
                            n_row = row + dir[0]
                            n_col = col + dir[1]
                            if n_row >= 0 and n_row < len(grid) and n_col >= 0 and n_col < len(grid[0]) and grid[n_row][n_col] == '@':
                                nb_rolls += 1
                        count[(row, col)] = nb_rolls

            if part1 == 0:
                part1 = len([ x for x in count.values() if x < 4 ])

            part2 += len([ x for x in count.values() if x < 4 ])

        for line in grid:
            print(line)

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")