#!/bin/env python
import pathlib
import itertools


class Computer:
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    def adv(self, operand):
        self.A >>= self.combo_operand(operand)

    def bxl(self, operand):
        self.B ^= operand

    def bst(self, operand):
        self.B = self.combo_operand(operand) % 8

    def jnz(self, operand):
        if self.A != 0:
            assert operand % 2 == 0
            self.ip = (operand >> 1) - 1

    def bxc(self, operand):
        self.B ^= self.C

    def out(self, operand):
        self.output.append(self.combo_operand(operand) % 8)

    def bdv(self, operand):
        self.B = self.A >> self.combo_operand(operand)

    def cdv(self, operand):
        self.C = self.A >> self.combo_operand(operand)

    INSTRUCTIONS = {
        ADV: adv,
        BXL: bxl,
        BST: bst,
        JNZ: jnz,
        BXC: bxc,
        OUT: out,
        BDV: bdv,
        CDV: cdv,
    }

    def __init__(self, lines):
        self.A = int(next(lines).split(":", 1)[1].strip())
        self.B = int(next(lines).split(":", 1)[1].strip())
        self.C = int(next(lines).split(":", 1)[1].strip())
        assert next(lines).strip() == ""
        self.prog = [
            (int(opcode.strip()), int(operand.strip()))
            for opcode, operand in itertools.batched(
                next(lines).split(":", 1)[1].split(","), 2
            )
        ]
        self.ip = 0
        self.output = []

    def __str__(self):
        return f"A: {self.A}, B: {self.B}, C: {self.C}, prog: {self.prog}"

    def combo_operand(self, operand):
        match operand:
            case x if x <= 3:
                return x
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise ValueError(f"Reserved operand {operand}")
            case _:
                raise ValueError(f"Invalid combo operand {operand}")

    def run(self):
        self.output = []
        self.ip = 0
        while self.ip < len(self.prog):
            assert self.ip >= 0
            op = self.prog[self.ip]
            self.INSTRUCTIONS[op[0]](self, op[1])
            self.ip += 1
        return self.output


def main():
    for filename in (
        "input.example.txt",
        "input.quine.example.txt",
        "input.txt",
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            computer = Computer(file)
        print(computer)
        print(",".join(map(str, computer.run())))


if __name__ == "__main__":
    main()
