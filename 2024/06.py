import time

def main():
    part1 = 0
    part2 = 0
    grid: list[str] = []
    directions=[(0,-1),(1,0),(0,1),(-1,0)]
    pos=(0,0)
    dir=0
    height = 0
    width = 0
    with open("06.ex") as input:
        for row, line in enumerate(input.read().splitlines()):
            width = len(line)
            height += 1
            if '^' in line:
                pos = (line.find('^'), row)
            grid.append(line)
                
    while 0 <= pos[0] < width and 0 <= pos[1] < height:
        grid[pos[1]] = grid[pos[1]][:pos[0]] + 'X' + grid[pos[1]][pos[0] + 1:]
        # for row in grid:
        #     print(row)
        # print('----------------')
        
        next_pos = (pos[0] + directions[dir][0], pos[1] + directions[dir][1])
        if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height and grid[next_pos[1]][next_pos[0]] == '#':
            dir = (dir + 1) % 4
        else:
            pos = next_pos
    
    part1 = sum([ row.count('X') for row in grid ])
    
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")