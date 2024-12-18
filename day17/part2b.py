#!/bin/env python
import pathlib


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
            self.ip = operand - 2

    def bxc(self, operand):
        self.B ^= self.C

    def out(self, operand):
        value = self.combo_operand(operand) % 8
        # if len(self.output) >= len(self.prog):
        #     raise RuntimeError(
        #         # f"output {self.output} longer than program {self.prog}"
        #     )
        # if value != self.prog[len(self.output)]:
        #     raise RuntimeError(
        #         # f"next output {value} at position {len(self.output)} ({self.output}) does not match program {self.prog}"
        #     )
        self.output.append(value)

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
        self.A = self.orig_A = int(next(lines).split(":", 1)[1].strip())
        self.B = self.orig_B = int(next(lines).split(":", 1)[1].strip())
        self.C = self.orig_C = int(next(lines).split(":", 1)[1].strip())
        assert next(lines).strip() == ""
        self.prog = [int(op.strip()) for op in next(lines).split(":", 1)[1].split(",")]
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
        while self.ip < len(self.prog) - 1:
            assert self.ip >= 0
            assert self.ip % 2 == 0
            opcode = self.prog[self.ip]
            operand = self.prog[self.ip + 1]
            self.INSTRUCTIONS[opcode](self, operand)
            self.ip += 2
        return self.output

    def reset(self, A):
        self.output = []
        self.ip = 0
        self.A = A
        self.B = self.orig_B
        self.C = self.orig_C


def main():
    filepath = pathlib.Path(__file__).parent / "input.txt"
    print(filepath)
    with open(filepath, "r") as file:
        computer = Computer(file)
    print(computer)
    # Program: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
    #
    # BST A
    # BXL 1
    # CDV B
    # BXL 5
    # BXC
    # OUT B
    # ADV 3
    # JNZ 0
    #
    # repeat:
    #   B = A % 8
    #   B = B ^ 0b1
    #   C = A >> B
    #   B = B ^ 0b101
    #   B = B ^ C
    #   print(B % 8)
    #   A = A >> 3
    # until A == 0
    possible_A = {1}
    solutions = set()
    output = []
    while possible_A:
        A = possible_A.pop()
        for A in range(A, A + 8):
            computer.reset(A=A)
            output = computer.run()
            print(f"A = {A}:", ",".join(map(str, output)))
            if output == computer.prog[-len(output) :]:
                # output using A matches end of program
                if len(output) == len(computer.prog):
                    solutions.add(A)
                    print("Found")
                possible_A.add(8 * A)
    print(f"Solutions: {solutions}")
    print(f"Lowest solution: {min(solutions)}")


if __name__ == "__main__":
    main()
