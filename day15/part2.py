#!/bin/env python
import pathlib


class Map:
    def __init__(self, lines):
        self.map = []
        self.robot_pos = None
        for y, line in enumerate(lines):
            self.map.append([])
            for x, ch in enumerate(line.strip()):
                match ch:
                    case "#":
                        self.map[y] += ["#", "#"]
                    case "O":
                        self.map[y] += ["[", "]"]
                    case ".":
                        self.map[y] += [".", "."]
                    case "@":
                        if self.robot_pos is not None:
                            raise ValueError("more than one robot not supported")
                        self.robot_pos = (2 * x, y)
                        self.map[y] += [".", "."]
                    case _:
                        raise ValueError(f"character '{ch}' in map not supported")
        self.height = len(self.map)
        self.width = len(self.map[0])

    def do(self, moves):
        for move in moves:
            match move:
                case "<":
                    self.move_left()
                case "^":
                    self.move_up()
                case ">":
                    self.move_right()
                case "v":
                    self.move_down()
                case _:
                    raise ValueError(f"move '{move}' not supported")
            print(f"{move}:\n{self}")

    def move_left(self):
        robot_x, robot_y = self.robot_pos
        for box_cnt in range(robot_x):
            # box_cnt is the number of box parts, not actual full boxes
            match ch := self.map[robot_y][robot_x - box_cnt - 1]:
                case "#":
                    # wall encountered before free space, do nothing
                    break
                case "[" | "]":
                    # box encountered
                    continue
                case ".":
                    # free space encountered, move the robot and all boxes
                    assert box_cnt % 2 == 0
                    robot_x -= 1
                    if box_cnt > 0:
                        self.map[robot_y][robot_x - box_cnt : robot_x + 1] = self.map[
                            robot_y
                        ][robot_x - box_cnt + 1 : robot_x + 2]
                    break
                case _:
                    raise ValueError(f"character '{ch}' in map not supported")
        else:
            raise ValueError("no wall or free space encountered")
        self.robot_pos = (robot_x, robot_y)

    def move_right(self):
        robot_x, robot_y = self.robot_pos
        for box_cnt in range(self.width - robot_x - 1):
            # box_cnt is the number of box parts, not actual full boxes
            match ch := self.map[robot_y][robot_x + box_cnt + 1]:
                case "#":
                    # wall encountered before free space, do nothing
                    break
                case "[" | "]":
                    # box encountered
                    continue
                case ".":
                    # free space encountered, move the robot and all boxes
                    assert box_cnt % 2 == 0
                    robot_x += 1
                    if box_cnt > 0:
                        self.map[robot_y][robot_x : robot_x + box_cnt + 1] = self.map[
                            robot_y
                        ][robot_x - 1 : robot_x + box_cnt]
                    break
                case _:
                    raise ValueError(f"character '{ch}' in map not supported")
        else:
            raise ValueError("no wall or free space encountered")
        self.robot_pos = (robot_x, robot_y)

    def move_up(self):
        robot_x, robot_y = self.robot_pos
        moving_xs_in_rows = [{robot_x}]
        for y in range(robot_y - 1, -1, -1):
            row_xs = set()
            for x in moving_xs_in_rows[-1]:
                match ch := self.map[y][x]:
                    case "#":
                        # wall encountered before free space, do nothing
                        return
                    case "[":
                        if x >= self.width - 1:
                            raise ValueError("left part of box cannot be at right edge")
                        row_xs |= {x, x + 1}
                    case "]":
                        if x < 1:
                            raise ValueError("right part of box cannot be at left edge")
                        row_xs |= {x - 1, x}
                    case ".":
                        continue
                    case _:
                        raise ValueError(f"character '{ch}' in map not supported")
            if len(row_xs) == 0:
                # no more moving boxes to check
                break
            moving_xs_in_rows.append(row_xs)
        else:
            raise ValueError("no wall or free space encountered")
        # move all box parts and robot up
        for dy, row_xs in reversed(list(enumerate(moving_xs_in_rows))):
            y = robot_y - dy
            assert y > 0
            for x in row_xs:
                self.map[y - 1][x] = self.map[y][x]
                self.map[y][x] = "."
        self.robot_pos = (robot_x, robot_y - 1)

    def move_down(self):
        robot_x, robot_y = self.robot_pos
        moving_xs_in_rows = [{robot_x}]
        for y in range(robot_y + 1, self.height):
            row_xs = set()
            for x in moving_xs_in_rows[-1]:
                match ch := self.map[y][x]:
                    case "#":
                        # wall encountered before free space, do nothing
                        return
                    case "[":
                        if x >= self.width - 1:
                            raise ValueError("left part of box cannot be at right edge")
                        row_xs |= {x, x + 1}
                    case "]":
                        if x < 1:
                            raise ValueError("right part of box cannot be at left edge")
                        row_xs |= {x - 1, x}
                    case ".":
                        continue
                    case _:
                        raise ValueError(f"character '{ch}' in map not supported")
            if len(row_xs) == 0:
                # no more moving boxes to check
                break
            moving_xs_in_rows.append(row_xs)
        else:
            raise ValueError("no wall or free space encountered")
        # move all box parts and robot up
        for dy, row_xs in reversed(list(enumerate(moving_xs_in_rows))):
            y = robot_y + dy
            assert y < self.height
            for x in row_xs:
                self.map[y + 1][x] = self.map[y][x]
                self.map[y][x] = "."
        self.robot_pos = (robot_x, robot_y + 1)

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
                if ch == "[":
                    aggr += gps(x, y)
        return aggr


def gps(x, y):
    return 100 * y + x


def main():
    for filename in (
        "input.hollow.test.txt",
        "input.large.example.txt",
        "input.small.example.txt",
        "input.txt",
    ):
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
