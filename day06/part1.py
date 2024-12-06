#!/bin/env python
import pathlib


class Guard:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


class MapState:
    def __init__(self, lines):
        self.map = []
        self.guard = None
        self.visited_map = []
        for y, line in enumerate(lines):
            map_line = []
            visited_map_line = []
            for x, ch in enumerate(line.strip()):
                match ch:
                    case ".":
                        map_line.append(False)
                        visited_map_line.append(False)
                    case "#":
                        map_line.append(True)
                        visited_map_line.append(False)
                    case "^" | ">" | "v" | "<":
                        if self.guard:
                            raise ValueError("more than one guard on map")
                        map_line.append(False)
                        visited_map_line.append(True)
                        self.guard = Guard((x, y), ch)
                    case "X":
                        # This should never occur in the input map.
                        map_line.append(False)
                        visited_map_line.append(True)
                    case _:
                        raise ValueError(f"unknown character on map: {ch}")
            self.map.append(map_line)
            self.visited_map.append(visited_map_line)

    def __repr__(self):
        result = ""
        for y, line in enumerate(self.map):
            for x, has_obstacle in enumerate(line):
                if (x, y) == self.guard.position:
                    result += self.guard.direction
                elif has_obstacle:
                    result += "#"
                elif self.visited_map[y][x]:
                    result += "X"
                else:
                    result += "."
            result += "\n"
        return result

    def count_visited(self):
        return sum(line.count(True) for line in self.visited_map)

    def step(self):
        x, y = self.guard.position
        match self.guard.direction:
            case "^":
                if y == 0:
                    return False
                if self.map[y - 1][x]:
                    self.guard.direction = ">"
                else:
                    y -= 1
            case ">":
                if x == len(self.map[y]) - 1:
                    return False
                if self.map[y][x + 1]:
                    self.guard.direction = "v"
                else:
                    x += 1
            case "v":
                if y == len(self.map) - 1:
                    return False
                if self.map[y + 1][x]:
                    self.guard.direction = "<"
                else:
                    y += 1
            case "<":
                if x == 0:
                    return False
                if self.map[y][x - 1]:
                    self.guard.direction = "^"
                else:
                    x -= 1
        self.visited_map[y][x] = True
        self.guard.position = (x, y)
        return True


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        map_state = MapState(file.readlines())
        if map_state.guard is None:
            raise ValueError("no guard on map")
        print(map_state)
        while map_state.step():
            pass
        print(map_state)
    print(map_state.count_visited())


if __name__ == "__main__":
    main()
