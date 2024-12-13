#!/bin/env python
import itertools
import numpy as np
import pathlib
import re

BUTTON_EXPR_RE = re.compile(r"^Button\s+(\w+)\s*:\s*X\+(\d+)\s*,\s*Y\+(\d+)$")
PRIZE_EXPR_RE = re.compile(r"^Prize\s*:\s+X=(\d+)\s*,\s*Y=(\d+)$")


class Machine:
    prize_vec_diff = 10000000000000

    def __init__(self, lines):
        self.button_vecs = {}
        self.prize_vec = None
        for line in lines:
            if m := BUTTON_EXPR_RE.match(line):
                self.button_vecs[m[1]] = (int(m[2]), int(m[3]))
            elif m := PRIZE_EXPR_RE.match(line):
                if self.prize_vec is not None:
                    raise ValueError("multiple prizes not supported")
                self.prize_vec = (
                    Machine.prize_vec_diff + int(m[1]),
                    Machine.prize_vec_diff + int(m[2]),
                )
        if {"A", "B"} != set(self.button_vecs.keys()):
            raise ValueError("only exactly A and B buttons supported")
        if self.prize_vec is None:
            raise ValueError("no prize in machine")

    def play_game(self):
        ax, ay = self.button_vecs["A"]
        bx, by = self.button_vecs["B"]
        px, py = self.prize_vec
        coeff_matrix = np.column_stack(((ax, ay), (bx, by)))
        sol = np.linalg.solve(coeff_matrix, (px, py))
        a = int(round(sol[0]))
        b = int(round(sol[1]))
        if a * ax + b * bx == px and a * ay + b * by == py:
            return 3 * a + b, True
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
                print(f"Won prize using {tokens} tokens")
                total_tokens += tokens
                total_prizes += 1
    print(f"Prizes won: {total_prizes}, tokens spent: {total_tokens}")


if __name__ == "__main__":
    main()
