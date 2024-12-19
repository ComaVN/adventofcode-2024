#!/bin/env python
import collections
import heapq
import pathlib


def match_design_to_patterns(design, patterns):
    to_do_heap = [0]
    heapq.heapify(to_do_heap)
    ways_to_get_to_pos = collections.defaultdict(int)
    ways_to_get_to_pos[0] = 1
    tried_pos = set()
    while len(to_do_heap) > 0:
        pos = heapq.heappop(to_do_heap)
        if pos == len(design):
            continue
        if pos in tried_pos:
            continue
        tried_pos.add(pos)
        for pattern in patterns:
            if len(pattern) > len(design) - pos:
                continue
            if design[pos : pos + len(pattern)] == pattern:
                ways_to_get_to_pos[pos + len(pattern)] += ways_to_get_to_pos[pos]
                heapq.heappush(to_do_heap, pos + len(pattern))

    return ways_to_get_to_pos[len(design)]


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
                if ways := match_design_to_patterns(design, patterns):
                    print(f"{ways} ways to match {design}")
                    aggr += ways
                else:
                    print(f"no way to match {design}")

            print(aggr)


if __name__ == "__main__":
    main()
