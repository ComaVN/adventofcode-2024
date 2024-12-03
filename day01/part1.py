#!/bin/env python
import pathlib


def main():
    left_list = []
    right_list = []
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        for line in file.readlines():
            values = line.strip().split("   ")
            left_list.append(int(values[0]))
            right_list.append(int(values[1]))
    left_list.sort()
    right_list.sort()
    # print(
    #     len(left_list), "\n", left_list, "\n", len(right_list), "\n", right_list, "\n"
    # )
    aggr = 0
    for idx, left_value in enumerate(left_list):
        aggr += abs(left_value - right_list[idx])
    print(aggr)


if __name__ == "__main__":
    main()
