#!/bin/env python
import pathlib
import re

WIDTH = 140
HORIZONTAL_RE = re.compile(r"X(?=MAS)", flags=re.DOTALL)
HORIZONTAL_REV_RE = re.compile(r"S(?=AMX)", flags=re.DOTALL)
VERTICAL_RE = re.compile(f"X(?=.{{{WIDTH}}}M.{{{WIDTH}}}A.{{{WIDTH}}}S)", flags=re.DOTALL)
VERTICAL_REV_RE = re.compile(f"S(?=.{{{WIDTH}}}A.{{{WIDTH}}}M.{{{WIDTH}}}X)", flags=re.DOTALL)
POS_DIAGONAL_RE = re.compile(f"X(?=.{{{WIDTH + 1}}}M.{{{WIDTH + 1}}}A.{{{WIDTH + 1}}}S)", flags=re.DOTALL)
POS_DIAGONAL_REV_RE = re.compile(f"S(?=.{{{WIDTH + 1}}}A.{{{WIDTH + 1}}}M.{{{WIDTH + 1}}}X)", flags=re.DOTALL)
NEG_DIAGONAL_RE = re.compile(f"X(?=.{{{WIDTH - 1}}}M.{{{WIDTH - 1}}}A.{{{WIDTH - 1}}}S)", flags=re.DOTALL)
NEG_DIAGONAL_REV_RE = re.compile(f"S(?=.{{{WIDTH - 1}}}A.{{{WIDTH - 1}}}M.{{{WIDTH - 1}}}X)", flags=re.DOTALL)


def count_xmas(puzzle):
    cnt = len(HORIZONTAL_RE.findall(puzzle))
    cnt += len(HORIZONTAL_REV_RE.findall(puzzle))
    cnt += len(VERTICAL_RE.findall(puzzle))
    cnt += len(VERTICAL_REV_RE.findall(puzzle))
    cnt += len(POS_DIAGONAL_RE.findall(puzzle))
    cnt += len(POS_DIAGONAL_REV_RE.findall(puzzle))
    cnt += len(NEG_DIAGONAL_RE.findall(puzzle))
    cnt += len(NEG_DIAGONAL_REV_RE.findall(puzzle))
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
