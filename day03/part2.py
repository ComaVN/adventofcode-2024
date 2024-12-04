#!/bin/env python
import pathlib
import re

DODONT_SPLIT_RE = re.compile(r"do(n't)?\(\)")
MUL_EXPR_RE = re.compile(r"mul\(([1-9][0-9]{0,2}),([1-9][0-9]{0,2})\)")


def parse_line(line, enabled):
    chunks = DODONT_SPLIT_RE.split(line)
    muls = []
    for idx, chunk in enumerate(chunks):
        if idx % 2:
            enabled = not chunk
        elif enabled:
            muls += [tuple(int(v) for v in tup) for tup in MUL_EXPR_RE.findall(chunk)]
    return muls, enabled


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
        muls = []
        enabled = True
        for line in file.readlines():
            new_muls, enabled = parse_line(line, enabled)
            muls += new_muls
        aggr = 0
        for mul in muls:
            aggr += execute_mul(mul)
        print(aggr)


if __name__ == "__main__":
    main()
