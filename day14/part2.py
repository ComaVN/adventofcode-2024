#!/bin/env python
import collections
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
        self.tick_nr = 0

    def tick(self, nr):
        for robot in self.robots:
            robot.tick(nr)
        self.tick_nr += nr

    def __str__(self):
        cnt_per_position = collections.defaultdict(int)
        for robot in self.robots:
            cnt_per_position[robot.pos] += 1
        result = f"{'#'*self.width} (tick {self.tick_nr})\n"
        for y in range(self.height):
            for x in range(self.width):
                cnt = cnt_per_position[(x, y)]
                result += (
                    format(cnt, "x") if 0 < cnt <= 15 else "*" if cnt > 15 else " "
                )
            result += "\n"
        return result


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        m = Map(
            file.readlines(),
            width=101,
            height=103,
        )
    print(m)
    # I should probably just have searched ticks with rows of 10 1's or something, but hindsight is 20/20.
    start_tick = 23 # first tick that shows a vague column structure
    m.tick(start_tick)
    print(m)
    for _ in range(200): # every 103 ticks show a vague row structure
        m.tick(101) # every 101 ticks shows a vague column structure
        print(m)


if __name__ == "__main__":
    main()
