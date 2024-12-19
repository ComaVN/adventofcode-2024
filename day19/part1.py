#!/bin/env python
import heapq
import pathlib
# import re


# def make_re(line):
#     patterns = [pattern.strip() for pattern in line.split(",")]
#     assert len(patterns) == len(set(patterns))
#     return re.compile(f"(?:{"|".join(patterns)})+")


def match_design_to_patterns(design, patterns):
    to_do_heap = [len(design)]
    tried_remaining = set()
    heapq.heapify(to_do_heap)
    while len(to_do_heap) > 0:
        remaining = heapq.heappop(to_do_heap)
        if remaining == 0:
            return True
        if remaining in tried_remaining:
            continue
        tried_remaining.add(remaining)
        pos = len(design) - remaining
        for pattern in patterns:
            if len(pattern) > remaining:
                continue
            if design[pos : pos + len(pattern)] == pattern:
                heapq.heappush(to_do_heap, remaining - len(pattern))

    return False


def main():
    for filename in (
        "input.tiny.example.txt",
        "input.example.txt",
        "input.txt",
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            patterns = [pattern.strip() for pattern in next(file).split(",")]
            patterns.sort(key=lambda s: -len(s))
            assert len(patterns) == len(set(patterns))
            assert next(file).strip() == ""
            aggr = 0
            for design in (line.strip() for line in file):
                if match_design_to_patterns(design, patterns):
                    aggr += 1
            print(aggr)


if __name__ == "__main__":
    main()
