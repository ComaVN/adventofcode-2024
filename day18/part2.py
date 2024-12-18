#!/bin/env python
import heapq
import pathlib


class Cell:
    def __init__(self, *, accessible=True):
        self.accessible = accessible
        self.part_of_final_path = False


class Map:
    def __init__(self, size):
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        self.height = self.width = size
        self.map = [[Cell() for _ in range(size)] for _ in range(size)]

    def drop_byte(self, line):
        x, y = [int(v.strip()) for v in line.split(",", 1)]
        self.map[y][x].accessible = False
        return (x, y)

    def __str__(self):
        result = ""
        for y, line in enumerate(self.map):
            for x, ch in enumerate(line):
                cell = self.map[y][x]
                if not cell.accessible:
                    ch = "#"
                elif self.start == (x, y):
                    ch = "S"
                elif self.end == (x, y):
                    ch = "E"
                elif cell.part_of_final_path:
                    ch = "O"
                else:
                    ch = "."
                result += ch
            result += "\n"
        return result

    def solve(self):
        to_do_heap = [
            (
                0,
                self.start,
                [],
            )
        ]
        heapq.heapify(to_do_heap)
        touched_positions = {self.start}
        final_steps = None
        final_path = None
        while len(to_do_heap) > 0:
            # print(self)
            steps, (x, y), path = heapq.heappop(to_do_heap)
            if (x, y) == self.end:
                assert final_path is None
                final_path = path
                break
            cell = self.map[y][x]
            if not cell.accessible:
                continue
            new_heap_positions = []
            if x > 0:
                # try going left
                new_heap_positions.append((x - 1, y))
            if x < self.width - 1:
                # try going right
                new_heap_positions.append((x + 1, y))
            if y > 0:
                # try going up
                new_heap_positions.append((x, y - 1))
            if y < self.height - 1:
                # try going down
                new_heap_positions.append((x, y + 1))
            for new_heap_pos in new_heap_positions:
                if new_heap_pos not in touched_positions:
                    heapq.heappush(
                        to_do_heap,
                        (
                            steps + 1,
                            new_heap_pos,
                            path + [(x, y)],
                        ),
                    )
                    touched_positions.add(new_heap_pos)
        if final_path:
            for pos in final_path:
                self.map[pos[1]][pos[0]].part_of_final_path = True
            return True
        return False


def main():
    for filename, map_size, nr in (
        ("input.example.txt", 7, 12),
        ("input.txt", 71, 1024),
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            m = Map(map_size)
            print(m)
            for line in file:
                pos = m.drop_byte(line)
                if not m.solve():
                    print(m)
                    print(pos)
                    break


if __name__ == "__main__":
    main()
