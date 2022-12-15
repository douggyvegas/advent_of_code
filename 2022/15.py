#!/usr/bin/env python3

import math
import time
import re

def manhattanDistance(a, b):
    d = abs(b[0] - a[0]) + abs(b[1] - a[1])
    return d

def merge(intervals):
    if len(intervals) == 0 or len(intervals) == 1:
        return intervals
    intervals.sort(key=lambda x:x[0])
    result = [intervals[0]]
    for interval in intervals[1:]:
        if interval[0] <= result[-1][1]:
            result[-1][1] = max(result[-1][1], interval[1])
        else:
            result.append(interval)
    return result

def split(interval, x):
    interval = sorted(interval)
    if interval[0] == x:
        interval = [ [ interval[0] + 1, interval[1] ] ]
    elif interval[1] == x:
        interval = [ [ interval[0], interval[1] - 1 ] ]
    elif interval[0] < x < interval[1]:
        interval = [ [ interval[0], x - 1 ], [ x + 1, interval[1] ] ]
    return interval

def getCellsInBeaconRange(y, sensor_to_beacon, min_x, max_x):
    cells_in_beacon_range = [ ]
    for sensor, beacon in sensor_to_beacon.items():
        dx = manhattanDistance(sensor, beacon) - abs(y - sensor[1])
        if dx > 0:
            r = [ max(sensor[0] - dx, min_x), min(sensor[0] + dx, max_x) ]
            if beacon[1] == y or sensor[1] == y:
                if beacon[1] == y:
                    cells_in_beacon_range += split(r, beacon[0])
                if sensor[1] == y:
                    cells_in_beacon_range += split(r, sensor[0])
            else:
                cells_in_beacon_range += [ r ]

    cells_in_beacon_range = merge(cells_in_beacon_range)
    return cells_in_beacon_range

def main():
    sensor_to_beacon = { }
    with open('15.in') as input:
        for line in input.read().splitlines():
            match = re.match("Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)", line)
            sensor = ( int(match.group(1)), int(match.group(2)) )
            beacon = ( int(match.group(3)), int(match.group(4)) )
            sensor_to_beacon[sensor] = beacon

    print("part1 =", sum(r[1] - r[0] + 1 for r in getCellsInBeaconRange(2000000, sensor_to_beacon, -math.inf, math.inf)))

    max_y = 4000000
    found = [ ]
    for y in range(max_y, 0, -1):
        cells_in_beacon_range = getCellsInBeaconRange(y, sensor_to_beacon, 0, max_y)
        for sensor, beacon in sensor_to_beacon.items():
            if sensor[1] == y:
                cells_in_beacon_range += [ [ sensor[0], sensor[0] ] ]
            if beacon[1] == y:
                cells_in_beacon_range += [ [ beacon[0], beacon[0] ] ]
        cells_in_beacon_range = sorted(cells_in_beacon_range)
        count = max_y + 1 - sum(r[1] - r[0] + 1 for r in cells_in_beacon_range)
        if y % 100000 == 0:
            print((max_y - y) / max_y * 100, "%")
        if count == 1:
            print("FOUND IT")
            previous_x = -1
            for i in cells_in_beacon_range:
                if i[0] - previous_x == 2:
                    print(previous_x + 1)
                    found = [previous_x + 1, y]
                    break
                previous_x = i[1]

            if len(found) != 0:
                break

    print("part2 =", found[0] * max_y + found[1])

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")