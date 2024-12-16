import time
import re

directions: dict[str, tuple[int, int]] = {
    "v": (0, 1),
    ">": (1, 0),
    "^": (0, -1),
    "<": (-1, 0),
}

def printGrid(boxes, walls, pos, width, height):
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) == pos:
                line += "@"
            elif (x, y) in [(col, row) for (r, row) in boxes for col in r]:
                line += "O"
            elif (x, y) in [(col, row) for (r, row) in walls for col in r]:
                line += "#"
            else:
                line += "."
        print(line)

def intersect(a: tuple[range, int], b: tuple[range, int]):
    return (
        a[1] == b[1]
        and (a[0].start <= b[0].start < a[0].stop
        or b[0].start <= a[0].start < b[0].stop)
    )
    
def contains(pos: tuple[int, int], element: tuple[range, int]) -> bool:
    return intersect((range(pos[0], pos[0] + 1), pos[1]), element)

def findElement(pos: tuple[int, int], elements: set[tuple[range, int]]) -> tuple[range, int] | None:
    for e in elements:
        if contains(pos, e):
            return e
    return None

def findOverlappingBoxes(box: tuple[range, int], boxes: set[tuple[range, int]]) -> set[tuple[range, int]]:
    res: set[tuple[range, int]] = set()
    for b in boxes:
        if intersect(box, b):
            res.add(b)
    return res

def push(box: tuple[range, int], direction: tuple[int, int], boxes: set[tuple[range, int]], walls: set[tuple[range, int]]) -> set[tuple[range, int]]:
    next_box = (
        range(
            box[0].start + direction[0],
            box[0].start + direction[0] + (box[0].stop - box[0].start),
        ),
        box[1] + direction[1],
    )
    if not any([ intersect(next_box, wall) for wall in walls ]):
        boxes.remove(box)
        overlapping_boxes = findOverlappingBoxes(next_box, boxes)
        if len(overlapping_boxes) > 0:
            maybe_boxes = boxes.copy()
            for overlapping_box in overlapping_boxes:
                maybe_boxes = push(overlapping_box, direction, maybe_boxes, walls)
            if not any([ intersect(next_box, box) for box in maybe_boxes ]):
                boxes = maybe_boxes
                boxes.add(next_box)
            else:
                boxes.add(box)
        else:
            boxes.add(next_box)

    return boxes

def solve(commands: str, start_pos: tuple[int, int], boxes: set[tuple[range, int]], walls: set[tuple[range, int]], width: int, height: int) -> int:
    pos = start_pos
    #printGrid(boxes, walls, pos, width, height)
    for command in commands:
        #print(command)
        direction = directions[command]
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if not any([ contains(next_pos, wall) for wall in walls ]):
            box = findElement(next_pos, boxes)
            if box != None:
                boxes = push(box, direction, boxes, walls)
            
            if not any([ contains(next_pos, box) for box in boxes ]):
                pos = next_pos
        #printGrid(boxes, walls, pos, width, height)
                
    return sum([100 * row + col.start for (col, row) in boxes])


def main():
    part1 = 0
    part2 = 0

    boxes1: set[tuple[range, int]] = set()
    walls1: set[tuple[range, int]] = set()

    boxes2: set[tuple[range, int]] = set()
    walls2: set[tuple[range, int]] = set()

    commands: str = ""
    width = 0
    height = 0
    start_pos1: tuple[int, int]
    start_pos2: tuple[int, int]
    with open("15.in") as input:
        map: bool = True
        lines = input.read().splitlines()
        width = len(lines[0])
        for row, line in enumerate(lines):
            if map:
                if not len(line) == 0:
                    boxes1 |= set(
                        [
                            (range(col, col + 1), row)
                            for col, c in enumerate(line)
                            if c == "O"
                        ]
                    )
                    boxes2 |= set(
                        [
                            (range(col * 2, col * 2 + 2), row)
                            for col, c in enumerate(line)
                            if c == "O"
                        ]
                    )
                    walls1 |= set(
                        [(range(col, col + 1), row) for col, c in enumerate(line) if c == "#"]
                    )
                    walls2 |= set(
                        [(range(col * 2, col * 2 + 2), row) for col, c in enumerate(line) if c == "#"]
                    )
                    if "@" in line:
                        start_pos1 = (line.find("@"), row)
                        start_pos2 = (line.find("@") * 2, row)
                else:
                    height = row
                    map = False
            else:
                commands += line

    part1 = solve(commands, start_pos1, boxes1, walls1, width, height)
    print("part 1:", part1)
    
    part2 = solve(commands, start_pos2, boxes2, walls2, width * 2, height)
    print("part 2:", part2)


start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")
