import time

directions = [(0,-1),(1,0),(0,1),(-1,0)]

def getTrailHeadScore(grid: list[list[int]], grid_height: int, grid_width: int, row: int, col: int, summits: set[tuple[int, int]]) -> int:
    
    current_height = grid[row][col]
    if current_height == 9 and (row, col) not in summits:
        summits.add((row, col))
        return 1
        
    score = 0
    for d in directions:
        next_col = col + d[0]
        next_row = row + d[1]
        if 0 <= next_col < grid_width and 0 <= next_row < grid_height:
            if grid[next_row][next_col] == current_height + 1:
                score += getTrailHeadScore(grid, grid_height, grid_width, next_row, next_col, summits)
                
    return score

def getTrailHeadScore2(grid: list[list[int]], grid_height: int, grid_width: int, row: int, col: int) -> int:
    
    current_height = grid[row][col]
    if current_height == 9:
        return 1
        
    score = 0
    for d in directions:
        next_col = col + d[0]
        next_row = row + d[1]
        if 0 <= next_col < grid_width and 0 <= next_row < grid_height:
            if grid[next_row][next_col] == current_height + 1:
                score += getTrailHeadScore2(grid, grid_height, grid_width, next_row, next_col)
                
    return score

def main():
    part1 = 0
    part2 = 0
    grid: list[list[int]] = []
    grid_width = 0
    grid_height = 0
    with open("10.in") as input:
        for line in input.read().splitlines():
            grid.append([ int(c) for c in line ])
            grid_width = len(line)
            grid_height += 1
    
    print(grid)
    
    for row, line in enumerate(grid):
        for col, height in enumerate(line):
            if height == 0:
                summits = set()
                part1 += getTrailHeadScore(grid, grid_height, grid_width, row, col, summits)
                part2 += getTrailHeadScore2(grid, grid_height, grid_width, row, col)

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")