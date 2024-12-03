#!/bin/env python
import pathlib


def parse_report(line):
    return tuple(int(value) for value in line.strip().split(" "))


def safe(report):
    if len(report) < 2:
        return True
    if report[0] == report[1]:
        return False
    increasing = True if report[1] > report[0] else False
    if abs(report[1] - report[0]) > 3:
        return False
    prev = report[1]
    for v in report[2:]:
        diff = v - prev
        if diff == 0:
            print("same", increasing, v, diff, report)
            return False
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
        print(len([None for line in file.readlines() if safe(parse_report(line))]))


if __name__ == "__main__":
    main()
