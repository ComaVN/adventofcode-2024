#!/bin/env python
import pathlib


class Map:
    def __init__(self, lines):
        self.map = []
        self.robot_pos = None
        for y, line in enumerate(lines):
            self.map.append([])
            for x, ch in enumerate(line.strip()):
                if ch == "@":
                    if self.robot_pos is not None:
                        raise ValueError("more than one robot not supported")
                    self.robot_pos = (x, y)
                    ch = "."
                self.map[y].append(ch)
        self.height = len(self.map)
        self.width = len(self.map[0])

    def do(self, moves):
        robot_x, robot_y = self.robot_pos
        for move in moves:
            match move:
                case "<":
                    for box_cnt in range(robot_x):
                        match ch := self.map[robot_y][robot_x - box_cnt - 1]:
                            case "#":
                                # wall encountered before free space, do nothing
                                break
                            case "O":
                                # box encountered
                                continue
                            case ".":
                                # free space encountered, move the robot and all boxes
                                robot_x -= 1
                                if box_cnt > 0:
                                    self.map[robot_y][robot_x - box_cnt] = "O"
                                    self.map[robot_y][robot_x] = "."
                                break
                            case _:
                                raise ValueError(
                                    f"character '{ch}' in map not supported"
                                )
                    else:
                        raise ValueError("no wall or free space encountered")
                case "^":
                    for box_cnt in range(robot_y):
                        match ch := self.map[robot_y - box_cnt - 1][robot_x]:
                            case "#":
                                # wall encountered before free space, do nothing
                                break
                            case "O":
                                # box encountered
                                continue
                            case ".":
                                # free space encountered, move the robot and all boxes
                                robot_y -= 1
                                if box_cnt > 0:
                                    self.map[robot_y - box_cnt][robot_x] = "O"
                                    self.map[robot_y][robot_x] = "."
                                break
                            case _:
                                raise ValueError(
                                    f"character '{ch}' in map not supported"
                                )
                    else:
                        raise ValueError("no wall or free space encountered")
                case ">":
                    for box_cnt in range(self.width - robot_x - 1):
                        match ch := self.map[robot_y][robot_x + box_cnt + 1]:
                            case "#":
                                # wall encountered before free space, do nothing
                                break
                            case "O":
                                # box encountered
                                continue
                            case ".":
                                # free space encountered, move the robot and all boxes
                                robot_x += 1
                                if box_cnt > 0:
                                    self.map[robot_y][robot_x + box_cnt] = "O"
                                    self.map[robot_y][robot_x] = "."
                                break
                            case _:
                                raise ValueError(
                                    f"character '{ch}' in map not supported"
                                )
                    else:
                        raise ValueError("no wall or free space encountered")
                case "v":
                    for box_cnt in range(self.height - robot_y - 1):
                        match ch := self.map[robot_y + box_cnt + 1][robot_x]:
                            case "#":
                                # wall encountered before free space, do nothing
                                break
                            case "O":
                                # box encountered
                                continue
                            case ".":
                                # free space encountered, move the robot and all boxes
                                robot_y += 1
                                if box_cnt > 0:
                                    self.map[robot_y + box_cnt][robot_x] = "O"
                                    self.map[robot_y][robot_x] = "."
                                break
                            case _:
                                raise ValueError(
                                    f"character '{ch}' in map not supported"
                                )
                    else:
                        raise ValueError("no wall or free space encountered")
                case _:
                    raise ValueError(f"move '{move}' not supported")
        self.robot_pos = (robot_x, robot_y)

    def __str__(self):
        result = ""
        for y, line in enumerate(self.map):
            for x, ch in enumerate(line):
                if self.robot_pos == (x, y):
                    ch = "@"
                result += ch
            result += "\n"
        return result

    def gps_sum(self):
        aggr = 0
        for y, line in enumerate(self.map):
            for x, ch in enumerate(line):
                if ch == "O":
                    aggr += gps(x, y)
        return aggr


def gps(x, y):
    return 100 * y + x


def main():
    for filename in ("input.small.example.txt", "input.large.example.txt", "input.txt"):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            map_lines = []
            while map_line := file.readline().strip():
                map_lines.append(map_line)
            moves = tuple(d for line in file for d in line.strip())
        m = Map(map_lines)
        print(m)
        m.do(moves)
        print(m)
        print(m.gps_sum())


if __name__ == "__main__":
    main()
