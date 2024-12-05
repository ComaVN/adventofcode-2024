#!/bin/env python
import pathlib
import collections


def parse_order(ordering_rules, line):
    left, right = [int(p) for p in line.split("|")]
    ordering_rules[left]["lt"].add(right)
    ordering_rules[right]["gt"].add(left)


def parse_pages(line):
    return [int(p) for p in line.split(",")]


def verify_order(ordering_rules, pages):
    valid = True
    for idx, page in enumerate(pages):
        if page in ordering_rules:
            page_rule = ordering_rules[page]
            if set(pages[:idx]) & page_rule["lt"]:
                valid = False
                break
            if set(pages[idx + 1 :]) & page_rule["gt"]:
                valid = False
                break
    return valid


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    aggr = 0
    with open(filepath, "r") as file:
        reading_ordering = True
        ordering_rules = collections.defaultdict(lambda: {"lt": set(), "gt": set()})
        for line in file.readlines():
            line = line.strip()
            if reading_ordering:
                if line == "":
                    reading_ordering = False
                else:
                    parse_order(ordering_rules, line)
            else:
                pages = parse_pages(line)
                if verify_order(ordering_rules, pages):
                    print(pages, ": valid")
                    aggr += pages[len(pages) // 2]
                else:
                    print(pages, ": invalid")
    print(aggr)


if __name__ == "__main__":
    main()
