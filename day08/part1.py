#!/bin/env python
import collections
import pathlib
import itertools


class Map:
    def __init__(self, lines):
        self.map = []
        self.antennas = collections.defaultdict(set)
        for y, line in enumerate(lines):
            map_line = []
            for x, ch in enumerate(line.strip()):
                if ch != ".":
                    map_line.append(MapPoint(ch))
                    self.antennas[ch].add((x, y))
                else:
                    map_line.append(MapPoint())
            self.map.append(map_line)
        self.height = len(self.map)
        self.width = len(self.map[0]) if self.height > 0 else None

    def __str__(self):
        return (
            "\n".join(["".join([str(mp) for mp in line]) for line in self.map])
            + "\n"
            + repr(dict(self.antennas))
        )

    def calculate_antinodes(self):
        for antenna, positions in self.antennas.items():
            print(antenna, positions)
            for pair in itertools.combinations(positions, 2):
                x1 = pair[0][0]
                y1 = pair[0][1]
                x2 = pair[1][0]
                y2 = pair[1][1]
                dx = x1 - x2
                dy = y1 - y2
                antinodes = [(x1 + dx, y1 + dy), (x2 - dx, y2 - dy)]
                for antinode in antinodes:
                    x, y = antinode
                    if (0 <= x < self.width) and (0 <= y < self.height):
                        self.map[y][x].antinode = True

    def count_antinodes(self):
        return sum([sum([1 if p.antinode else 0 for p in line]) for line in self.map])


class MapPoint:
    def __init__(self, antenna=None, antinode=False):
        self.antenna = antenna
        self.antinode = antinode

    def __str__(self):
        return (self.antenna if self.antenna is not None else ".") + (
            "#" if self.antinode else " "
        )


def parse_map(lines):
    return Map(lines)


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        map = parse_map(file.readlines())
    print(map)
    map.calculate_antinodes()
    print(map)
    print(map.count_antinodes())


if __name__ == "__main__":
    main()
