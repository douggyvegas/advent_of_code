from itertools import combinations
import time

from matplotlib import patches, pyplot as plt
from matplotlib.collections import LineCollection

def main():
    part1 = 0
    part2 = 0
    with open("09.in") as input:
        tiles:list[list[int]] = [list(map(int, line.split(','))) for line in input.read().splitlines() ]

    max_area = 0
    for tile1, tile2 in combinations(tiles, 2):
        area = (abs(tile2[0] - tile1[0]) + 1) * (abs(tile2[1] - tile1[1]) + 1)
        if area > max_area:
            max_area = area

    part1 = max_area
    print('part 1:', part1)

    edges:list[tuple[list[int], list[int]]] = list(zip(tiles, tiles[1:] + tiles[:1]))
    special = [ ((min(x1, x2), y1), (max(x1, x2), y2)) for (x1, y1), (x2, y2) in edges if abs(x1 - x2) > 10000 ]

    max_area = 0
    corners: list[tuple[int, int]] = []
    bottom, top = sorted(special, key=lambda s: s[0][1])
    for corner, direction in (bottom, -1), (top, 1):
        x1, y = corner[0]
        x2 = corner[1][0]
        y_max = 0
        for (edge_x1, edge_y1), (edge_x2, edge_y2) in edges:
            if edge_y1 == edge_y2:
                min_edge_x, max_edge_x = (min(edge_x1, edge_x2), max(edge_x1, edge_x2))
                if min_edge_x <= x2 <= max_edge_x and (edge_y1 - y) * direction > 0:
                    y_max = edge_y1
                    break
        
        for tx, ty in tiles:
            if tx < x1 or tx > x2 or ty < min(y, y_max) or ty > max(y, y_max):
                continue
            if any(edge_y1 == edge_y2 and 
                min(y, ty) < edge_y1 < max(y, ty) and 
                min(edge_x1, edge_x2) < x2 and max(edge_x1, edge_x2) > tx 
                for (edge_x1, edge_y1), (edge_x2, edge_y2) in edges):
                continue
        
            area = (x2 - tx + 1) * (abs(y - ty) + 1)
            if area > max_area:
                max_area = area
                corners = [ (x2, y), (tx, ty) ]

    part2 = max_area
    print('part 2:', part2)

    # ------------------------------------------------------------------
    # 4️⃣  Compute rectangle bounds
    # ------------------------------------------------------------------
    xmin = min(corners[0][0], corners[1][0])
    ymin = min(corners[0][1], corners[1][1])
    xmax = max(corners[0][0], corners[1][0])
    ymax = max(corners[0][1], corners[1][1])

    width  = xmax - xmin
    height = ymax - ymin

    _, ax = plt.subplots(figsize=(8, 6))
    x,y = zip(*tiles)
    ax.scatter(x,y, s=1, linewidth=0.5, zorder=2)
    rect = patches.Rectangle((xmin, ymin), width, height,
                            linewidth=0.5, edgecolor='red', facecolor='red', linestyle='--')
    ax.add_patch(rect)
    ax.autoscale()
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, linestyle=':', alpha=0.4)
    output_file = 'polygon_with_rectangle.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {output_file}")

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")