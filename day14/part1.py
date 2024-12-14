#!/bin/env python
import collections
import math
import pathlib
import re


ROBOT_EXPR_RE = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")


class Robot:
    def __init__(self, map, pos, velocity):
        self.map = map
        self.pos = tuple(pos)
        self.velocity = tuple(velocity)

    def tick(self, nr):
        self.pos = (
            (self.pos[0] + nr * self.velocity[0]) % self.map.width,
            (self.pos[1] + nr * self.velocity[1]) % self.map.height,
        )


class Map:
    def __init__(self, lines, width, height):
        self.width = width
        self.height = height
        self.robots = []
        for line in lines:
            if m := ROBOT_EXPR_RE.match(line):
                self.robots.append(
                    Robot(self, (int(m[1]), int(m[2])), (int(m[3]), int(m[4])))
                )
            else:
                raise ValueError("invalid robot line")

    def tick(self, nr):
        for robot in self.robots:
            robot.tick(nr)

    def safety_factor(self):
        cnt_per_q = collections.defaultdict(int)
        middle_x = self.width // 2
        middle_y = self.height // 2
        for robot in self.robots:
            if robot.pos[1] < middle_y:
                # top half
                if robot.pos[0] < middle_x:
                    # top-left quadrant
                    cnt_per_q[(0, 0)] += 1
                elif robot.pos[0] > middle_x:
                    # top-right quadrant
                    cnt_per_q[(1, 0)] += 1
            elif robot.pos[1] > middle_y:
                # bottom half
                if robot.pos[0] < middle_x:
                    # bottom-left quadrant
                    cnt_per_q[(0, 1)] += 1
                elif robot.pos[0] > middle_x:
                    # bottom-right quadrant
                    cnt_per_q[(1, 1)] += 1
        return math.prod(cnt_per_q.values())

    def __str__(self):
        cnt_per_position = collections.defaultdict(int)
        for robot in self.robots:
            cnt_per_position[robot.pos] += 1
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                cnt = cnt_per_position[(x, y)]
                result += (
                    format(cnt, "x") if 0 < cnt <= 15 else "*" if cnt > 15 else "."
                )
            result += "\n"
        return result


def main():
    filepath = pathlib.Path(__file__).parent / "input.example.txt"
    print(filepath)
    with open(filepath, "r") as file:
        m = Map(
            file.readlines(),
            width=11,
            height=7,
        )
    print(m)
    m.tick(100)
    print(m)
    print(m.safety_factor())

    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        m = Map(
            file.readlines(),
            width=101,
            height=103,
        )
    print(m)
    m.tick(100)
    print(m)
    print(m.safety_factor())


if __name__ == "__main__":
    main()
