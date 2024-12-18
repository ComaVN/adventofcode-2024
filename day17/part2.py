#!/bin/env python
import pathlib
import sys


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
        if len(self.output) >= len(self.prog):
            raise RuntimeError(
                # f"output {self.output} longer than program {self.prog}"
            )
        if value != self.prog[len(self.output)]:
            raise RuntimeError(
                # f"next output {value} at position {len(self.output)} ({self.output}) does not match program {self.prog}"
            )
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
    sys.stdout.reconfigure(line_buffering=True)
    for filename in (
        # "input.example.txt",
        # "input.quine.example.txt",
        "input.txt",
    ):
        filepath = pathlib.Path(__file__).parent / filename
        print(filepath)
        with open(filepath, "r") as file:
            computer = Computer(file)
        print(computer)
        # up to 700000000 has been exhaustively searched:
        # A = 6: 2
        # A = 14: 2,4                                                                               +8 = 2^3 = 0b100
        # A = 332: 2,4,1                                                                            +318 :/
        # A = 23948989: 2,4,1,1,7,5,1,5,4                                                           +23948657 :/
        # A = 23949245: 2,4,1,1,7,5,1,5,4                                                           +256
        # A = 695037629: 2,4,1,1,7,5,1,5,4,1                                                        +671088640 = 2^29+2^27 = 0b101000000000000000000000000000
        # A = 695037885: 2,4,1,1,7,5,1,5,4,1                                                        +256
        # these have been found jumping up by 0x4000000:
        # A = 3894888197821 (3894888197821 + offset 0): 2,4,1,1,7,5,1,5,4,1,5,5,0,3
        # A = 3894888198077 (3894888197821 + offset 256): 2,4,1,1,7,5,1,5,4,1,5,5,0,3
        # A = 3894955306685 (3894955306685 + offset 0): 2,4,1,1,7,5,1,5,4,1,5,5,0,3
        # A = 3894955306941 (3894955306685 + offset 256): 2,4,1,1,7,5,1,5,4,1,5,5,0,3
        # A = 34681213775549 (34681213775549 + offset 0): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3
        # A = 34681213775805 (34681213775549 + offset 256): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3
        # A = 34681280884413 (34681280884413 + offset 0): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3
        # A = 34681280884669 (34681280884413 + offset 256): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3
        # A = 164278764924605 (164278764924605 + offset 0): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        # A = 164278764924861 (164278764924605 + offset 256): 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        # these are quines, but not the lowest, apparently:
        # A = 164281851932349: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        # A = 164281851932605: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        # this one is lower:
        # A = 164281784823741: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
        A = 695037629
        output = []
        while output != computer.prog:
            # if A % 0x28000000 * 100000 == 695037629 % 0x28000000:
            #     print(A)
            for offset in range(-512, 768, 256):
                computer.reset(A=A + offset)
                try:
                    output = computer.run()
                    print(f"A = {A+offset} ({A} + offset {offset}):", ",".join(map(str, output)))
                except RuntimeError:
                    pass
            A += 0x4000000


if __name__ == "__main__":
    main()
