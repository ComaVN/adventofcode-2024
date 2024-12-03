#!/bin/env python
import pathlib


def parse_report(line):
    return [int(value) for value in line.strip().split(" ")]


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
        safe_cnt = 0
        for line in file.readlines():
            report = parse_report(line)
            for idx in range(len(report),-1,-1):
                print(f"ignoring index {idx}")
                if safe(report[:idx] + report[idx + 1 :]):
                    safe_cnt += 1
                    break
        print(safe_cnt)


if __name__ == "__main__":
    main()
