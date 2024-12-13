#!/bin/env python
import itertools
import pathlib
import re


BUTTON_EXPR_RE = re.compile(r"^Button\s+(\w+)\s*:\s*X\+(\d+)\s*,\s*Y\+(\d+)$")
PRIZE_EXPR_RE = re.compile(r"^Prize\s*:\s+X=(\d+)\s*,\s*Y=(\d+)$")


class Machine:
    def __init__(self, lines):
        self.button_vecs = {}
        self.prize_vec = None
        for line in lines:
            if m := BUTTON_EXPR_RE.match(line):
                self.button_vecs[m[1]] = (int(m[2]), int(m[3]))
            elif m := PRIZE_EXPR_RE.match(line):
                if self.prize_vec is not None:
                    raise ValueError("multiple prizes not supported")
                self.prize_vec = (int(m[1]), int(m[2]))
        if {"A", "B"} != set(self.button_vecs.keys()):
            raise ValueError("only exactly A and B buttons supported")
        if self.prize_vec is None:
            raise ValueError("no prize in machine")

    def play_game(self):
        ax = self.button_vecs["A"][0]
        ay = self.button_vecs["A"][1]
        bx = self.button_vecs["B"][0]
        by = self.button_vecs["B"][1]
        px = self.prize_vec[0]
        py = self.prize_vec[1]
        for a in range(100):
            x, y = (a * ax, a * ay)
            for b in range(100):
                if x > px or y > py:
                    break
                if x == px and y == py:
                    return 3 * a + b, True
                x += bx
                y += by
        return None, False


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    total_tokens = 0
    total_prizes = 0
    with open(filepath, "r") as file:
        while lines := tuple(
            line.strip() for line in itertools.islice(file, 4) if len(line.strip()) > 0
        ):
            machine = Machine(lines)
            tokens, won = machine.play_game()
            if won:
                total_tokens += tokens
                total_prizes += 1
    print(f"Prizes won: {total_prizes}, tokens spent: {total_tokens}")


if __name__ == "__main__":
    main()
