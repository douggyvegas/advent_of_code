from functools import reduce
import operator
import time

def main():
    part1 = 0
    part2 = 0
    
    boxes: list[list[int]] = []
    max_pairs = 1000
    with open("08.in") as input:
    # max_pairs = 10
    # with open("08.ex") as input:
        for line in input.read().splitlines():
            boxes.append([ int(n) for n in line.split(",")])

    distances: dict[tuple[int, int], int] = {}
    for i, b1 in enumerate(boxes[:-1]):
        for j in range(i + 1, len(boxes)):
            b2 = boxes[j]
            dist = sum([ (b1[c] - b2[c]) * (b1[c] - b2[c]) for c in range(0, 3) ])
            distances[(i,j)] = dist

    # print("distances =", [ (i[0][0], boxes[i[0][0]], i[0][1], boxes[i[0][1]], i[1]) for i in distances.items() ])
    sorted_boxes = [ (k,d) for k, d in sorted(distances.items(), key = lambda item: item[1] ) ]


    # print("sorted_boxes =", sorted_boxes )

    circuits: list[set[int]] = [ set([ b[0], b[1] ]) for b,_ in sorted_boxes[:max_pairs] ]
    previous_len = 0
    while previous_len != len(circuits):
        previous_len = len(circuits)
        i = 0
        while i < len(circuits) - 1:
            c1 = circuits[i]
            remaining_circuits: list[set[int]] = []
            merged_circuit: set[int] = set(c1)
            for j in range(i + 1, len(circuits)):
                c2 = circuits[j]
                if len(c1.intersection(c2)) != 0:
                    merged_circuit = merged_circuit.union(c2)
                else:
                    remaining_circuits += [ c2 ]

            circuits =  circuits[:i] + [ merged_circuit ] + remaining_circuits
            # print(i, len(circuits), previous_len, "circuits =", circuits)
            i += 1

    circuits = sorted(circuits, key=lambda c:len(c), reverse=True)
    part1 = reduce(operator.mul, [ len(c) for c in circuits[:3]], 1)
    print('part 1:', part1)

    pairs: list[set[int]] = [ set([ b[0], b[1] ]) for b, _ in sorted_boxes ]
    circuits: list[set[int]] = []
    for pair in pairs:
        found = False
        for c1, circuit in enumerate(circuits):
            if pair.intersection(circuit):
                circuit.update(pair)
                found = True
                while c1 < len(circuits) - 1:
                    c2 = c1 + 1
                    while c2 < len(circuits):
                        if circuits[c1].intersection(circuits[c2]):
                            circuits[c1].update(circuits[c2])
                            circuits.pop(c2)
                            c1 = len(circuits)
                            c2 = len(circuits)
                        else:
                            c2 += 1
                    c1 += 1
                if len(circuits) == 1 and len(circuits[0]) == len(boxes):
                    b1 = pair.pop()
                    b2 = pair.pop()
                    part2 = boxes[b1][0] * boxes[b2][0]
                    break

        if not found:
            circuits.append(pair)

        if part2 != 0:
            break
    
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")