import time
import re

# N,E,S,W
directions = [ (-1,0), (0,1), (1,0), (0,-1) ]
pipes = { '|': (0,2), '-': (1,3), 'L': (0,1), 'J': (0,3), '7': (2,3), 'F': (1,2) }

def main():
    with open("10.in") as input:
        map = [ ]
        for line in input.read().splitlines():
            map += [ line ]

    # find starting point of loop (could be simpler...)
    start = (-1,-1)
    start_pipe_exit = 0
    loop_start = (-1,-1)
    for row, line in enumerate(map):
        col = line.find('S')
        if col != -1:
            start = (row, col) 
            for n in range(4):
                next_cell = (start[0] + directions[n][0], start[1] + directions[n][1])
                if 0 <= next_cell[0] < len(map) and 0 <= next_cell[1] < len(line):
                    pipe = map[next_cell[0]][next_cell[1]]
                    if pipe in pipes.keys():
                        next_direction = pipes[pipe]
                        for pipe_exit in range(2):
                            if next_cell[0] + directions[next_direction[pipe_exit]][0] == start[0] and next_cell[1] + directions[next_direction[pipe_exit]][1] == start[1]:
                                loop_start = next_cell
                                start_pipe_exit = pipe_exit
                                break
                    else:
                        continue
                    break
            else:
                continue
            break

    # walk through the loop
    last_pipe_exit = 0
    length = 1
    loop = [ start ]
    current_cell = loop_start
    while current_cell != start:
        pipe = map[current_cell[0]][current_cell[1]]
        if pipe in pipes.keys():
            next_direction = pipes[pipe]
            for pipe_exit in range(2):
                if current_cell[0] + directions[next_direction[pipe_exit]][0] == loop[-1][0] and current_cell[1] + directions[next_direction[pipe_exit]][1] == loop[-1][1]:
                    next_cell = (current_cell[0] + directions[next_direction[1-pipe_exit]][0], current_cell[1] + directions[next_direction[1-pipe_exit]][1])
                    if 0 <= next_cell[0] < len(map) and 0 <= next_cell[1] < len(map[0]):
                        length += 1
                        loop.append(current_cell)
                        current_cell = next_cell
                        last_pipe_exit = pipe_exit
                    else:
                        next_cell = current_cell
    
    # convert starting point to pipe
    start_pipe = [ k for k,v in pipes.items() if v == (start_pipe_exit, last_pipe_exit) or v == (last_pipe_exit, start_pipe_exit) ][0]
    
    # create map with just the loop
    map_loop = [ ]
    for i, row in enumerate(map):
        p = ""
        for j, c in enumerate(row):
            if (c == 'S'):
                p += start_pipe
            elif (i,j) in loop:
                p += c
            else:
                p += '.'
        map_loop += [ p ]
    
    # a cell is inside the loop if the horizontal line starting at cell column intersects with top-bottom walls a odd number of times
    inside = 0
    inside_cells = [ ]
    for i, row in enumerate(map_loop):
        walls = [ m.start() for m in re.finditer(r"L-*7|F-*J|\|", row) ]
        for empty_col in [ m.start() for m in re.finditer(r"\.", row) ]:
            is_inside = (len([ w for w in walls if w > empty_col ]) % 2 == 1)
            if is_inside:
                inside += 1
                inside_cells += [ (i, empty_col) ]

    # draw the map
    for i, row in enumerate(map_loop):
        p = ""
        for j, c in enumerate(row):
            if (i,j) in inside_cells:
                p += 'I'
            else:
                p += c
        print(p)

    print(f"part 1: {length//2}")
    print(f"part 2: {inside}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")