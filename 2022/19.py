#!/usr/bin/env python3

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import islice
import math
import logging
import operator
import time

RESOURCES = [ "ore", "clay", "obsidian", "geode" ]

@dataclass
class State:
    elapsed: int
    collected: list[int]
    robots: list[int]

def main():

    logging.basicConfig(level=logging.INFO)

    with open('19.in') as input:
        blueprints = { }
        for line in input.read().splitlines():
            words = line.replace(":", "").replace(".", "").replace("\w", "").split(" ")
            id = int(words[1])
            blueprints[id] = [ [ ] ] * 4
            blueprints[id][0] = [ 0 ] * 4
            blueprints[id][0][0] = int(words[6])
            blueprints[id][1] = [ 0 ] * 4
            blueprints[id][1][0] = int(words[12])
            blueprints[id][2] = [ 0 ] * 4
            blueprints[id][2][0] = int(words[18])
            blueprints[id][2][1] = int(words[21])
            blueprints[id][3] = [ 0 ] * 4
            blueprints[id][3][0] = int(words[27])
            blueprints[id][3][2] = int(words[30])

    print("part 1:", sum([ g * (i + 1) for i,g in enumerate(crackGeodes(blueprints, 24)) ] ))
    print("part 2:", reduce(operator.mul, [ g for g in crackGeodes(dict(islice(blueprints.items(), 3)), 32) ] ))


def crackGeodes(blueprints, max_time):
    
    all_max_geodes = [ 0 ] * len(blueprints.keys())
    
    for id, costs in blueprints.items():
        max_geodes = 0

        q = deque()
        q.append(State(0, [ 0, 0, 0, 0 ], [ 1, 0, 0, 0 ]))

        max_required_robots = [ max([ cost[robot] for cost in costs ]) for robot in range(4) ]
        max_required_robots[3] = math.inf

        while len(q) != 0:
            state = q.pop()

            for next_robot in range(4):
                if state.robots[next_robot] >= max_required_robots[next_robot]:
                    continue

                required_times = [ -math.inf ] * 4
                cost = costs[next_robot]
                
                for resource in range(4):
                    if cost[resource] != 0:
                        if cost[resource] <= state.collected[resource]:
                            required_times[resource] = 0
                        elif state.robots[resource] == 0:
                            required_times[resource] = math.inf
                        else:
                            required_times[resource] = (cost[resource] - state.collected[resource] - 1) // state.robots[resource] + 1
                    else:
                        required_times[resource] = -math.inf

                waiting_time = max(required_times)

                new_elapsed = state.elapsed + waiting_time + 1
                if new_elapsed >= max_time:
                    continue
                
                new_collected = [ state.collected[resource] + state.robots[resource] * (waiting_time + 1) - cost[resource] for resource in range(4) ]
                new_robots = deepcopy(state.robots)
                new_robots[next_robot] += 1

                # no need to continue if we can't beat max_geodes even if we built new geodes robots every turn
                if max_geodes > new_collected[3] + sum([ r for r in range(state.robots[3], state.robots[3] + (max_time - state.elapsed)) ]):
                    continue

                new_state = State(new_elapsed, new_collected, new_robots)
                q.append((new_state))

            geodes = state.collected[3] + state.robots[3] * (max_time - state.elapsed)
            # logging.info("%s %s %s geodes", id, state, geodes)
            max_geodes = max(max_geodes, geodes)

        logging.info("blueprint %s: %s max geodes", id, max_geodes)
        all_max_geodes[id - 1] = max_geodes

    return all_max_geodes

start_time = time.time_ns()
main()
logging.error(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")