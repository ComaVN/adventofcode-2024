#!/bin/env python
import pathlib


def parse_line(line):
    return tuple((int(v) for v in line.split(" ")))


def blink(stones):
    result = []
    for s in stones:
        sstr = str(s)
        if s == 0:
            result.append(1)
        elif len(sstr) % 2 == 0:
            result.append(int(sstr[: len(sstr) // 2]))
            result.append(int(sstr[len(sstr) // 2 :]))
        else:
            result.append(s * 2024)

    return tuple(result)


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        stones = parse_line(file.readline())
    print(stones)
    for i in range(1, 26):
        stones = blink(stones)
        print(stones)
        print(f" (after {i} blinks)")
    print(len(stones))


if __name__ == "__main__":
    main()
