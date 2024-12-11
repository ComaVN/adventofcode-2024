#!/bin/env python
import collections
import math
import pathlib
from deepdiff import DeepDiff


def parse_line(line):
    return collections.Counter(int(v) for v in line.split(" "))


stones_after_blink = {}


def blink(stones):
    result = collections.Counter()
    for s, s_cnt in stones.items():
        if s not in stones_after_blink:
            if s == 0:
                new_stones = {1: 1}
            else:
                s_len = int(math.log10(s)) + 1
                if s_len % 2 == 0:
                    new_stones = collections.Counter(divmod(s, 10 ** (s_len // 2)))
                else:
                    new_stones = {s * 2024: 1}
            stones_after_blink[s] = new_stones
        result.update({k: s_cnt * v for k, v in stones_after_blink[s].items()})

    return result


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        stones = parse_line(file.readline())
    print(stones)
    for i in range(1, 76):
        stones = blink(stones)
        # print(stones)
        # print(f" {sum(stones.values())} ({len(stones)} different, (after {i} blinks)")
    print(sum(stones.values()))


if __name__ == "__main__":
    main()
