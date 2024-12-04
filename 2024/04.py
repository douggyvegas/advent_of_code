import time
import re

def main():
    part1 = 0
    part2 = 0
    directions = [ (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) ]
    table = []
    height = 0
    width = 0
    with open("04.in") as input:
        for line in input.read().splitlines():
            width = len(line)
            height += 1
            table.append(line)

    wordToFind = "XMAS"
    for col in range(width):
        for row in range(height):
            for dir in directions:
                found = True
                for c in range(len(wordToFind)):
                    currentCol = col + dir[0] * c
                    currentRow = row + dir[1] * c
                    if currentCol < 0 or currentCol >= width:
                        found = False
                        break
                    if currentRow < 0 or currentRow >= height:
                        found = False
                        break 
                    if table[currentRow][currentCol] != wordToFind[c]:
                        found = False
                        break
                if found:
                    part1 += 1
            
            if 0 < row < height - 1 and 0 < col < width - 1:
                if table[row][col] == "A":
                    se = table[row+directions[1][1]][col+directions[1][0]]
                    sw = table[row+directions[3][1]][col+directions[3][0]]
                    nw = table[row+directions[5][1]][col+directions[5][0]]
                    ne = table[row+directions[7][1]][col+directions[7][0]]
                    if (se == "M" and nw == "S" or se == "S" and nw == "M") and (sw == "M" and ne == "S" or sw == "S" and ne == "M"):
                        part2 += 1 
            
    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")