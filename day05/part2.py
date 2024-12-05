#!/bin/env python
import pathlib
import functools


def parse_order(ordering_rules, line):
    left, right = [int(p) for p in line.split("|")]
    ordering_rules[(left, right)] = True
    ordering_rules[(right, left)] = False


def parse_pages(line):
    return [int(p) for p in line.split(",")]


# This is merely to double-check our solution, it is not required for the solution itself.
def verify_order(ordering_rules, pages):
    for idx, page in enumerate(pages):
        for other_page in pages[:idx]:
            page_tup = (other_page, page)
            if page_tup in ordering_rules:
                if not ordering_rules[page_tup]:
                    return False
        for other_page in pages[idx + 1 :]:
            page_tup = (page, other_page)
            if page_tup in ordering_rules:
                if not ordering_rules[page_tup]:
                    return False
    return True


def page_rule_cmp(ordering_rules):
    def cmp(a, b):
        if (a, b) in ordering_rules:
            return -1 if ordering_rules[(a, b)] else 1
        else:
            return 0

    return cmp


# Returns the pages sorted according to the partial ordering defined by the rules, leaving the input unchanged.
def fix_order(ordering_rules, pages):
    return sorted(pages, key=functools.cmp_to_key(page_rule_cmp(ordering_rules)))


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    aggr = 0
    with open(filepath, "r") as file:
        reading_ordering = True
        ordering_rules = {}
        for line in file.readlines():
            line = line.strip()
            if reading_ordering:
                if line == "":
                    reading_ordering = False
                else:
                    parse_order(ordering_rules, line)
            else:
                pages = parse_pages(line)
                fixed_pages = fix_order(ordering_rules, pages)
                if pages == fixed_pages:
                    print(pages, ": valid")
                    if not verify_order(ordering_rules, pages):
                        print(" *** double-check failed for ", pages)
                else:
                    print(pages, ": fixed to: ", fixed_pages)
                    if not verify_order(ordering_rules, fixed_pages):
                        print(" *** double-check failed for ", fixed_pages)
                    aggr += fixed_pages[len(fixed_pages) // 2]

    print(aggr)


if __name__ == "__main__":
    main()
