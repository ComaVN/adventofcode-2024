#!/bin/env python
import copy
import pathlib


class LoopFound(RuntimeError):
    pass


class Guard:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


class MapState:
    def __init__(self, *, line_iterator=None, map_and_guard=None):
        self.steps = 0
        if map_and_guard:
            map = map_and_guard[0]
            guard = map_and_guard[1]
            self.map = copy.deepcopy(map)
            self.guard = Guard(guard.position, guard.direction)
            self.visited_map = [[False for _ in line] for line in self.map]
        elif line_iterator:
            self.map = []
            self.guard = None
            self.visited_map = []
            for y, line in enumerate(line_iterator):
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
                            # Note that this must now be false, because we now don't care about the visited places, rather the places where we could place an extra obstacle:
                            visited_map_line.append(False)
                            self.guard = Guard((x, y), ch)
                        case "X":
                            # This should never occur in the input map.
                            map_line.append(False)
                            visited_map_line.append(True)
                        case _:
                            raise ValueError(f"unknown character on map: {ch}")
                self.map.append(map_line)
                self.visited_map.append(visited_map_line)
        else:
            raise ValueError("missing map source")
        self.height = len(self.map)
        self.width = len(self.map[0])

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

    def potential_new_obstacles(self):
        for y, line in enumerate(self.visited_map):
            for x, visited in enumerate(line):
                if visited:
                    yield (x, y)

    def step(self):
        self.steps += 1
        if self.steps > self.height * self.width * 4 * 2:
            # Crude estimate of an upper bound for the number of steps...
            raise LoopFound()
        x, y = self.guard.position
        match self.guard.direction:
            case "^":
                if y == 0:
                    return False
                if self.map[y - 1][x]:
                    self.guard.direction = ">"
                else:
                    y -= 1
                    self.move(x, y)
            case ">":
                if x == self.width - 1:
                    return False
                if self.map[y][x + 1]:
                    self.guard.direction = "v"
                else:
                    x += 1
                    self.move(x, y)
            case "v":
                if y == self.height - 1:
                    return False
                if self.map[y + 1][x]:
                    self.guard.direction = "<"
                else:
                    y += 1
                    self.move(x, y)
            case "<":
                if x == 0:
                    return False
                if self.map[y][x - 1]:
                    self.guard.direction = "^"
                else:
                    x -= 1
                    self.move(x, y)
        return True

    def move(self, x, y):
        self.visited_map[y][x] = True
        self.guard.position = (x, y)


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        map_state = MapState(line_iterator=file.readlines())
        if map_state.guard is None:
            raise ValueError("no guard on map")
        print(map_state)
        orig_guard = Guard(map_state.guard.position, map_state.guard.direction)
        while map_state.step():
            pass
        print(map_state)
        aggr = 0
        for new_obstacle in map_state.potential_new_obstacles():
            map = copy.deepcopy(map_state.map)
            if map[new_obstacle[1]][new_obstacle[0]]:
                raise ValueError(
                    f"obstacle already present at ({new_obstacle[0]}, {new_obstacle[1]})"
                )
            map[new_obstacle[1]][new_obstacle[0]] = True
            new_map_state = MapState(map_and_guard=(map, orig_guard))
            try:
                while new_map_state.step():
                    pass
            except LoopFound:
                # print(new_map_state)
                aggr += 1
        print(aggr)


if __name__ == "__main__":
    main()
