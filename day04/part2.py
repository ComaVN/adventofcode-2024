#!/bin/env python
import pathlib
import re

WIDTH = 140
POS_DIAGONAL_RE = re.compile(
    f"(?<=M.{{{WIDTH + 1}}})A(?=.{{{WIDTH + 1}}}S)|(?<=S.{{{WIDTH + 1}}})A(?=.{{{WIDTH + 1}}}M)",
    flags=re.DOTALL,
)
NEG_DIAGONAL_RE = re.compile(
    f"(?<=M.{{{WIDTH - 1}}})A(?=.{{{WIDTH - 1}}}S)|(?<=S.{{{WIDTH - 1}}})A(?=.{{{WIDTH - 1}}}M)",
    flags=re.DOTALL,
)


def count_xmas(puzzle):
    cnt = 0
    pos_diagonal_match_indices = {m.start() for m in POS_DIAGONAL_RE.finditer(puzzle)}
    for neg_m in NEG_DIAGONAL_RE.finditer(puzzle):
        if neg_m.start() in pos_diagonal_match_indices:
            cnt += 1
    return cnt


def execute_mul(mul):
    print(mul)
    return mul[0] * mul[1]


def safe(report):
    if len(report) < 1:
        return True
    prev = report[0]
    increasing = None
    for v in report[1:]:
        diff = v - prev
        if diff == 0:
            print("same", v, diff, report)
            return False
        if increasing is None:
            increasing = diff > 0
        if (diff > 0) != increasing:
            print("wrong direction", increasing, v, diff, report)
            return False
        if abs(diff) > 3:
            print("jump too large", increasing, v, diff, report)
            return False
        prev = v
    print("safe", increasing, v, diff, report)
    return True


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        puzzle = file.read()
        cnt = count_xmas(puzzle)
        print(cnt)


if __name__ == "__main__":
    main()
