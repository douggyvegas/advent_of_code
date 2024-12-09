import time

def main():
    part1 = 0
    part2 = 0
    with open("09.in") as input:
        for line in input.read().splitlines():
            compacted_line_1: list[int] = []
            blocks = [ int(c) for c in line ]
            file_blocks = [ b for i, b in enumerate(blocks) if i % 2 == 0 ]
            free_blocks = [ b for i, b in enumerate(blocks) if i % 2 == 1 ]
            ids = [ i for i in range(len(file_blocks)) ]
            current_block = 0
            while len(ids) > 0:
                if current_block % 2 == 1:
                    # free space
                    free_space = free_blocks.pop(0)
                    while free_space != 0 and len(file_blocks) > 0:
                        blocks_to_compact = file_blocks.pop()
                        id = ids.pop()
                        moved_blocks = min(blocks_to_compact, free_space)
                        blocks_to_compact -= moved_blocks
                        free_space -= moved_blocks
                        compacted_line_1 += [id] * moved_blocks
                        if blocks_to_compact != 0:
                            ids += [id]
                            file_blocks += [blocks_to_compact]
                else:
                    # file block
                    if len(file_blocks) > 0:
                        id = ids.pop(0)
                        blocks_to_compact = file_blocks.pop(0)
                        compacted_line_1 += [id] * blocks_to_compact
                
                current_block += 1

            part1 = sum([ i * id for i,id in enumerate(compacted_line_1) ])

            files: dict[int, range] = {}
            free: list[range] = []
            offset = 0
            id = 0
            for i in range(len(blocks)):
                slot = range(offset, offset + blocks[i])
                if i % 2 == 0:
                    # file block
                    files[id] = slot
                    id += 1
                else:
                    # free block
                    free.append(slot)
                offset += blocks[i]

            for id in sorted(files.keys(), reverse=True):
                file = files[id]
                size = len(file)
                free_index = next((i for i, r in enumerate(free) if len(r) >= size and r.start < file.start), None)
                if free_index is not None:
                    # found a big enough free slot
                    slot = free[free_index]
                    files[id] = range(slot.start, slot.start + size)
                    free[free_index] = range(slot.start + size, slot.stop)

            for id, file in files.items():
                for offset in file:
                    part2 += offset * id

    print('part 1:', part1)
    print('part 2:', part2)

start_time = time.time_ns()
main()
print(f"Duration: {(time.time_ns() - start_time) / 10 ** 9} s")