#!/bin/env python
import pathlib


def parse_line(line):
    test_value, remaining_line = line.strip().split(":", maxsplit=1)
    test_value = int(test_value)
    return test_value, [int(v) for v in remaining_line.split(" ") if v != ""]


def try_equation(test_value, numbers):
    bin_ops = {
        "+": lambda a, b: a + b,
        "*": lambda a, b: a * b,
    }

    def try_part(aggr, remaining_numbers):
        if len(remaining_numbers) == 0:
            return aggr == test_value
        next_number = remaining_numbers[0]
        for op in bin_ops.values():
            next_aggr = op(aggr, next_number)
            if next_aggr > test_value:
                continue
            if try_part(next_aggr, remaining_numbers[1:]):
                return True
        return False

    return test_value if try_part(numbers.pop(0), numbers) else 0


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    aggr = 0
    with open(filepath, "r") as file:
        for line in file.readlines():
            aggr += try_equation(*parse_line(line))
    print(aggr)


if __name__ == "__main__":
    main()
