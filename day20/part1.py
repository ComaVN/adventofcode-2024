#!/bin/env python
import collections
import pathlib


class TrackPart:
    def __init__(self):
        self.distance = None


class Map:
    def __init__(self, lines):
        self.start = None
        self.end = None
        self.track = {}
        for y, line in enumerate(lines):
            for x, ch in enumerate(line.strip()):
                match ch:
                    case "#":
                        pass
                    case ".":
                        self.track[(x, y)] = TrackPart()
                    case "S":
                        self.track[(x, y)] = TrackPart()
                        self.start = (x, y)
                    case "E":
                        self.track[(x, y)] = TrackPart()
                        self.end = (x, y)
                    case _:
                        raise ValueError(f"character '{ch}' in map not supported")
            self.width = x + 1
        self.height = y + 1
        if self.start is None:
            raise ValueError("map must have a start position")
        if self.end is None:
            raise ValueError("map must have an end position")

    def __str__(self):
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                if self.start == pos:
                    ch = "S"
                elif self.end == pos:
                    ch = "E"
                elif pos in self.track:
                    ch = "."
                else:
                    ch = "#"
                result += ch
            result += "\n"
        return result

    def measure(self):
        assert self.start != self.end
        measured = set()
        pos = self.start
        distance = 0
        while True:
            self.track[pos].distance = distance
            measured.add(pos)
            distance += 1
            x, y = pos
            next_pos_set = {
                (x - 1, y),
                (x, y - 1),
                (x + 1, y),
                (x, y + 1),
            } & self.track.keys() - measured
            if pos == self.end:
                if len(next_pos_set) > 0:
                    raise ValueError("track continues after end")
                break
            if len(next_pos_set) == 0:
                if pos == self.end:
                    break
                raise ValueError("map does not have a connected track")
            if len(next_pos_set) > 1:
                raise ValueError("map does not have a unambiguous track")
            pos = next(iter(next_pos_set))
        return self.track[self.end].distance

    def find_cheats(self):
        cheats = []
        for pos, part in self.track.items():
            x, y = pos
            possible_cheats = [
                ((x - 1, y), (x - 2, y)),  # left, left
                ((x - 1, y), (x - 1, y - 1)),  # left, up
                ((x - 1, y), (x - 1, y + 1)),  # left, down
                ((x + 1, y), (x + 2, y)),  # right, right
                ((x + 1, y), (x + 1, y - 1)),  # right, up
                ((x + 1, y), (x + 1, y + 1)),  # right, down
                ((x, y - 1), (x, y - 2)),  # up, up
                ((x, y - 1), (x - 1, y - 1)),  # up, left
                ((x, y - 1), (x + 1, y - 1)),  # up, right
                ((x, y + 1), (x, y + 2)),  # down, down
                ((x, y + 1), (x - 1, y + 1)),  # down, left
                ((x, y + 1), (x + 1, y + 1)),  # down, right
            ]
            for cheat in (c for c in possible_cheats if c[1] in self.track):
                improvement = self.track[cheat[1]].distance - part.distance - 2
                if improvement > 0:
                    print(f"from {pos}: {cheat} ({improvement})")
                    cheats.append((cheat, improvement))
        return cheats


def main():
    for filename in (
        "input.example.txt",
        "input.txt",
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            m = Map(file)
        print(m)
        distance = m.measure()
        print(distance)
        aggr = 0
        cheats_by_improvement = collections.defaultdict(int)
        for cheat, improvement in m.find_cheats():
            print(f"{cheat}: {improvement}")
            cheats_by_improvement[improvement] += 1
            if improvement >= 100:
                aggr += 1
        print(cheats_by_improvement)
        print(aggr)


if __name__ == "__main__":
    main()
