#!/bin/env python
import collections
import pathlib


def main():
    left_counts = collections.defaultdict(int)
    right_counts = collections.defaultdict(int)
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        for line in file.readlines():
            left_item, right_item = line.strip().split("   ")
            left_int = int(left_item)
            right_int = int(right_item)
            left_counts[left_int] += 1
            right_counts[right_int] += 1
    # print(
    #     len(left_counts),
    #     "\n",
    #     left_counts,
    #     "\n",
    #     len(right_counts),
    #     "\n",
    #     right_counts,
    #     "\n",
    # )
    aggr = 0
    for left_value, left_count in left_counts.items():
        aggr += left_value*right_counts[left_value]
    print(aggr)


if __name__ == "__main__":
    main()
