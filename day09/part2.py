#!/bin/env python
import pathlib


def parse_line(line):
    disk = []
    empty_ranges = []
    file_ranges = []
    file_cnt = 0
    for idx, ch in enumerate(line):
        if ch == "\n":
            break
        if idx % 2:
            # free space
            free_len = int(ch)
            if free_len > 0:
                empty_ranges.append((len(disk), free_len))
                disk += [None] * free_len
        else:
            # file
            file_len = int(ch)
            if file_len > 0:
                file_ranges.append((len(disk), file_len))
                disk += [file_cnt] * int(ch)
            else:
                raise ValueError("Unexpected 0-length file")
            file_cnt += 1
    return disk, file_ranges, empty_ranges


def defragment(disk, file_ranges, empty_ranges):
    for file_nr, file_range in reversed(list(enumerate(file_ranges))):
        file_idx = file_range[0]
        file_len = file_range[1]
        # print(disk, file_ranges, empty_ranges)
        for empty_nr, empty_range in enumerate(empty_ranges):
            empty_idx = empty_range[0]
            if file_idx < empty_idx:
                break
            empty_len = empty_range[1]
            if file_len > empty_len:
                continue
            disk[empty_idx : empty_idx + file_len] = [file_nr] * file_len
            disk[file_idx : file_idx + file_len] = [None] * file_len
            break
        # recalculate empty space
        empty_ranges = []
        empty_start = None
        empty_len = None
        for idx, v in enumerate(disk):
            if empty_start is None:
                if v is None:
                    empty_start = idx
                    empty_len = 1
            else:
                if v is None:
                    empty_len += 1
                else:
                    empty_ranges.append((empty_start, empty_len))
                    empty_start = None
                    empty_len = None


def checksum(disk):
    return sum([idx * id for idx, id in enumerate(disk) if id])


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        disk, file_ranges, empty_ranges = parse_line(file.readline())
    print(disk, file_ranges, empty_ranges)
    defragment(disk, file_ranges, empty_ranges)
    print(disk, file_ranges, empty_ranges)
    print(checksum(disk))


if __name__ == "__main__":
    main()
