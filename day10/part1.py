#!/bin/env python
import pathlib


class Map:
    def __init__(self, lines):
        self.map = []
        self.possible_trailheads = set()
        for y, line in enumerate(lines):
            self.map.append([])
            for x, z in enumerate(line.strip()):
                z = int(z)
                self.map[-1].append(z)
                if z == 0:
                    self.possible_trailheads.add((x, y))
        self.height = len(self.map)
        self.width = len(self.map[0])
        # TODO: filter alts without possible path neighbours?

    def calculate_score(self):
        score = 0
        for x, y in self.possible_trailheads:
            score += len(self.find_trail_ends(x, y))
        return score

    def find_trail_ends(self, x, y):
        z = self.map[y][x]
        if z == 9:
            return {(x, y)}
        trail_ends = set()
        if x > 0 and self.map[y][x - 1] == z + 1:
            trail_ends |= self.find_trail_ends(x - 1, y)
        if x < self.width - 1 and self.map[y][x + 1] == z + 1:
            trail_ends |= self.find_trail_ends(x + 1, y)
        if y > 0 and self.map[y - 1][x] == z + 1:
            trail_ends |= self.find_trail_ends(x, y - 1)
        if y < self.height - 1 and self.map[y + 1][x] == z + 1:
            trail_ends |= self.find_trail_ends(x, y + 1)
        return trail_ends

    def __str__(self):
        return (
            "\n".join(["".join([str(mp) for mp in line]) for line in self.map])
            + "\n"
            + repr(self.possible_trailheads)
        )


def parse_lines(lines):
    for line in lines:
        pass
    return map


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        map = Map(file.readlines())
    print(map)
    print(map.calculate_score())


if __name__ == "__main__":
    main()
