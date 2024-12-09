#!/bin/env python
import pathlib


def parse_line(line):
    disk = []
    file_cnt = 0
    for idx, ch in enumerate(line):
        if ch == "\n":
            break
        if idx % 2:
            # free space
            disk += [None] * int(ch)
        else:
            # file
            disk += [file_cnt] * int(ch)
            file_cnt += 1
    return disk


def defragment(disk):
    for empty_idx, file_block_idx in zip(
        (idx for idx, id in enumerate(disk) if id is None),
        (
            len(disk) - 1 - idx
            for idx, id in enumerate(reversed(disk))
            if id is not None
        ),
    ):
        # print(empty_idx, file_block_idx)
        if file_block_idx < empty_idx:
            break
        disk[empty_idx] = disk[file_block_idx]
        disk[file_block_idx] = None


def checksum(disk):
    return sum([idx * id for idx, id in enumerate(disk) if id])


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        disk = parse_line(file.readline())
    print(disk)
    defragment(disk)
    print(disk)
    print(checksum(disk))


if __name__ == "__main__":
    main()
